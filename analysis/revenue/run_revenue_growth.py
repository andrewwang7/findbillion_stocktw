# ref: https://towardsdatascience.com/polynomial-regression-bbe8b9d97491

import sys
import os
import numpy as np
import json
from multiprocessing import Pool
from itertools import repeat

import matplotlib
#matplotlib.use('Agg')


from findbillion.core.class_findbillion_database import class_findbillion_database
from findbillion.models.class_fs_revenues_month import class_fs_revenues_month
from findbillion.core.class_est_growth import class_est_growth


dataset_path = r'../../data'
findbillion_database = class_findbillion_database(dataset_path)

stockid = 2330
year_end = 2019
month_end = 12
check_year = 3

en_plot = 1


def main():
    year_start = year_end - check_year  # 2017/1~2019/12
    month_start = 12
    if month_start == 12:
        year_start += 1
        month_start = 1

    est_growth = class_est_growth(findbillion_database)
    RevenueRegress_YoYEst = est_growth.get_revenue_growth(stockid, year_start, month_start, year_end, month_end, en_plot)

    print('The revenue growth of 2330: {:6.4f}%'.format(RevenueRegress_YoYEst*100))



if __name__ == '__main__':
    main()
