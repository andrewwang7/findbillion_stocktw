import pandas as pd
import os


class class_fs_revenues_month:
    '''
    revenuesmonth:
    "id","stockid","year","isConsolidating",
    "month01accu","month02accu","month03accu",
    "month04accu","month05accu","month06accu",
    "month07accu","month08accu","month09accu",
    "month10accu","month11accu","month12accu",
    "month01single","month02single","month03single",
    "month04single","month05single","month06single",
    "month07single","month08single","month09single",
    "month10single","month11single","month12single"
    '''

    def __init__(self, findbillion_database):
        self.df_revenuesmonth = findbillion_database.df_revenuesmonth

    def __get_value__(self, stockid, year, col_name):
        cond_stockid = self.df_revenuesmonth['stockid'] == stockid
        cond_year = self.df_revenuesmonth['year'] == year

        df_sel = self.df_revenuesmonth[cond_stockid & cond_year]
        df_sel = df_sel.sort_values(by=['isConsolidating'], ascending=False)
        values_ = df_sel[col_name].values/1000  # /1000 for thousand to million


        if(len(values_)>0):
            return values_[0]
        else:
            return None

        return value

    #--------------------------------------------
    def get_revenue(self, stockid, year, month):
        col_name = "month%02dsingle" % month
        revenues_month = self.__get_value__(stockid, year, col_name)

        return revenues_month

    def get_revenue_accu(self, stockid, year, month):
        col_name = "month%02daccu" % month
        revenues_month_accu = self.__get_value__(stockid, year, col_name)

        return revenues_month_accu





