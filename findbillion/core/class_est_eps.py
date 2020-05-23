
from findbillion.core.class_financial_ratio import class_financial_ratio

class class_est_eps:
    def __init__(self, findbillion_database):
        self.financial_ratio = class_financial_ratio(findbillion_database)

    def est_last_4q_eps_by_netincome_ratio(self, stockid, year_est, quarter_est):
        # Net income ratio
        year_stat = year_est
        quarter_stat = quarter_est - 1
        if quarter_stat==0:
            year_stat -= 1
            quarter_stat = 4
        net_income_ratio = self.financial_ratio.get_net_income_ratio(stockid, year_stat, quarter_stat)

        # Last 12 month revenues
        month_est = int(3*quarter_est)
        revenues_last_12month = self.financial_ratio.get_revenues_last_12month(stockid, year_est, month_est)

        # Estimate EPS
        if revenues_last_12month is not None and net_income_ratio is not None:
            net_income = revenues_last_12month * net_income_ratio
            eps_est = self.financial_ratio.get_eps_from_net_income(stockid, year_stat, quarter_stat, net_income)

            return eps_est
        else:
            return None

    '''
    def est_last_4q_regrssion(self, year, quarter):
        pass
    '''