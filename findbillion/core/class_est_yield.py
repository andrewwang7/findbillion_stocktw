import sys
from sklearn.linear_model import LinearRegression
import numpy as np

sys.path.append('../..')
from findbillion.core.class_financial_ratio import class_financial_ratio
from findbillion.models.class_fs_dividendpolicy import class_fs_dividendpolicy

class class_est_yield:
    def __init__(self, findbillion_database):
        self.fs_dividendpolicy = class_fs_dividendpolicy(findbillion_database)
        self.financial_ratio = class_financial_ratio(findbillion_database)

    def get_average_5y_cash_dividend(self, stockid, year_stat):

        dividend_cash_5y = []
        check_year = year_stat
        for idx in range(5):
            dividend_cash = self.fs_dividendpolicy.get_Dividend_Cash(stockid, check_year)
            if dividend_cash is not None:
                dividend_cash_5y.append(dividend_cash)
            check_year -= 1

        if len(dividend_cash_5y)>0:
            dividend_cash_average = sum(dividend_cash_5y)/len(dividend_cash_5y)
        else:
            dividend_cash_average = 0

        return dividend_cash_average


    def get_average_5y_cash_dividend_payout_ratio(self, stockid, year_stat):
        dividend_payout_ratio_5y = []
        check_year = year_stat
        for idx in range(5):
            eps_last_4q = self.financial_ratio.get_eps_last_4q(stockid, check_year, 4)
            dividend_cash = self.fs_dividendpolicy.get_Dividend_Cash(stockid, check_year)
            if dividend_cash is not None and eps_last_4q is not None:
                if eps_last_4q==0:
                    dividend_payout_ratio_5y.append(0)
                else:
                    dividend_payout_ratio_5y.append(dividend_cash/eps_last_4q)
            check_year -= 1

        if len(dividend_payout_ratio_5y)>0:
            dividend_payout_ratio = sum(dividend_payout_ratio_5y)/len(dividend_payout_ratio_5y)
        else:
            dividend_payout_ratio = 0

        return dividend_payout_ratio


    def est_cash_dividend_by_dividend_payout_ratio(self, stockid, year_stat, eps):
        cash_dividend_payout_ratio = self.get_average_5y_cash_dividend_payout_ratio(stockid, year_stat-1)

        if eps is not None and cash_dividend_payout_ratio is not None:
            if eps<0 or cash_dividend_payout_ratio<0:
                est_cash_dividend = 0
            else:
                est_cash_dividend = eps * cash_dividend_payout_ratio
        else:
            est_cash_dividend = None

        return est_cash_dividend


    def est_cash_dividend_by_linear_regression_5y(self, stockid, year_stat, eps):
        eps_5y = []
        dividend_payout_ratio_5y = []
        check_year = year_stat
        for idx in range(5):
            eps_last_4q = self.financial_ratio.get_eps_last_4q(stockid, check_year, 4)
            dividend_cash = self.fs_dividendpolicy.get_Dividend_Cash(stockid, check_year)
            if dividend_cash is not None and eps_last_4q is not None and not np.isnan(dividend_cash) and not np.isnan(eps_last_4q):
                dividend_payout_ratio_5y.append(dividend_cash / eps_last_4q)
                eps_5y.append([eps_last_4q])
            check_year -= 1

        if len(dividend_payout_ratio_5y)>0 and len(eps_5y)>0:
            try:
                regr = LinearRegression()
                regr.fit( np.array(eps_5y), np.array(dividend_payout_ratio_5y))
                dividend_payout_ratio_est = regr.predict([[eps]])[0]

                if eps<0 or dividend_payout_ratio_est<0:
                    est_cash_dividend = 0
                else:
                    est_cash_dividend = eps * dividend_payout_ratio_est
            except:
                est_cash_dividend = None
        else:
            est_cash_dividend = None

        return est_cash_dividend




