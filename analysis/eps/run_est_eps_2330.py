from tqdm import tqdm
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import json
from multiprocessing import Pool
from itertools import repeat
import sys
sys.path.append('../..')

from findbillion.core.class_findbillion_database import class_findbillion_database
from findbillion.core.class_financial_ratio import class_financial_ratio
from findbillion.core.class_est_eps import class_est_eps
from findbillion.models.class_stockinfo import class_stockinfo

dataset_path = r'D:\python\data_set\findbillion_csv\20200512'
num_cpu = 4
debug = 0

year_list = [2013, 2014, 2015, 2016, 2017, 2018, 2019]
quarter = 4
stockid = 2330

def main():
    findbillion_database = class_findbillion_database(dataset_path)

    for year in year_list:
        print('----------------------------')
        print(year)

        # eps ground truth
        financial_ratio = class_financial_ratio(findbillion_database)
        eps_true = financial_ratio.get_eps_last_4q(stockid, year, quarter)

        # estimated eps
        est_eps = class_est_eps(findbillion_database)
        eps_pred = est_eps.est_last_4q_eps_by_netincome_ratio(stockid, year, quarter)

        # error
        err_percentage = (eps_pred - eps_true)/eps_true * 100

        print("eps (true):       {:2.2f}".format(eps_true))
        print("eps (predict):    {:2.2f}".format(eps_pred))
        print("error of predict: {:2.2f}%".format(err_percentage))


if __name__ == '__main__':
    main()
