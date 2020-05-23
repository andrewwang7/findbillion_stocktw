from . import dataset_path

import sys
import os
sys.path.append('../../')
from findbillion.models.class_fs_balancesheet import class_fs_balancesheet
from findbillion.core.class_findbillion_database import class_findbillion_database

#-------------------------------------------------------------

stockid = 2330
year = 2019
quarter = 1

findbillion_database = class_findbillion_database(dataset_path)
fs_balancesheet = class_fs_balancesheet(findbillion_database)

#-------------------------------------------------------------
class Test_class_fs_balancesheet():

    def test_get_TotalEquity(self):
        TotalEquity = fs_balancesheet.get_TotalEquity(stockid, year, quarter)
        TotalEquity_ans = 1743518

        assert TotalEquity==TotalEquity_ans

    # TOOD: others
