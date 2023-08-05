# Copyright 2021 Sony Corporation.
# Copyright 2021 Sony Group Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from typing import Any, Dict, Union, cast

import gym
import numpy as np

import nnabla as nn
import nnabla.solvers as NS
import nnabla_rl.environment_explorers as EE
import nnabla_rl.model_trainers as MT
from nnabla_rl.algorithm import Algorithm, AlgorithmConfig, eval_api
from nnabla_rl.builders import ExplorerBuilder, ModelBuilder, ReplayBufferBuilder, SolverBuilder
from nnabla_rl.environment_explorer import EnvironmentExplorer
from nnabla_rl.environment_explorers.epsilon_greedy_explorer import epsilon_greedy_action_selection
from nnabla_rl.environments.environment_info import EnvironmentInfo
from nnabla_rl.model_trainers.model_trainer import ModelTrainer, TrainingBatch
from nnabla_rl.models import DQNQFunction, QFunction
from nnabla_rl.replay_buffer import ReplayBuffer
from nnabla_rl.utils import context
from nnabla_rl.utils.data import add_batch_dimension, marshal_experiences, set_data_to_variable
from nnabla_rl.utils.misc import create_variable, sync_model


@dataclass
class MunchausenDQNConfig(AlgorithmConfig):
    """
    List of configurations for Munchausen DQN algorithm

    Args:
        gamma (float): discount factor of rewards. Defaults to 0.99.
        learning_rate (float): learning rate which is set to all solvers. \
            You can customize/override the learning rate for each solver by implementing the \
            (:py:class:`SolverBuilder <nnabla_rl.builders.SolverBuilder>`) by yourself. \
            Defaults to 0.00005.
        batch_size (int): training batch size. Defaults to 32.
        num_steps (int): number of steps for N-step Q targets. Defaults to 1.
        learner_update_frequency (int): the interval of learner update. Defaults to 4
        target_update_frequency (int): the interval of target q-function update. Defaults to 10000.
        start_timesteps (int): the timestep when training starts.\
            The algorithm will collect experiences from the environment by acting randomly until this timestep.
            Defaults to 50000.
        replay_buffer_size (int): the capacity of replay buffer. Defaults to 1000000.
        max_explore_steps (int): the number of steps decaying the epsilon value.\
            The epsilon will be decayed linearly \
            :math:`\\epsilon=\\epsilon_{init} - step\\times\\frac{\\epsilon_{init} - \
            \\epsilon_{final}}{max\\_explore\\_steps}`.\
            Defaults to 1000000.
        initial_epsilon (float): the initial epsilon value for ε-greedy explorer. Defaults to 1.0.
        final_epsilon (float): the last epsilon value for ε-greedy explorer. Defaults to 0.01.
        test_epsilon (float): the epsilon value on testing. Defaults to 0.001.
        entropy_temperature (float): temperature parameter of softmax policy distribution. Defaults to 0.03.
        munchausen_scaling_term (float): scalar of scaled log policy. Defaults to 0.9.
        clipping_value (float): Lower value of the logarithm of policy distribution. Defaults to -1.
    """

    gamma: float = 0.99
    learning_rate: float = 0.00005
    batch_size: int = 32
    num_steps: int = 1
    # network update
    learner_update_frequency: float = 4
    target_update_frequency: float = 10000
    # buffers
    start_timesteps: int = 50000
    replay_buffer_size: int = 1000000
    # explore
    max_explore_steps: int = 1000000
    initial_epsilon: float = 1.0
    final_epsilon: float = 0.01
    test_epsilon: float = 0.001
    # munchausen dqn training parameters
    entropy_temperature: float = 0.03
    munchausen_scaling_term: float = 0.9
    clipping_value: float = -1

    def __post_init__(self):
        '''__post_init__

        Check set values are in valid range.

        '''
        self._assert_between(self.gamma, 0.0, 1.0, 'gamma')
        self._assert_positive(self.batch_size, 'batch_size')
        self._assert_positive(self.num_steps, 'num_steps')
        self._assert_positive(self.learning_rate, 'learning_rate')
        self._assert_positive(self.learner_update_frequency, 'learner_update_frequency')
        self._assert_positive(self.target_update_frequency, 'target_update_frequency')
        self._assert_positive(self.start_timesteps, 'start_timesteps')
        self._assert_smaller_than(self.start_timesteps, self.replay_buffer_size, 'start_timesteps')
        self._assert_positive(self.replay_buffer_size, 'replay_buffer_size')
        self._assert_between(self.initial_epsilon, 0.0, 1.0, 'initial_epsilon')
        self._assert_between(self.final_epsilon, 0.0, 1.0, 'final_epsilon')
        self._assert_between(self.test_epsilon, 0.0, 1.0, 'test_epsilon')
        self._assert_positive(self.max_explore_steps, 'max_explore_steps')
        self._assert_negative(self.clipping_value, 'clipping_value')


class DefaultQFunctionBuilder(ModelBuilder[QFunction]):
    def build_model(self,  # type: ignore[override]
                    scope_name: str,
                    env_info: EnvironmentInfo,
                    algorithm_config: MunchausenDQNConfig,
                    **kwargs) -> QFunction:
        return DQNQFunction(scope_name, env_info.action_dim)


class DefaultQSolverBuilder(SolverBuilder):
    def build_solver(self,  # type: ignore[override]
                     env_info: EnvironmentInfo,
                     algorithm_config: MunchausenDQNConfig,
                     **kwargs) -> nn.solvers.Solver:
        assert isinstance(algorithm_config, MunchausenDQNConfig)
        return NS.Adam(algorithm_config.learning_rate, eps=1e-2 / algorithm_config.batch_size)


class DefaultReplayBufferBuilder(ReplayBufferBuilder):
    def build_replay_buffer(self,  # type: ignore[override]
                            env_info: EnvironmentInfo,
                            algorithm_config: MunchausenDQNConfig,
                            **kwargs) -> ReplayBuffer:
        assert isinstance(algorithm_config, MunchausenDQNConfig)
        return ReplayBuffer(capacity=algorithm_config.replay_buffer_size)


class DefaultExplorerBuilder(ExplorerBuilder):
    def build_explorer(self,  # type: ignore[override]
                       env_info: EnvironmentInfo,
                       algorithm_config: MunchausenDQNConfig,
                       algorithm: "MunchausenDQN",
                       **kwargs) -> EnvironmentExplorer:
        explorer_config = EE.LinearDecayEpsilonGreedyExplorerConfig(
            warmup_random_steps=algorithm_config.start_timesteps,
            initial_step_num=algorithm.iteration_num,
            initial_epsilon=algorithm_config.initial_epsilon,
            final_epsilon=algorithm_config.final_epsilon,
            max_explore_steps=algorithm_config.max_explore_steps
        )
        explorer = EE.LinearDecayEpsilonGreedyExplorer(
            greedy_action_selector=algorithm._greedy_action_selector,
            random_action_selector=algorithm._random_action_selector,
            env_info=env_info,
            config=explorer_config)
        return explorer


class MunchausenDQN(Algorithm):
    '''Munchausen-DQN algorithm.

    This class implements the Munchausen-DQN (Munchausen Deep Q Network) algorithm
    proposed by N. Vieillard, et al. in the paper: "Munchausen Reinforcement Learning"
    For details see: https://proceedings.neurips.cc/paper/2020/file/2c6a0bae0f071cbbf0bb3d5b11d90a82-Paper.pdf

    Args:
        env_or_env_info\
        (gym.Env or :py:class:`EnvironmentInfo <nnabla_rl.environments.environment_info.EnvironmentInfo>`):
            the environment to train or environment info
        config (:py:class:`MunchausenDQNConfig <nnabla_rl.algorithms.munchausen_dqn.MunchausenDQNConfig>`):
            configuration of MunchausenDQN algorithm
        q_func_builder (:py:class:`ModelBuilder[QFunction] <nnabla_rl.builders.ModelBuilder>`):
            builder of q-function models
        q_solver_builder (:py:class:`SolverBuilder <nnabla_rl.builders.SolverBuilder>`):
            builder for q-function solvers
        replay_buffer_builder (:py:class:`ReplayBufferBuilder <nnabla_rl.builders.ReplayBufferBuilder>`):
            builder of replay_buffer
        explorer_builder (:py:class:`ExplorerBuilder <nnabla_rl.builders.ExplorerBuilder>`):
            builder of environment explorer
    '''

    # type declarations to type check with mypy
    # NOTE: declared variables are instance variable and NOT class variable, unless it is marked with ClassVar
    # See https://mypy.readthedocs.io/en/stable/class_basics.html for details
    _config: MunchausenDQNConfig
    _q: QFunction
    _target_q: QFunction
    _q_solver: nn.solver.Solver
    _replay_buffer: ReplayBuffer

    _explorer_builder: ExplorerBuilder
    _environment_explorer: EnvironmentExplorer
    _q_function_trainer: ModelTrainer

    _eval_state_var: nn.Variable
    _a_greedy: nn.Variable

    _q_function_trainer_state: Dict[str, Any]

    def __init__(self, env_or_env_info: Union[gym.Env, EnvironmentInfo],
                 config: MunchausenDQNConfig = MunchausenDQNConfig(),
                 q_func_builder: ModelBuilder[QFunction] = DefaultQFunctionBuilder(),
                 q_solver_builder: SolverBuilder = DefaultQSolverBuilder(),
                 replay_buffer_builder: ReplayBufferBuilder = DefaultReplayBufferBuilder(),
                 explorer_builder: ExplorerBuilder = DefaultExplorerBuilder()):
        super(MunchausenDQN, self).__init__(env_or_env_info, config=config)

        self._explorer_builder = explorer_builder

        with nn.context_scope(context.get_nnabla_context(self._config.gpu_id)):
            self._q = q_func_builder(scope_name='q', env_info=self._env_info, algorithm_config=self._config)
            self._q_solver = q_solver_builder(env_info=self._env_info, algorithm_config=self._config)
            self._target_q = cast(QFunction, self._q.deepcopy('target_' + self._q.scope_name))

            self._replay_buffer = replay_buffer_builder(env_info=self._env_info, algorithm_config=self._config)

    @eval_api
    def compute_eval_action(self, state):
        with nn.context_scope(context.get_nnabla_context(self._config.gpu_id)):
            (action, _), _ = epsilon_greedy_action_selection(state,
                                                             self._greedy_action_selector,
                                                             self._random_action_selector,
                                                             epsilon=self._config.test_epsilon)
            return action

    def _before_training_start(self, env_or_buffer):
        # set context globally to ensure that the training runs on configured gpu
        context.set_nnabla_context(self._config.gpu_id)
        self._environment_explorer = self._setup_environment_explorer(env_or_buffer)
        self._q_function_trainer = self._setup_q_function_training(env_or_buffer)

    def _setup_environment_explorer(self, env_or_buffer):
        return None if self._is_buffer(env_or_buffer) else self._explorer_builder(self._env_info, self._config, self)

    def _setup_q_function_training(self, env_or_buffer):
        trainer_config = MT.q_value_trainers.MunchausenDQNQTrainerConfig(
            num_steps=self._config.num_steps,
            reduction_method='mean',
            q_loss_scalar=0.5,
            grad_clip=(-1.0, 1.0),
            tau=self._config.entropy_temperature,
            alpha=self._config.munchausen_scaling_term,
            clip_min=self._config.clipping_value,
            clip_max=0.0)

        q_function_trainer = MT.q_value_trainers.MunchausenDQNQTrainer(
            train_functions=self._q,
            solvers={self._q.scope_name: self._q_solver},
            target_function=self._target_q,
            env_info=self._env_info,
            config=trainer_config)
        sync_model(self._q, self._target_q)
        return q_function_trainer

    def _run_online_training_iteration(self, env):
        experiences = self._environment_explorer.step(env)
        self._replay_buffer.append_all(experiences)
        if self._config.start_timesteps < self.iteration_num:
            if self.iteration_num % self._config.learner_update_frequency == 0:
                self._m_dqn_training(self._replay_buffer)

    def _run_offline_training_iteration(self, buffer):
        self._m_dqn_training(buffer)

    @eval_api
    def _greedy_action_selector(self, s):
        s = add_batch_dimension(s)
        if not hasattr(self, '_eval_state_var'):
            self._eval_state_var = create_variable(1, self._env_info.state_shape)
            self._a_greedy = self._q.argmax_q(self._eval_state_var)
        set_data_to_variable(self._eval_state_var, s)
        self._a_greedy.forward()
        return np.squeeze(self._a_greedy.d, axis=0), {}

    def _random_action_selector(self, s):
        action = self._env_info.action_space.sample()
        return np.asarray(action).reshape((1, )), {}

    def _m_dqn_training(self, replay_buffer):
        experiences_tuple, info = replay_buffer.sample(self._config.batch_size, num_steps=self._config.num_steps)
        if self._config.num_steps == 1:
            experiences_tuple = (experiences_tuple, )
        assert len(experiences_tuple) == self._config.num_steps

        batch = None
        for experiences in reversed(experiences_tuple):
            (s, a, r, non_terminal, s_next, *_) = marshal_experiences(experiences)
            batch = TrainingBatch(batch_size=self._config.batch_size,
                                  s_current=s,
                                  a_current=a,
                                  gamma=self._config.gamma,
                                  reward=r,
                                  non_terminal=non_terminal,
                                  s_next=s_next,
                                  weight=info['weights'],
                                  next_step_batch=batch)

        self._q_function_trainer_state = self._q_function_trainer.train(batch)
        if self.iteration_num % self._config.target_update_frequency == 0:
            sync_model(self._q, self._target_q)

        td_errors = self._q_function_trainer_state['td_errors']
        replay_buffer.update_priorities(td_errors)

    def _models(self):
        models = {}
        models[self._q.scope_name] = self._q
        return models

    def _solvers(self):
        solvers = {}
        solvers[self._q.scope_name] = self._q_solver
        return solvers

    @classmethod
    def is_supported_env(cls, env_or_env_info):
        env_info = EnvironmentInfo.from_env(env_or_env_info) if isinstance(env_or_env_info, gym.Env) \
            else env_or_env_info
        return not env_info.is_continuous_action_env()

    @property
    def latest_iteration_state(self):
        latest_iteration_state = super(MunchausenDQN, self).latest_iteration_state
        if hasattr(self, '_q_function_trainer_state'):
            latest_iteration_state['scalar'].update({'q_loss': self._q_function_trainer_state['q_loss']})
            latest_iteration_state['histogram'].update(
                {'td_errors': self._q_function_trainer_state['td_errors'].flatten()})
        return latest_iteration_state
