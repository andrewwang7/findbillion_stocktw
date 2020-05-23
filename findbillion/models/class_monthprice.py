import pandas as pd
import os

class class_monthprice:
    #"id","StockID","year","month","PriceHigh","PriceLow","PriceAvg","PriceOpen","PriceClose","PERatioAvg"

    def __init__(self, findbillion_database, ):
        self.df_monthprice = findbillion_database.df_monthprice

    def __get_value__(self, stockid, year, month, col_name):
        cond_stockid = self.df_monthprice['StockID'] == stockid
        cond_year = self.df_monthprice['year'] == year
        cond_month = self.df_monthprice['month'] == month
        df_sel = self.df_monthprice[cond_stockid & cond_year & cond_month]
        values_ = df_sel[col_name].values  # & cond_isConsolidating

        if (len(values_) > 0):
            return values_[0]
        else:
            return None

    #---------------------------------------------------------------
    def get_PriceHigh(self, stockid, year, month):
        return self.__get_value__(stockid, year, month, "PriceHigh")

    def get_PriceLow(self, stockid, year, month):
        return self.__get_value__(stockid, year, month, "PriceLow")

    def get_PriceAvg(self, stockid, year, month):
        return self.__get_value__(stockid, year, month, "PriceAvg")

    def getPriceOpen(self, stockid, year, month):
        return self.__get_value__(stockid, year, month, "PriceOpen")

    def getPriceClose(self, stockid, year, month):
        return self.__get_value__(stockid, year, month, "PriceClose")

    def getPERatioAvg(self, stockid, year, month):
        return self.__get_value__(stockid, year, month, "PERatioAvg")
