import pandas as pd
import os
from findbillion.core.class_findbillion_database import class_findbillion_database


class class_fs_cashflowstatement:
    '''
    cashflowstatement
    "id","stockid","year","quarter","isConsolidating",
    "NetIncome","OperatingActivities","InvestingActivities","FinancingActivities","FinancingActivities_Dividend"
    '''

    def __init__(self, findbillion_database, ):
        self.df_cashflowstatement = findbillion_database.df_cashflowstatement


    def __get_value__(self, stockid, year, quarter, col_name):
        cond_stockid = self.df_cashflowstatement['stockid'] == stockid
        cond_year = self.df_cashflowstatement['year'] == year
        cond_quarter = self.df_cashflowstatement['quarter'] == quarter

        df_sel = self.df_cashflowstatement[cond_stockid & cond_year & cond_quarter]
        df_sel = df_sel.sort_values(by=['isConsolidating'], ascending=False)
        values_ = df_sel[col_name].values

        if(len(values_)>0):
            return values_[0]
        else:
            return None

        return value


    #--------------------------------------------
    def get_NetIncomes(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "NetIncome")

    def get_OperatingActivities(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "OperatingActivities")

    def get_InvestingActivities(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "InvestingActivities")

    def get_FinancingActivities(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "FinancingActivities")

    def get_FinancingActivities_Dividend(self, stockid, year, quarter):
        return self.__get_value__(stockid, year, quarter, "FinancingActivities_Dividend")

