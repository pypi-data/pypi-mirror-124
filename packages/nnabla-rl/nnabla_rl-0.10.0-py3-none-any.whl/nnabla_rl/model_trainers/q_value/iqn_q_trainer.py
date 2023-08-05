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
from typing import Dict, Sequence, Union

import nnabla as nn
from nnabla_rl.environments.environment_info import EnvironmentInfo
from nnabla_rl.model_trainers.model_trainer import TrainingVariables
from nnabla_rl.model_trainers.q_value.state_action_quantile_function_trainer import (
    StateActionQuantileFunctionTrainer, StateActionQuantileFunctionTrainerConfig)
from nnabla_rl.models import StateActionQuantileFunction


@dataclass
class IQNQTrainerConfig(StateActionQuantileFunctionTrainerConfig):
    pass


class IQNQTrainer(StateActionQuantileFunctionTrainer):
    # type declarations to type check with mypy
    # NOTE: declared variables are instance variable and NOT class variable, unless it is marked with ClassVar
    # See https://mypy.readthedocs.io/en/stable/class_basics.html for details
    _target_function: StateActionQuantileFunction

    def __init__(self,
                 train_functions: Union[StateActionQuantileFunction, Sequence[StateActionQuantileFunction]],
                 solvers: Dict[str, nn.solver.Solver],
                 target_function: StateActionQuantileFunction,
                 env_info: EnvironmentInfo,
                 config: IQNQTrainerConfig = IQNQTrainerConfig()):
        self._target_function = target_function
        super(IQNQTrainer, self).__init__(train_functions, solvers, env_info, config)

    def _compute_target(self, training_variables: TrainingVariables) -> nn.Variable:
        gamma = training_variables.gamma
        reward = training_variables.reward
        non_terminal = training_variables.non_terminal
        s_next = training_variables.s_next

        batch_size = training_variables.batch_size
        N_prime = self._config.N_prime

        tau_j = self._target_function.sample_tau(shape=(batch_size, N_prime))
        Z_tau_j = self._target_function.max_q_quantile_values(s_next, tau_j)
        assert Z_tau_j.shape == (batch_size, N_prime)
        target = reward + non_terminal * gamma * Z_tau_j
        return target
