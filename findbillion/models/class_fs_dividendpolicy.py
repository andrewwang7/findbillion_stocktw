import pandas as pd
import os

class class_fs_dividendpolicy:
    #"id", "StockID", "year", "Dividend_Cash", "Dividend_Stock"

    def __init__(self, findbillion_database, ):
        self.df_dividendpolicy = findbillion_database.df_dividendpolicy

    def __get_value__(self, stockid, year, col_name):
        cond_stockid = self.df_dividendpolicy['StockID'] == stockid
        cond_year = self.df_dividendpolicy['year'] == year
        df_sel = self.df_dividendpolicy[cond_stockid & cond_year]
        values_ = df_sel[col_name].values  # & cond_isConsolidating

        if (len(values_) > 0):
            return values_[0]
        else:
            return None

    #---------------------------------------------------------------
    def get_Dividend_Cash(self, stockid, year,):
        return self.__get_value__(stockid, year, "Dividend_Cash")


    def get_Dividend_Stock(self, stockid, year,):
        return self.__get_value__(stockid, year, "Dividend_Stock")



