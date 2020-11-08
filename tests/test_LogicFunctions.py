import numpy as np
from typing import List
import pandas as pd
import numpy as np
import pytest
from application import appsettings as config
from application.functions import Logic_functions as lg

_months: List[int] = list(range(1, 13))


class TestLogicFunctions:
    def test_unique_preserves_order(self):
        xs = [1, 3, 2, 3, 6]
        unique_xs = lg.unique(xs)
        assert(unique_xs == [1,3,2,6])
