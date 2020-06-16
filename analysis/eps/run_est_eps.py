from tqdm import tqdm

import numpy as np
import os
#import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import json
from multiprocessing import Pool
from itertools import repeat
import sys
sys.path.append('../..')

from findbillion.core.class_findbillion_database import class_findbillion_database
from findbillion.core.class_financial_ratio import class_financial_ratio
from findbillion.core.class_est_eps import class_est_eps
from findbillion.models.class_stockinfo import class_stockinfo
from analysis.analysis_utility import dict_to_csv, stat_dict

dataset_path = r'../../data'
save_path = r'../../~result'
num_cpu = 4
debug = 0

year_est_list = [2013, 2014, 2015, 2016, 2017, 2018, 2019]  #[2018]  # [2013, 2014, 2015, 2016, 2017, 2018]


findbillion_database = class_findbillion_database(dataset_path)

def func_est_eps(stockid, year_est):
    quarter_est = 4

    # ground true
    financial_ratio = class_financial_ratio(findbillion_database)
    eps_true = financial_ratio.get_eps_last_4q(stockid, year_est, quarter_est)

    # estimate
    est_eps = class_est_eps(findbillion_database)
    eps_pred = est_eps.est_last_4q_eps_by_netincome_ratio(stockid, year_est, quarter_est)

    # error
    if eps_true is None or eps_pred is None:
        err_percentage = None
    elif eps_true != 0:
        err_percentage = (eps_pred - eps_true)/eps_true * 100
    else:
        err_percentage = None  #(eps_pred - 0.001) / 0.001 * 100

    return eps_true, eps_pred, err_percentage


def processing_est_eps(stockid, year_est):
    print(format(stockid) + '...')
    year_stat = year_est - 1
    quarter_est = 4
    financial_ratio = class_financial_ratio(findbillion_database)
    roe_avg = financial_ratio.get_ROE_avg(stockid, year_stat, quarter_est, 5)
    if roe_avg is not None:
        eps_true, eps_pred, err_percentage = func_est_eps(stockid, year_est)
    else:
        eps_true, eps_pred, err_percentage = None, None, None

    return {stockid: eps_true}, {stockid: eps_pred}, {stockid: err_percentage}


def processing_est_eps_roe15(stockid, year_est):
    print(format(stockid) + '...')
    year_stat = year_est - 1
    quarter_est = 4
    financial_ratio = class_financial_ratio(findbillion_database)
    roe_avg = financial_ratio.get_ROE_avg(stockid, year_stat, quarter_est, 5)
    if roe_avg is not None and roe_avg > 0.15:
        eps_true, eps_pred, err_percentage = func_est_eps(stockid, year_est)
    else:
        eps_true, eps_pred, err_percentage = None, None, None

    return {stockid: eps_true}, {stockid: eps_pred}, {stockid: err_percentage}


def main():
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    #------------------------------------------------
    # list all stock
    stockinfo = class_stockinfo(findbillion_database)
    stock_list = stockinfo.get_stock_list()

    if debug == 1:
        stock_list = stock_list[:30]


    '''
    # For Debug
    for i_stock in stock_list:
        eps_true, eps_pred, err_percentage = processing_est_eps(i_stock, year)
        break_pt = 1
    '''

    #============================================
    for year_est in year_est_list:
        print('=======================================')
        print('Year: ' + format(year_est))
        #--------------------------------------------------
        # method 1: estimate all stock
        print('--------------------------------')
        print('method 1')
        with Pool(num_cpu) as pool:
            est_eps_result =pool.starmap(processing_est_eps, zip(stock_list, repeat(year_est)))

        #eps_true, eps_pred, err_percentage
        dict_to_csv(est_eps_result, 'est_eps_'+format(year_est)+'.csv', save_path=save_path)
        stat_dict(est_eps_result, 'est_eps_'+format(year_est), up_bound_pa=10, low_bound_pa=-10, save_path=save_path)


        # --------------------------------------------------
        # method 2: estimate the ROE>15% stock
        print('--------------------------------')
        print('method 2')
        with Pool(num_cpu) as pool:
            est_eps_result =pool.starmap(processing_est_eps_roe15, zip(stock_list, repeat(year_est)))

        dict_to_csv(est_eps_result, 'est_eps_roe15_'+format(year_est)+'.csv', save_path=save_path)
        stat_dict(est_eps_result, 'est_eps_roe15_'+format(year_est), up_bound_pa=10, low_bound_pa=-10, save_path=save_path)




if __name__ == '__main__':
    main()
