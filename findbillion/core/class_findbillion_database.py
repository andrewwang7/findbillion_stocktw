import pandas as pd
import os

class class_findbillion_database:

    def __init__(self, dataset_path, ):
        filename_stockinfo = 'stockinfo.csv'
        self.filename_csv = os.path.join(dataset_path, filename_stockinfo)
        self.df_stockinfo = pd.read_csv(self.filename_csv)

        filename_revenuesmonth = 'revenuesmonth.csv'
        self.filename_csv = os.path.join(dataset_path, filename_revenuesmonth)
        self.df_revenuesmonth = pd.read_csv(self.filename_csv)

        filename_balancesheet = 'webfs_balancesheet.csv'
        self.filename_csv = os.path.join(dataset_path, filename_balancesheet)
        self.df_balancesheet = pd.read_csv(self.filename_csv)

        filename_cashflowstatement = 'webfs_cashflowstatement.csv'
        self.filename_csv = os.path.join(dataset_path, filename_cashflowstatement)
        self.df_cashflowstatement = pd.read_csv(self.filename_csv)

        filename_incomestatement = 'webfs_incomestatement.csv'
        self.filename_csv = os.path.join(dataset_path, filename_incomestatement)
        self.df_incomestatement = pd.read_csv(self.filename_csv)

        filename_monthprice = 'monthprice.csv'
        self.filename_csv = os.path.join(dataset_path, filename_monthprice)
        self.df_monthprice = pd.read_csv(self.filename_csv)

        filename_dividendpolicy = "webfs_dividendpolicy.csv"
        self.filename_csv = os.path.join(dataset_path, filename_dividendpolicy)
        self.df_dividendpolicy = pd.read_csv(self.filename_csv)


