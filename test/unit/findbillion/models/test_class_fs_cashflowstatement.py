from . import dataset_path

import sys
import os
sys.path.append('../../../../')
from findbillion.models.class_fs_cashflowstatement import class_fs_cashflowstatement
from findbillion.core.class_findbillion_database import class_findbillion_database

#-------------------------------------------------------------
stockid = 2330
year = 2019
quarter = 1

findbillion_database = class_findbillion_database(dataset_path)
fs_cashflowstatement = class_fs_cashflowstatement(findbillion_database)

#-------------------------------------------------------------
class Test_class_fs_cashflowstatement():

    def test_get_OperatingActivities(self):
        OperatingActivities = fs_cashflowstatement.get_OperatingActivities(stockid, year, quarter)
        OperatingActivities_ans = 152670

        assert OperatingActivities==OperatingActivities_ans

    # TOOD: others
