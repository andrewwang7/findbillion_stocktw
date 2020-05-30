import sys
import os
import numpy as np
import json
from multiprocessing import Pool
from itertools import repeat

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

sys.path.append('../..')
from analysis.analysis_utility import dict_to_csv, stat_dict
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
debug =0

year_stat_list = [2012, 2013, 2014, 2015, 2016, 2017]  # 2012~2017
year_est_list =  [2013, 2014, 2015, 2016, 2017, 2018]  # 2013~2018


findbillion_database = class_findbillion_database(dataset_path)


def processing_roe_15pa(stockid, year_stat):
    print(format(stockid) + '...')

    financial_ratio = class_financial_ratio(findbillion_database)
    roe_avg = financial_ratio.get_ROE_avg(stockid, year_stat, 4, 5)
    if roe_avg is not None and roe_avg > 0.15:
        return stockid
    else:
        return None

def processing_free_cash_positive(stockid, year_stat):
    print(format(stockid) + '...')

    financial_ratio = class_financial_ratio(findbillion_database)
    free_cash_flow = financial_ratio.get_free_cash_flow(stockid, year_stat, 4, 2)
    if free_cash_flow is not None and free_cash_flow > 0:
        return stockid
    else:
        return None


def processing_return_for_average_5y_cash_dividend(stockid, year_stat, year_est, yield_buyin, hold_year):
    print(format(stockid) + '...')

    fs_dividendpolicy = class_fs_dividendpolicy(findbillion_database)
    dividend_cash_true = fs_dividendpolicy.get_Dividend_Cash(stockid, year_est)

    est_yield = class_est_yield(findbillion_database)
    est_dividend_cash = est_yield.get_average_5y_cash_dividend(stockid, year_stat)

    monthprice = class_monthprice(findbillion_database)
    price_buyin = monthprice.get_PriceHigh(stockid, year_est, 1)

    if est_dividend_cash is not None and price_buyin is not None:
        est_dividend_cash_yield = est_dividend_cash/price_buyin
    else:
        est_dividend_cash_yield = None

    if price_buyin is not None and est_dividend_cash_yield is not None and dividend_cash_true is not None \
            and est_dividend_cash_yield>yield_buyin:
        price_buyin_hold_1y = monthprice.get_PriceHigh(stockid, year_est+hold_year, 1)

        if price_buyin_hold_1y is not None:
            return_buyin = (price_buyin_hold_1y - price_buyin + dividend_cash_true)/price_buyin
        else:
            return_buyin = None
    else:
        price_buyin = None
        price_buyin_hold_1y = None
        return_buyin = None

    return {stockid: dividend_cash_true}, \
           {stockid: est_dividend_cash}, \
           {stockid: est_dividend_cash_yield}, \
           {stockid: price_buyin}, \
           {stockid: price_buyin_hold_1y}, \
           {stockid: return_buyin}



def processing_return_for_est_cash_dividend_by_netincome_ratio(stockid, year_stat, year_est, yield_buyin, hold_year):
    print(format(stockid) + '...')

    fs_dividendpolicy = class_fs_dividendpolicy(findbillion_database)
    dividend_cash_true = fs_dividendpolicy.get_Dividend_Cash(stockid, year_est)

    est_eps = class_est_eps(findbillion_database)
    eps_est_last_4q = est_eps.est_last_4q_eps_by_netincome_ratio(stockid, year_est, 4)

    est_yield = class_est_yield(findbillion_database)
    est_dividend_cash = est_yield.est_cash_dividend_by_linear_regression_5y(stockid, year_stat, eps_est_last_4q)

    monthprice = class_monthprice(findbillion_database)
    price_buyin = monthprice.get_PriceHigh(stockid, year_est, 1)
    if est_dividend_cash is not None and price_buyin is not None:
        est_dividend_cash_yield = est_dividend_cash/price_buyin
    else:
        est_dividend_cash_yield = None

    if price_buyin is not None and est_dividend_cash_yield is not None and est_dividend_cash_yield>yield_buyin:
        price_buyin_hold_1y = monthprice.get_PriceHigh(stockid, year_est+hold_year, 1)
        if price_buyin_hold_1y is not None:
            return_buyin = (price_buyin_hold_1y - price_buyin + dividend_cash_true)/price_buyin
        else:
            return_buyin = None
    else:
        price_buyin = None
        price_buyin_hold_1y = None
        return_buyin = None

    return {stockid: dividend_cash_true}, \
           {stockid: est_dividend_cash}, \
           {stockid: est_dividend_cash_yield}, \
           {stockid: price_buyin}, \
           {stockid: price_buyin_hold_1y}, \
           {stockid: return_buyin}





def dict_to_csv_yeild_return(dict_result, filename_csv, save_path=''):
    with open(os.path.join(save_path, filename_csv), 'w') as f:
        f.write('stock, dividend_cash_true, dividend_cash_pred, yield_pred, price_buy, price_hold, return \n')
        for dict_result_ in dict_result:
            dividend_cash_true, est_dividend_cash, est_dividend_cash_yield, price_buyin, price_buyin_hold_1y, return_buyin = dict_result_
            key = list(dividend_cash_true.keys())[0]
            if dividend_cash_true[key] is not None and \
                    est_dividend_cash[key] is not None and \
                est_dividend_cash_yield[key] is not None and \
                price_buyin[key] is not None and \
                price_buyin_hold_1y[key] is not None and \
                return_buyin[key] is not None:
                f.write("%s, %s, %s, %s, %s, %s, %s\n"%(key, dividend_cash_true[key], est_dividend_cash[key], est_dividend_cash_yield[key],
                                                             price_buyin[key], price_buyin_hold_1y[key], return_buyin[key],))


def bootstrap(data, num_samples, alpha):
    n = len(data)
    if type(data) is list:
        data = np.array(data)

    idx = np.random.randint(0, n, size=(num_samples, n))
    samples = data[idx]
    stat = np.sort(np.mean(samples, 1))
    mean_return = np.mean(stat)
    ci_low_return = stat[int((alpha/2)*num_samples)]
    ci_high_return = stat[int((1-alpha/2)*num_samples)]
    return mean_return, ci_low_return, ci_high_return



def stat_dict_return(dict_result, filename_save, low_bound_pa, save_path=''):
    # dict to list
    list_return = []
    for dict_result_ in dict_result:
        return_check = dict_result_[-1]
        key = list(return_check.keys())[0]
        if return_check[key] is not None:
            list_return.append(return_check[key])

    # stat
    mean_return, ci_low_return, ci_high_return  = bootstrap(list_return, 5, 0.05)

    # the ratio between +- 10%
    np_return = np.array(list_return)
    np_return_sel = np_return[np_return > low_bound_pa]
    if len(np_return)>0:
        ratio_return_pa = len(np_return_sel)/len(np_return) * 100
    else:
        ratio_return_pa = None

    print('mean of return with selecting 5 stock: {:6.4f}'.format(mean_return))
    print('95% confidience interval of return with selecting 5 stock: {:6.4f}~{:6.4f}'.format(ci_low_return,ci_high_return ))
    print('The ratio of return>{:2f}: {:6.4f}'.format(low_bound_pa, ratio_return_pa))
    dict_return = {'mean of return with selecting 5 stock': mean_return,
                   '95% confidience interval of return with selecting 5 stock': (ci_low_return, ci_high_return),
                   'The ratio of return>{:2f}'.format(low_bound_pa): ratio_return_pa}
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
        # method 1
        # yield_buyin > 0.05 and hold_year = 1
        yield_buyin = 0.05
        hold_year = 1
        print('--------------------------------')
        print('method 1')
        #'''
        with Pool(num_cpu) as pool:
            return_1y_for_average_5y_cash_dividend = pool.starmap(processing_return_for_average_5y_cash_dividend,
                                                      zip(stock_list, repeat(year_stat), repeat(year_est), repeat(yield_buyin), repeat(hold_year)))
        #'''
        '''
        return_1y_for_yield_result = []
        for i_stock in stock_list:
            return_1y_for_yield_result.append(processing_return_for_average_5y_cash_dividend(i_stock, year_stat, year_est, yield_buyin, hold_year))
        '''
        dict_to_csv_yeild_return(return_1y_for_average_5y_cash_dividend, 'return_1y_for_average_5y_cash_dividend_' + format(year_est) + '.csv',
                    save_path=save_path)
        stat_dict_return(return_1y_for_average_5y_cash_dividend, 'return_1y_for_average_5y_cash_dividend_' + format(year_est),
                  low_bound_pa=yield_buyin, save_path=save_path)

        # --------------------------------------------------
        # method 4
        # yield_buyin > 0.05 and hold_year = 1
        yield_buyin = 0.05
        hold_year = 1
        print('--------------------------------')
        print('method 4')

        print('search free cash>0 ...')
        with Pool(num_cpu) as pool:
            stock_free_cash_list = pool.starmap(processing_free_cash_positive , zip(stock_list, repeat(year_stat)))

        stock_list = []
        for i_stock in stock_free_cash_list:
            if i_stock is not None:
                stock_list.append(i_stock)
        stock_free_cash_list = stock_list

        #'''
        with Pool(num_cpu) as pool:
            return_1y_for_est_cash_dividend_by_netincome_ratio_result = pool.starmap(processing_return_for_est_cash_dividend_by_netincome_ratio, zip(stock_free_cash_list, repeat(year_stat), repeat(year_est), repeat(yield_buyin), repeat(hold_year)))
        #'''
        '''
        return_1y_for_est_cash_dividend_by_netincome_ratio_result = []
        for i_stock in stock_list:
            return_1y_for_est_cash_dividend_by_netincome_ratio_result.append(processing_return_for_est_cash_dividend_by_netincome_ratio(i_stock, year_stat, year_est, yield_buyin, hold_year))
        '''


        dict_to_csv_yeild_return(return_1y_for_est_cash_dividend_by_netincome_ratio_result, 'return_1y_for_est_cash_dividend_by_netincome_ratio_' + format(year_est) + '.csv',
                    save_path=save_path)
        stat_dict_return(return_1y_for_est_cash_dividend_by_netincome_ratio_result, 'return_1y_for_est_cash_dividend_by_netincome_ratio_' + format(year_est),
                  low_bound_pa=yield_buyin, save_path=save_path)




if __name__ == '__main__':
    main()
