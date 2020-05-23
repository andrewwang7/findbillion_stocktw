import sys

sys.path.append('../..')
from findbillion.core.class_financial_ratio import class_financial_ratio
from findbillion.core.class_est_yield import class_est_yield
from findbillion.core.class_est_eps import class_est_eps
from findbillion.core.class_findbillion_database import class_findbillion_database
from findbillion.models.class_fs_dividendpolicy import class_fs_dividendpolicy

dataset_path = r'D:\python\data_set\findbillion_csv\20200512'


def main():
    stockid = 2330
    year_est = 2018
    year_stat = 2017

    findbillion_database = class_findbillion_database(dataset_path)
    est_eps = class_est_eps(findbillion_database)
    est_yield = class_est_yield(findbillion_database)
    fs_dividendpolicy = class_fs_dividendpolicy(findbillion_database)
    dividend_cash = fs_dividendpolicy.get_Dividend_Cash(stockid, year_est)

    #-----------------------------------------
    # methed 1: average cash dividend
    dividend_cash_avg = est_yield.get_average_5y_cash_dividend(stockid, year_stat)

    error_method1 = (dividend_cash_avg - dividend_cash)/dividend_cash * 100

    print("Average cash dividend: ")
    print("cash dividend (true):       {:2.2f}".format(dividend_cash))
    print("cash dividend (predict):    {:2.2f}".format(dividend_cash_avg))
    print("error of predict: {:2.2f}%".format(error_method1))


    #--------------------------------------------------
    # methed 2: average dividend payout ratio
    print("----------------------------------------")
    eps_est_last4q = est_eps.est_last_4q_eps_by_netincome_ratio(stockid, year_est, 4)
    est_dividend_cash = est_yield.est_cash_dividend_by_dividend_payout_ratio(stockid, year_stat, eps_est_last4q)

    error_method2 = (est_dividend_cash - dividend_cash)/dividend_cash * 100

    print("Average cash dividend payout ratio: ")
    print("cash dividend (true):       {:2.2f}".format(dividend_cash))
    print("cash dividend (predict):    {:2.2f}".format(est_dividend_cash))
    print("error of predict: {:2.2f}%".format(error_method2))


    #--------------------------------------------------
    # methed 3: estimate dividend payout ratio by linear regression
    print("----------------------------------------")
    eps_est = est_eps.est_last_4q_eps_by_netincome_ratio(stockid, year_est, 4)
    est_dividend_cash = est_yield.est_cash_dividend_by_linear_regression_5y(stockid, year_stat, eps_est)

    error_method3 = (est_dividend_cash - dividend_cash)/dividend_cash * 100

    print("Estimate cash dividend payout ratio by linear regression: ")
    print("cash dividend (true):       {:2.2f}".format(dividend_cash))
    print("cash dividend (predict):    {:2.2f}".format(est_dividend_cash))
    print("error of predict: {:2.2f}%".format(error_method3))


if __name__ == '__main__':
    main()
