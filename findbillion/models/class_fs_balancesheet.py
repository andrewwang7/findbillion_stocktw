import pandas as pd
import os

class class_fs_balancesheet:
    '''
      balancesheet:
      "id","stockid","year","quarter","isConsolidating",
      "CapitalStock","AccountsReceivable","Inventories","PrepaidExpenses","CurrentAssets","TotalAssets",
      "AccruedExpenses","AccountsPayable","CurrentLiabilities","TotalLiabilities",
      "TotalEquity"
      '''

    def __init__(self, findbillion_database, ):
        self.df_balancesheet = findbillion_database.df_balancesheet


    def __get_value__(self, stockid, year, quarter, col_name):
        cond_stockid = self.df_balancesheet['stockid'] == stockid
        cond_year = self.df_balancesheet['year'] == year
        cond_quarter = self.df_balancesheet['quarter'] == quarter
        df_sel = self.df_balancesheet[cond_stockid & cond_year & cond_quarter]
        df_sel = df_sel.sort_values(by=['isConsolidating'], ascending=False)
        values_ = df_sel[col_name].values  #  & cond_isConsolidating

        if(len(values_)>0):
            return values_[0]
        else:
            return None

    #---------------------------------------------------------------
    def get_CapitalStock(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "CapitalStock")

    def get_AccountsReceivable(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "AccountsReceivable")

    def get_Inventories(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "Inventories")

    def get_PrepaidExpenses(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "PrepaidExpenses")

    def get_CurrentAssets(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "CurrentAssets")

    def get_TotalAssets(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "TotalAssets")

    def get_AccruedExpenses(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "AccruedExpenses")

    def get_AccountsPayable(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "AccountsPayable")

    def get_CurrentLiabilities(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "CurrentLiabilities")

    def get_TotalLiabilities(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "TotalLiabilities")

    def get_TotalEquity(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "TotalEquity")
