import sys
import os
import numpy as np
import json
from multiprocessing import Pool
from itertools import repeat
import math

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

sys.path.append('../..')
from analysis.analysis_utility import dict_to_csv, stat_dict, cal_retrun
from findbillion.core.class_findbillion_database import class_findbillion_database
from findbillion.core.class_financial_ratio import class_financial_ratio
from findbillion.core.class_est_eps import class_est_eps
from findbillion.core.class_est_yield import class_est_yield
from findbillion.models.class_fs_dividendpolicy import class_fs_dividendpolicy
from findbillion.models.class_stockinfo import class_stockinfo
from findbillion.models.class_monthprice import class_monthprice


dataset_path = r'../../data'
save_path = r'../../~result'
num_cpu = 4
debug = 0

#year_stat_list = [2012, 2013, 2014, 2015, 2016, 2017]  # 2012~2017
#year_est_list =  [2013, 2014, 2015, 2016, 2017, 2018]  # 2013~2018
#hold_year = 1

year_stat_list = [2016] #[2012, 2013, 2014, 2015, 2016, 2017]  # 2012~2017
year_est_list =  [2017] #[2013, 2014, 2015, 2016, 2017, 2018]  # 2013~2018
hold_year = 1
expect_return = 0.30
check_return = 0.20
yield_buyin = 0.0625

findbillion_database = class_findbillion_database(dataset_path)


np.random.seed(7)

def processing_roe_15pa(stockid, year_stat):
    print(format(stockid) + '...')

    financial_ratio = class_financial_ratio(findbillion_database)
    roe_avg = financial_ratio.get_ROE_avg(stockid, year_stat, 4, 5)
    if roe_avg is not None and roe_avg > 0.15:
        return stockid
    else:
        return None

def get_average_PERatio(stockid, year, month, year_stat_avg):
    monthprice = class_monthprice(findbillion_database)

    if stockid==1234:
        debug_tmp = 1

    check_year = year
    check_month = month
    per_avg = 0
    cnt_per = 0
    for idx_month in range(year_stat_avg*12):
        per_month = monthprice.getPERatioAvg(stockid, check_year, check_month)  # +1, est:2018 Q4 EPS, 2019/1 get revenues
        if per_month is not None:
            per_avg += per_month
            cnt_per += 1

        # next quarter
        check_month -= 1
        if (check_month <= 0):
            check_year -= 1
            check_month = 4

    if cnt_per>0:
        average_per = per_avg/cnt_per
    else:
        average_per = 0

    return average_per

def processing_free_cash_positive(stockid, year_stat):
    print(format(stockid) + '...')

    financial_ratio = class_financial_ratio(findbillion_database)
    free_cash_flow = financial_ratio.get_free_cash_flow(stockid, year_stat, 4, 2)
    if free_cash_flow is not None and free_cash_flow > 0:
        return stockid
    else:
        return None

def process_average_per(stockid, year_est, year_stat, hold_year, expect_return):
    fs_dividendpolicy = class_fs_dividendpolicy(findbillion_database)
    est_eps = class_est_eps(findbillion_database)
    monthprice = class_monthprice(findbillion_database)

    if stockid==1234:
        debug_tmp = 1

    PERatio = get_average_PERatio(stockid, year_est, 1, 3)

    eps_est_last_4q = est_eps.est_last_4q_eps_by_netincome_ratio(stockid, year_est, 4)
    if eps_est_last_4q is not None and PERatio is not None:
        price_target = eps_est_last_4q * PERatio
    else:
        price_target = 0

    price_buyin = monthprice.get_PriceHigh(stockid, year_est + 1, 1)

    if price_buyin is not None:
        price_target_buyin_diff = (price_target-price_buyin)/price_buyin
    else:
        price_target_buyin_diff = None

    if price_buyin is not None and price_target_buyin_diff is not None and price_target_buyin_diff>expect_return and PERatio<20:
        price_high_hold = get_high_price_hold(stockid, year_est + 1, 1, hold_year)
        price_target_high_diff = (price_high_hold - price_target)/price_target
        return_max = (price_high_hold-price_buyin)/price_buyin
    else:
        price_buyin = None
        price_high_hold = None
        price_target_high_diff = None
        return_max = None

    return {stockid: price_target}, \
           {stockid: PERatio}, \
           {stockid: price_buyin}, \
           {stockid: price_target_buyin_diff}, \
           {stockid: price_high_hold}, \
           {stockid: price_target_high_diff}, \
           {stockid: return_max}




def process_return_average_per_for_est_cash_dividend_by_netincome_ratio(stockid, year_est, year_stat, hold_year, expect_return, yield_buyin):
    #fs_dividendpolicy = class_fs_dividendpolicy(findbillion_database)
    est_eps = class_est_eps(findbillion_database)
    eps_est_last_4q = est_eps.est_last_4q_eps_by_netincome_ratio(stockid, year_est, 4)

    est_yield = class_est_yield(findbillion_database)
    est_dividend_cash = est_yield.est_cash_dividend_by_linear_regression_5y(stockid, year_stat, eps_est_last_4q)

    monthprice = class_monthprice(findbillion_database)
    price_buyin = monthprice.get_PriceHigh(stockid, year_est+1, 1)  # +1, estimate 2018 Q4 EPS, 2019/1 get revenues,
    if est_dividend_cash is not None and price_buyin is not None:
        est_dividend_cash_yield = est_dividend_cash/price_buyin
    else:
        est_dividend_cash_yield = None

    if stockid==1234:
        debug_tmp = 1

    PERatio = get_average_PERatio(stockid, year_est, 1, 3)

    eps_est_last_4q = est_eps.est_last_4q_eps_by_netincome_ratio(stockid, year_est, 4)
    if eps_est_last_4q is not None and PERatio is not None:
        price_target = eps_est_last_4q * PERatio
    else:
        price_target = 0

    price_buyin = monthprice.get_PriceHigh(stockid, year_est + 1, 1)

    if price_buyin is not None:
        price_target_buyin_diff = (price_target-price_buyin)/price_buyin
    else:
        price_target_buyin_diff = None

    if price_buyin is not None and price_target_buyin_diff is not None and price_target_buyin_diff>expect_return \
            and est_dividend_cash_yield is not None and est_dividend_cash_yield>yield_buyin:  # and PERatio<20
        price_high_hold = get_high_price_hold(stockid, year_est + 1, 1, hold_year)
        price_target_high_diff = (price_high_hold - price_target)/price_target
        return_max = (price_high_hold-price_buyin)/price_buyin
    else:
        price_buyin = None
        price_high_hold = None
        price_target_high_diff = None
        return_max = None

    return {stockid: price_target}, \
           {stockid: PERatio}, \
           {stockid: price_buyin}, \
           {stockid: price_target_buyin_diff}, \
           {stockid: price_high_hold}, \
           {stockid: price_target_high_diff}, \
           {stockid: return_max}




def get_high_price_hold(stockid, year_start, month_start, hold_year):
    price_high_record = 0
    year_check = year_start
    month_check = month_start
    monthprice = class_monthprice(findbillion_database)
    for i_month in range(hold_year*12):
        price_high = monthprice.get_PriceHigh(stockid, year_check, month_check)

        if price_high is not None and price_high > price_high_record:
            price_high_record = price_high

        # next month
        month_check += 1
        if month_check>12:
            year_check += 1
            month_check = 1

    return price_high_record

def dict_to_csv_per_return(dict_result, filename_csv, save_path=''):
    with open(os.path.join(save_path, filename_csv), 'w') as f:
        f.write('stock, expected_retrun, pe_ratio, price_buy, return_expected, price_max, diff_expected_high_price, return_max \n')
        for dict_result_ in dict_result:
            price_target, pe_ratio, price_buyin, price_target_buyin_diff, price_high_hold, price_target_high_diff, return_max = dict_result_
            key = list(price_target.keys())[0]
            if price_target[key] is not None and \
               price_buyin[key] is not None and \
               price_target_buyin_diff[key] is not None and \
               price_high_hold[key] is not None and \
               price_target_high_diff[key] is not None and\
               return_max[key] is not None :
                f.write("%s, %s, %s, %s, %s, %s, %s, %s, \n"%(key, price_target[key], pe_ratio[key], price_buyin[key],
                                                              price_target_buyin_diff[key],
                                                              price_high_hold[key], price_target_high_diff[key], return_max[key]))


def stat_dict_return(dict_result, filename_save, low_bound_pa, check_return, save_path=''):
    # dict to list
    list_price_target_high_diff = []
    list_return_max = []
    for dict_result_ in dict_result:
        price_target_high_diff = dict_result_[-2]
        return_max = dict_result_[-1]
        key = list(price_target_high_diff.keys())[0]
        if price_target_high_diff[key] is not None:
            list_price_target_high_diff.append(price_target_high_diff[key])
            list_return_max.append(return_max[key])


    np_meet_target_price = np.array(list_price_target_high_diff)
    np_meet_target_price_sel = np_meet_target_price[np_meet_target_price > low_bound_pa]
    if len(np_meet_target_price)>0:
        ratio_meet_target_price_pa = len(np_meet_target_price_sel)/len(np_meet_target_price) * 100
    else:
        ratio_meet_target_price_pa = None

    np_return = np.array(list_return_max)
    np_return_sel = np_return[np_return > check_return]
    if len(np_return)>0:
        ratio_return_pa = len(np_return_sel)/len(np_return) * 100
    else:
        ratio_return_pa = None


    print('The ratio of meet target price>{:2f}: {:6.4f}'.format(low_bound_pa, ratio_meet_target_price_pa))
    print('The ratio of meet return>{:2f}: {:6.4f}'.format(check_return, ratio_return_pa))
    dict_return = {'The ratio of target price>{:2f}'.format(low_bound_pa): ratio_meet_target_price_pa,
                   'The ratio of meet return>{:2f}'.format(check_return): ratio_return_pa }
    with open(os.path.join(save_path, filename_save+'.json'), 'w') as outfile:
        json.dump(dict_return, outfile)




def main():
    if not os.path.exists(save_path):
        os.makedirs(save_path)


    # ------------------------------------------------
    stockinfo = class_stockinfo(findbillion_database)
    stock_all_list = stockinfo.get_stock_list()

    if debug == 1:
        stock_all_list = stock_all_list[:300]

    for (year_stat, year_est) in zip(year_stat_list, year_est_list):
        print('=======================================')
        print('Year: ' + format(year_est))

        print('search roe>15% ...')
        with Pool(num_cpu) as pool:
            stock_roe_15pa_list = pool.starmap(processing_roe_15pa, zip(stock_all_list, repeat(year_stat)))

        stock_list = []
        for i_stock in stock_roe_15pa_list:
            if i_stock is not None:
                stock_list.append(i_stock)



        # --------------------------------------------------
        # method 1 average PER Expected return > 30%
        print('--------------------------------')
        print('method 1')

        return_average_per = []
        for i_stock in stock_list:
            return_average_per.append(process_average_per(i_stock, year_est, year_stat, hold_year, expect_return))


        dict_to_csv_per_return(return_average_per, 'return_average_per_' + format(year_est) + '.csv',
                                     save_path=save_path)

        stat_dict_return(return_average_per, 'return_average_per_' + format(year_est), low_bound_pa=-0.1, check_return=check_return, save_path=save_path)


        # --------------------------------------------------
        # method 2
        print('--------------------------------')
        print('method 2')

        print('search free cash>0 ...')
        with Pool(num_cpu) as pool:
            stock_free_cash_list = pool.starmap(processing_free_cash_positive , zip(stock_list, repeat(year_stat)))

        stock_list = []
        for i_stock in stock_free_cash_list:
            if i_stock is not None:
                stock_list.append(i_stock)
        stock_free_cash_list = stock_list

        return_average_per_free_cash = []
        for i_stock in stock_free_cash_list:
            return_average_per_free_cash.append(process_return_average_per_for_est_cash_dividend_by_netincome_ratio(i_stock, year_est, year_stat, hold_year, expect_return, yield_buyin))



        dict_to_csv_per_return(return_average_per_free_cash, 'return_average_per_free_cash_' + format(year_est) + '.csv',
                                     save_path=save_path)

        stat_dict_return(return_average_per_free_cash, 'return_average_per_free_cash_' + format(year_est), low_bound_pa=-0.1, check_return=check_return, save_path=save_path)



if __name__ == '__main__':
    main()

