import pandas as pd
import os


class class_fs_incomestatement:
    '''
    incomestatement
    "id","stockid","year","quarter","isConsolidating",
    "OperatingRevenues","OperatingCosts","GrossIncome",
    "OperatingExpenses","OperatingIncome",
    "NonOperatingIncome","NonOperatingExpenses",
    "NetIncomeBeforeTax","NetIncome","EPS"
    '''

    def __init__(self, findbillion_database):
        self.df_incomestatement = findbillion_database.df_incomestatement

    def __get_value__(self, stockid, year, quarter, col_name):
        cond_stockid = self.df_incomestatement['stockid'] == stockid
        cond_year = self.df_incomestatement['year'] == year
        cond_quarter = self.df_incomestatement['quarter'] == quarter
        df_sel = self.df_incomestatement[cond_stockid & cond_year & cond_quarter]
        df_sel = df_sel.sort_values(by=['isConsolidating'], ascending=False)
        values_ = df_sel[col_name].values

        if(len(values_)>0):
            return values_[0]
        else:
            return None

    #---------------------------------------------------------------
    def get_OperatingRevenues(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "OperatingRevenues")

    def get_OperatingCosts(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "OperatingCosts")

    def get_GrossIncome(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "GrossIncome")

    def get_OperatingExpenses(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "OperatingExpenses")

    def get_OperatingIncome(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "OperatingIncome")

    def get_NonOperatingIncome(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "NonOperatingIncome")

    def get_NonOperatingExpenses(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "NonOperatingExpenses")

    def get_NetIncomeBeforeTax(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "NetIncomeBeforeTax")

    def get_NetIncome(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "NetIncome")

    def get_EPS(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "EPS")