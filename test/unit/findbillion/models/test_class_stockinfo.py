from . import dataset_path

import sys
import os
sys.path.append('../../')
from findbillion.models.class_stockinfo import class_stockinfo
from findbillion.core.class_findbillion_database import class_findbillion_database


#-------------------------------------------------------------
findbillion_database = class_findbillion_database(dataset_path)
stockinfo = class_stockinfo(findbillion_database)

#-------------------------------------------------------------
class Test_class_fs_revenures_month():

    def test_get_PriceAvg(self):
        stock_list = stockinfo.get_stock_list()

        assert len(stock_list)>1000

    # TOOD: others
