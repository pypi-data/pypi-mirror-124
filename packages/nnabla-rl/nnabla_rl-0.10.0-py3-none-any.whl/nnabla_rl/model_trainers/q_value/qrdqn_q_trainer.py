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
from nnabla_rl.model_trainers.q_value.quantile_distribution_function_trainer import (
    QuantileDistributionFunctionTrainer, QuantileDistributionFunctionTrainerConfig)
from nnabla_rl.models import QuantileDistributionFunction


@dataclass
class QRDQNQTrainerConfig(QuantileDistributionFunctionTrainerConfig):
    pass


class QRDQNQTrainer(QuantileDistributionFunctionTrainer):
    # type declarations to type check with mypy
    # NOTE: declared variables are instance variable and NOT class variable, unless it is marked with ClassVar
    # See https://mypy.readthedocs.io/en/stable/class_basics.html for details
    _target_function: QuantileDistributionFunction

    def __init__(self,
                 train_functions: Union[QuantileDistributionFunction, Sequence[QuantileDistributionFunction]],
                 solvers: Dict[str, nn.solver.Solver],
                 target_function: QuantileDistributionFunction,
                 env_info: EnvironmentInfo,
                 config: QRDQNQTrainerConfig = QRDQNQTrainerConfig()):
        self._target_function = target_function
        super(QRDQNQTrainer, self).__init__(train_functions, solvers, env_info, config)

    def _compute_target(self, training_variables: TrainingVariables, **kwargs) -> nn.Variable:
        gamma = training_variables.gamma
        reward = training_variables.reward
        non_terminal = training_variables.non_terminal
        s_next = training_variables.s_next

        theta_j = self._target_function.max_q_quantiles(s_next)
        Ttheta_j = reward + non_terminal * gamma * theta_j
        return Ttheta_j
