from . import dataset_path

import sys
import os
import pytest
sys.path.append('../../../../')
from findbillion.core.class_financial_ratio import class_financial_ratio
from findbillion.core.class_findbillion_database import class_findbillion_database

stockid = 2330
year = 2019
quarter = 1

findbillion_database = class_findbillion_database(dataset_path)
financial_ratio = class_financial_ratio(findbillion_database)
#-------------------------------------------------------------
class Test_class_financial_ratio():
    def test_get_net_income_ratio(self):
        net_income_ratio = financial_ratio.get_net_income_ratio(stockid, year, quarter)
        net_income_ratio_ans = 0.32

        assert net_income_ratio==pytest.approx(net_income_ratio_ans, abs=0.01)


    def test_get_eps_last_4q(self):
        eps_last_4q = financial_ratio.get_eps_last_4q(stockid, year, quarter)
        eps_last_4q_ans = 12.44

        assert eps_last_4q==pytest.approx(eps_last_4q_ans, abs=0.01)


    # TOOD: others

