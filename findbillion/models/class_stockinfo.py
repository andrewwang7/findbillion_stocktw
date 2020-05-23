import pandas as pd
import os

class class_stockinfo:
    #"id","StockID","year","month","PriceHigh","PriceLow","PriceAvg","PriceOpen","PriceClose","PERatioAvg"

    def __init__(self, findbillion_database, ):
        self.df_stockinfo = findbillion_database.df_stockinfo

    def get_stock_list(self):
        stock_list = self.df_stockinfo['StockID'].values

        return stock_list
