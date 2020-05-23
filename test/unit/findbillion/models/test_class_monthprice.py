from . import dataset_path

import sys
import os
sys.path.append('../../')
from findbillion.models.class_monthprice import class_monthprice
from findbillion.core.class_findbillion_database import class_findbillion_database

#-------------------------------------------------------------
stockid = 2330
year = 2018
month = 5

findbillion_database = class_findbillion_database(dataset_path)
monthprice = class_monthprice(findbillion_database)

#-------------------------------------------------------------
class Test_class_fs_revenures_month():

    def test_get_PriceAvg(self):
        PriceAvg = monthprice.get_PriceAvg(stockid, year, month)
        PriceAvg_ans = 227.05

        assert PriceAvg==PriceAvg_ans

    # TOOD: others

