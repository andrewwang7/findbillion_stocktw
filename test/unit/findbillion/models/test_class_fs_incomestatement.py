from . import dataset_path

import sys
import os
sys.path.append('../../')
from findbillion.models.class_fs_incomestatement import class_fs_incomestatement
from findbillion.core.class_findbillion_database import class_findbillion_database

#-------------------------------------------------------------
stockid = 2330
year = 2019
quarter = 1

findbillion_database = class_findbillion_database(dataset_path)
fs_incomestatement = class_fs_incomestatement(findbillion_database)

#-------------------------------------------------------------
class Test_class_fs_incomestatement():

    def test_get_EPS(self):
        eps = fs_incomestatement.get_EPS(stockid, year, quarter)
        eps_ans = 2.37

        assert eps==eps_ans

    # TOOD: others
