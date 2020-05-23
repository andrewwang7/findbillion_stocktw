from . import dataset_path

import sys
import os
sys.path.append('../../')
from findbillion.models.class_fs_revenues_month import class_fs_revenues_month
from findbillion.core.class_findbillion_database import class_findbillion_database

#-------------------------------------------------------------
stockid = 2330
year = 2019
month = 1

findbillion_database = class_findbillion_database(dataset_path)
fs_revenues_month = class_fs_revenues_month(findbillion_database)

#-------------------------------------------------------------
class Test_class_fs_revenures_month():

    def test_get_revenue(self):
        revenue = fs_revenues_month.get_revenue(stockid, year, month)
        revenue_ans = 78093.827

        assert revenue==revenue_ans

    # TOOD: others

