# Copyright (c) 2019-2021 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/boschresearch/pylife
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

__author__ = "Johannes Mueller"
__maintainer__ = __author__

import numpy as np
import pandas as pd

from pylife.materiallaws import WoehlerCurve
import pylife.stress.rainflow


@pd.api.extensions.register_series_accessor('fatigue')
@pd.api.extensions.register_dataframe_accessor('fatigue')
class Fatigue(WoehlerCurve):

    def damage(self, load_hist):
        cycles = self.basquin_cycles(load_hist.amplitude)

        result = load_hist.cycles.divide(cycles, axis=0)
        result.name = 'damage'
        return result

    def security_load(self, load, cycles, allowed_failure_probability):
        allowed_load = self.basquin_load(cycles, allowed_failure_probability)
        return allowed_load / load.sigma_a

    def security_cycles(self, cycles, load, allowed_failure_probability):
        allowed_cycles = self.basquin_cycles(load.sigma_a, allowed_failure_probability)
        return allowed_cycles / cycles
