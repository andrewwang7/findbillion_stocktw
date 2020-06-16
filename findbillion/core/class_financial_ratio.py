import sys
import os
import math

sys.path.append('../..')
from findbillion.models.class_fs_revenues_month import class_fs_revenues_month
from findbillion.models.class_fs_balancesheet import class_fs_balancesheet
from findbillion.models.class_fs_cashflowstatement import class_fs_cashflowstatement
from findbillion.models.class_fs_incomestatement import class_fs_incomestatement


class class_financial_ratio:
    def __init__(self, findbillion_database):
        self.fs_revenues_month = class_fs_revenues_month(findbillion_database)
        self.fs_balancesheet = class_fs_balancesheet(findbillion_database)
        self.fs_cashflowstatement = class_fs_cashflowstatement(findbillion_database)
        self.fs_incomestatement = class_fs_incomestatement(findbillion_database)


    #=======================================================
    def get_net_income_ratio(self, stockid, year, quarter):
        check_year = year
        check_quarter = quarter
        cal_NetIncome_ratio = []
        for idx in range(4):
            revenues_quarter = self.fs_incomestatement.get_OperatingRevenues(stockid, check_year, check_quarter)
            netincome_quarter = self.fs_incomestatement.get_NetIncome(stockid, check_year, check_quarter)
            if netincome_quarter is not None and netincome_quarter is not None:
                if revenues_quarter>0 and not math.isnan(netincome_quarter) and not math.isnan(revenues_quarter):
                    cal_NetIncome_ratio.append(netincome_quarter/revenues_quarter)
            #else:
            #    raise ValueError('NetIncome is None')

            # next quarter
            check_quarter -= 1
            if(check_quarter<=0):
                check_year -= 1
                check_quarter = 4

        # NetIncome_ratio
        if len(cal_NetIncome_ratio)>0:
            NetIncome_ratio = sum(cal_NetIncome_ratio)/len(cal_NetIncome_ratio)
        else:
            NetIncome_ratio = None

        return NetIncome_ratio



    def get_eps_last_4q(self, stockid, year, quarter):
        check_year = year
        check_quarter = quarter

        net_income_last_4q = self.get_net_income_last_4q(stockid, year, quarter)
        eps_last_4q =  self.get_eps_from_net_income( stockid, check_year, check_quarter, net_income_last_4q)

        return eps_last_4q


    def get_net_income_last_4q(self, stockid, year, quarter):
        check_year = year
        check_quarter = quarter
        cal_NetIncome = 0.0
        for idx in range(4):
            if quarter == 4:
                cal_NetIncome = self.fs_incomestatement.get_NetIncome(stockid, check_year, 0)
            else:
                netincome_quarter = self.fs_incomestatement.get_NetIncome(stockid, check_year, check_quarter)
                if netincome_quarter is not None:
                    cal_NetIncome += netincome_quarter
                else:
                    raise ValueError('NetIncome is None')

                # next quarter
                check_quarter -= 1
                if (check_quarter <= 0):
                    check_year -= 1
                    check_quarter = 4

        return cal_NetIncome

    def get_eps_from_net_income(self, stockid, year, quarter, net_income):
        cal_CapitalStock = self.fs_balancesheet.get_CapitalStock(stockid, year, quarter)
        if cal_CapitalStock is not None and cal_CapitalStock>0:
            eps_cal = net_income / cal_CapitalStock * 10
        else:
            eps_cal = None

        return eps_cal


    def get_revenues_last_12month(self, stockid, year, month):
        if month==12:
            revenues_last_12month = self.fs_revenues_month.get_revenue_accu(stockid, year, 12)
            return revenues_last_12month
        else:
            revenues_last_12month_this_year = self.fs_revenues_month.get_revenue_accu(stockid, year, month)
            revenues_last_12month_last_year_end = self.fs_revenues_month.get_revenue_accu(stockid, year-1, 12)
            revenues_last_12month_last_year_begin = self.fs_revenues_month.get_revenue_accu(stockid, year-1, month+1)

            if  revenues_last_12month_this_year is not None and\
                revenues_last_12month_last_year_end  is not None and\
                revenues_last_12month_last_year_begin is not None:
                revenues_last_12month = revenues_last_12month_this_year + (revenues_last_12month_last_year_end-revenues_last_12month_last_year_begin)
                return revenues_last_12month
            else:
                return None

    def get_ROE(self, stockid, year, quarter):
        net_income_last_4q = self.get_net_income_last_4q(stockid, year, quarter)
        total_equity = self.fs_balancesheet.get_TotalEquity(stockid, year, quarter)

        if net_income_last_4q is not None and \
           total_equity  is not None:
            if total_equity>0:
                roe = net_income_last_4q/total_equity
            else:
                roe = None

            return roe
        else:
            return None

    def get_ROE_avg(self, stockid, year, quarter, avg_year):
        check_year = year
        roe_list = []
        for y_idx in range(avg_year):
            roe = self.get_ROE(stockid, check_year, quarter)
            if roe is not None:
                roe_list.append(roe)
            check_year -= 1

        if None in roe_list:
            return None
        else:
            if len(roe_list)>0:
                roe_avg = sum(roe_list)/len(roe_list)
            else:
                roe_avg = None

        return roe_avg


    def get_free_cash_flow(self, stockid, year, quarter, acc_year):
        check_year = year
        check_quarter = quarter
        cash_OperatingActivities = 0
        cash_InvestingActivities = 0
        for idx in range(acc_year * 4):
            cash_OperatingActivities__ = self.fs_cashflowstatement.get_OperatingActivities(stockid, check_year, check_quarter)
            cash_InvestingActivities__ = self.fs_cashflowstatement.get_InvestingActivities(stockid, check_year, check_quarter)

            if cash_OperatingActivities__ is not None or cash_InvestingActivities__ is not None:
                cash_OperatingActivities += cash_OperatingActivities__
                cash_InvestingActivities += cash_InvestingActivities__

            # next quarter
            check_quarter -= 1
            if (check_quarter <= 0):
                check_year -= 1
                check_quarter = 4

        free_cash_flow = cash_OperatingActivities + cash_InvestingActivities

        return free_cash_flow

    def get_opetating_activities_ratio(self, stockid, year, quarter, acc_year):
        check_year = year
        check_quarter = quarter
        cash_OperatingActivities = 0
        cash_NetIncomes = 0
        for idx in range(acc_year * 4):
            cash_OperatingActivities__ = self.fs_cashflowstatement.get_OperatingActivities(stockid, check_year, check_quarter)
            cash_NetIncomes__ = self.fs_cashflowstatement.get_NetIncomes(stockid, check_year, check_quarter)

            if cash_OperatingActivities__ is not None or cash_NetIncomes__ is not None:
                cash_OperatingActivities += cash_OperatingActivities__
                cash_NetIncomes += cash_NetIncomes__

            # next quarter
            check_quarter -= 1
            if (check_quarter <= 0):
                check_year -= 1
                check_quarter = 4

        if cash_NetIncomes>0:
            opetating_activities_ratio = cash_OperatingActivities/cash_NetIncomes
        else:
            opetating_activities_ratio = None

        return opetating_activities_ratio




