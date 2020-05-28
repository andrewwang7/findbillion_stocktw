import sys
import os
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


dataset_path = r'../../data'
save_path = r'../../~result'
num_cpu = 4
debug = 0

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


def processing_opetating_activities_ratio(stockid, year_stat):
    print(format(stockid) + '...')

    financial_ratio = class_financial_ratio(findbillion_database)
    opetating_activities_ratio = financial_ratio.get_opetating_activities_ratio(stockid, year_stat, 4, 2)
    if opetating_activities_ratio is not None and opetating_activities_ratio > 0.5:
        return stockid
    else:
        return None



def processing_est_cash_dividend_average(stockid, year_stat, year_est):
    print(format(stockid) + '...')

    fs_dividendpolicy = class_fs_dividendpolicy(findbillion_database)
    dividend_cash_true = fs_dividendpolicy.get_Dividend_Cash(stockid, year_est)

    est_yield = class_est_yield(findbillion_database)
    est_dividend_cash = est_yield.get_average_5y_cash_dividend(stockid, year_stat)

    if dividend_cash_true is not None and est_dividend_cash is not None:
        if dividend_cash_true==0:
            err_percentage = None
        else:
            err_percentage = (est_dividend_cash - dividend_cash_true)/dividend_cash_true * 100
    else:
        dividend_cash_true, est_dividend_cash, err_percentage = None, None, None

    return {stockid: dividend_cash_true}, {stockid: est_dividend_cash}, {stockid: err_percentage}


def processing_est_cash_dividend_average_dividend_payout_ratio(stockid, year_stat, year_est):
    print(format(stockid) + '...')

    fs_dividendpolicy = class_fs_dividendpolicy(findbillion_database)
    dividend_cash_true = fs_dividendpolicy.get_Dividend_Cash(stockid, year_est)

    est_eps = class_est_eps(findbillion_database)
    eps_est = est_eps.est_last_4q_eps_by_netincome_ratio(stockid, year_stat, 4)

    est_yield = class_est_yield(findbillion_database)
    est_dividend_cash = est_yield.est_cash_dividend_by_dividend_payout_ratio(stockid, year_stat, eps_est)

    if dividend_cash_true is not None and est_dividend_cash is not None:
        if dividend_cash_true==0:
            err_percentage = None
        else:
            err_percentage = (est_dividend_cash - dividend_cash_true) / dividend_cash_true * 100
    else:
        dividend_cash_true, est_dividend_cash, err_percentage = None, None, None\

    return {stockid: dividend_cash_true}, {stockid: est_dividend_cash}, {stockid: err_percentage}



def  processing_est_cash_dividend_by_netincome_ratio(stockid, year_stat, year_est):
    print(format(stockid) + '...')

    fs_dividendpolicy = class_fs_dividendpolicy(findbillion_database)
    dividend_cash_true = fs_dividendpolicy.get_Dividend_Cash(stockid, year_est)

    est_eps = class_est_eps(findbillion_database)
    eps_est_last_4q = est_eps.est_last_4q_eps_by_netincome_ratio(stockid, year_est, 4)

    est_yield = class_est_yield(findbillion_database)
    est_dividend_cash = est_yield.est_cash_dividend_by_linear_regression_5y(stockid, year_stat, eps_est_last_4q)

    if dividend_cash_true is not None and est_dividend_cash is not None:
        if dividend_cash_true==0:
            err_percentage = None
        else:
            err_percentage = (est_dividend_cash - dividend_cash_true)/dividend_cash_true * 100
    else:
        dividend_cash_true, est_dividend_cash, err_percentage = None, None, None

    return {stockid: dividend_cash_true}, {stockid: est_dividend_cash}, {stockid: err_percentage}



def main():
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # ------------------------------------------------
    stockinfo = class_stockinfo(findbillion_database)
    stock_all_list = stockinfo.get_stock_list()

    if debug == 1:
        stock_all_list = stock_all_list[:100]

    for (year_stat, year_est) in zip(year_stat_list, year_est_list):
        print('=======================================')
        print('Year: ' + format(year_est))

        print('search roe>15% ...')
        with Pool(num_cpu) as pool:
            stock_roe_15pa_list = pool.starmap(processing_roe_15pa, zip(stock_all_list, repeat(year_stat) ))

        stock_list = []
        for i_stock in stock_roe_15pa_list:
            if i_stock is not None:
                stock_list.append(i_stock)

        '''
        for i_stock in stock_all_list:
            financial_ratio = class_financial_ratio(findbillion_database)
            roe_avg = financial_ratio.get_ROE_avg(i_stock, year_stat, 4, 5)
            if roe_avg is not None and roe_avg > 0.15:
                stock_list.append(i_stock)
        '''

        # --------------------------------------------------
        # method 1
        print('--------------------------------')
        print('method 1')
        with Pool(num_cpu) as pool:
            est_cash_dividend_result = pool.starmap(processing_est_cash_dividend_average, zip(stock_list, repeat(year_stat), repeat(year_est)))

        # eps_true, eps_pred, err_percentage
        dict_to_csv(est_cash_dividend_result, 'est_cash_dividend_average_'+format(year_est)+'.csv', save_path=save_path)
        stat_dict(est_cash_dividend_result, 'est_cash_dividend_average_'+format(year_est), up_bound_pa=20, low_bound_pa=-20, save_path=save_path)
        # --------------------------------------------------
        # method 2
        print('--------------------------------')
        print('method 2')
        with Pool(num_cpu) as pool:
            est_cash_dividend_average_dividend_payout_ratio = pool.starmap(processing_est_cash_dividend_average_dividend_payout_ratio, zip(stock_list, repeat(year_stat), repeat(year_est)))

        dict_to_csv(est_cash_dividend_average_dividend_payout_ratio, 'est_cash_dividend_average_dividend_payout_ratio'+format(year_est)+'.csv', save_path=save_path)
        stat_dict(est_cash_dividend_average_dividend_payout_ratio, 'est_cash_dividend_average_dividend_payout_ratio_'+format(year_est), up_bound_pa=20, low_bound_pa=-20, save_path=save_path)

        # --------------------------------------------------
        # method 3
        print('--------------------------------')
        print('method 3')
        with Pool(num_cpu) as pool:
            est_cash_dividend_by_netincome_ratio = pool.starmap(processing_est_cash_dividend_by_netincome_ratio, zip(stock_list, repeat(year_stat), repeat(year_est)))

        dict_to_csv(est_cash_dividend_by_netincome_ratio, 'est_cash_dividend_by_netincome_ratio_'+format(year_est)+'.csv', save_path=save_path)
        stat_dict(est_cash_dividend_by_netincome_ratio, 'est_cash_dividend_by_netincome_ratio_'+format(year_est), up_bound_pa=20, low_bound_pa=-20, save_path=save_path)


        # --------------------------------------------------
        # method 4
        print('method 4')
        print('search free cash>0 ...')
        with Pool(num_cpu) as pool:
            stock_free_cash_list = pool.starmap(processing_free_cash_positive, zip(stock_list, repeat(year_stat) ))

        '''
        stock_free_cash_list = []
        for i_stock in stock_list:
            stock_free_cash_list.append(processing_free_cash_positive(i_stock, year_stat))
        '''
        '''
        stock_list = []
        for i_stock in stock_free_cash_list:
            if i_stock is not None:
                stock_list.append(i_stock)
        stock_free_cash_list = stock_list
        
        with Pool(num_cpu) as pool:
            est_cash_dividend_by_netincome_ratio = pool.starmap(processing_est_cash_dividend_by_netincome_ratio, zip(stock_free_cash_list, repeat(year_stat), repeat(year_est)))

        dict_to_csv(est_cash_dividend_by_netincome_ratio, 'est_cash_dividend_by_netincome_ratio_free_cashflow_'+format(year_est)+'.csv', save_path=save_path)
        stat_dict(est_cash_dividend_by_netincome_ratio, 'est_cash_dividend_by_netincome_ratio_free_cashflow_'+format(year_est), up_bound_pa=20, low_bound_pa=-20, save_path=save_path)
        '''

        # --------------------------------------------------
        # method 5
        print('method 5')
        print('search opetating activities ratio >0.5 ...')
        #with Pool(num_cpu) as pool:
        #    stock_free_cash_list = pool.starmap(processing_opetating_activities_ratio, zip(stock_list, repeat(year_stat) ))

        #'''
        stock_opetating_activities_ratio_list = []
        for i_stock in stock_list:
            stock_opetating_activities_ratio_list.append(processing_opetating_activities_ratio(i_stock, year_stat))
        #'''

        stock_list = []
        for i_stock in stock_opetating_activities_ratio_list:
            if i_stock is not None:
                stock_list.append(i_stock)
        stock_opetating_activities_ratio_list = stock_list

        with Pool(num_cpu) as pool:
            est_cash_dividend_by_netincome_ratio = pool.starmap(processing_est_cash_dividend_by_netincome_ratio, zip(stock_opetating_activities_ratio_list, repeat(year_stat), repeat(year_est)))

        dict_to_csv(est_cash_dividend_by_netincome_ratio, 'est_cash_dividend_opetating_activities_ratio_by_netincome_ratio_free_cashflow_'+format(year_est)+'.csv', save_path=save_path)
        stat_dict(est_cash_dividend_by_netincome_ratio, 'est_cash_dividend_opetating_activities_ratio_by_netincome_ratio_free_cashflow_'+format(year_est), up_bound_pa=20, low_bound_pa=-20, save_path=save_path)






if __name__ == '__main__':
    main()
