from . import dataset_path

import sys
import os
sys.path.append('../../')
from findbillion.models.class_fs_dividendpolicy import class_fs_dividendpolicy
from findbillion.core.class_findbillion_database import class_findbillion_database

#-------------------------------------------------------------
stockid = 2330
year = 2018

findbillion_database = class_findbillion_database(dataset_path)
fs_dividendpolicy = class_fs_dividendpolicy(findbillion_database)

#-------------------------------------------------------------
class Test_class_fs_revenures_month():

    def test_get_Dividend_Cash(self):
        Dividend_Cash = fs_dividendpolicy.get_Dividend_Cash(stockid, year)
        Dividend_Cash_ans = 8

        assert Dividend_Cash==Dividend_Cash_ans

    # TOOD: others

