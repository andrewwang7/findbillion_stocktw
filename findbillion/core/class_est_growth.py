import sys
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import math

sys.path.append('../..')
from findbillion.models.class_fs_revenues_month import class_fs_revenues_month


class class_est_growth:
    def __init__(self, findbillion_database):
        self.fs_revenues_month = class_fs_revenues_month(findbillion_database)


    def __get_month_revenues_list(self, stockid, year_start, month_start, year_end, month_end):

        year_check = year_start
        month_check = month_start
        revenues_list = []

        if year_end<year_start:
            return None
        if year_end==year_start and month_end<month_start:
            return None

        while year_check<year_end or (year_check==year_end and month_check<=month_end):
            revenues_month = self.fs_revenues_month.get_revenue(stockid, year_check, month_check)

            if revenues_month is not None and not math.isnan(revenues_month)   :
                revenues_list.append(revenues_month)

            month_check += 1
            if month_check>12:
                year_check += 1
                month_check = 1

        return revenues_list



    def __cal_second_order_regression(self, revenues_list, en_plot=0):
        num_x = len(revenues_list)

        if num_x<12:
            return None, None

        x_np = np.linspace(0,  num_x-1, num_x).reshape(num_x, 1)
        revenues_np = np.array(revenues_list).reshape(num_x, 1)  #  [n_samples, n_features]

        polynomial_features= PolynomialFeatures(degree=2)
        x_poly = polynomial_features.fit_transform(x_np)

        model = LinearRegression()
        model.fit(x_poly, revenues_np)
        y_poly_pred = model.predict(x_poly)

        #print(model.coef_)  # [[  0.         -15.80459558  16.71733017]]
        #print(model.intercept_)   # 78877.99301067

        b0 = model.intercept_[0]
        b2 = model.coef_[0][2]
        b1 = model.coef_[0][1]
        numData_3Y = len(revenues_list)
        dy_dt = b1 + 2 * b2 * numData_3Y
        y_t = b0 + b1 * numData_3Y + b2 * numData_3Y * numData_3Y
        RevenueRegress_YoYEst = dy_dt / y_t * 12
        if y_t < 0:
            RevenueRegress_YoYEst *= -1

        RevenueRegress_YoYEst_b2 = b2


        if en_plot==1:
            plt.plot(x_np, revenues_np)
            plt.plot(x_np, y_poly_pred)
            plt.show()

        return RevenueRegress_YoYEst, RevenueRegress_YoYEst_b2


    def get_revenue_growth(self, stockid, year_start, month_start, year_end, month_end, en_plot=0):
        revenues_list = self.__get_month_revenues_list(stockid, year_start, month_start, year_end, month_end)
        RevenueRegress_YoYEst, RevenueRegress_YoYEst_b2 = self.__cal_second_order_regression(revenues_list, en_plot=en_plot)

        '''
        if(RevenueRegress_YoYEst<0.05 & RevenueRegress_YoYEst>-0.05)
            RevenueRegress_YoYEst_Trend = "持平";
        else if (RevenueRegress_YoYEst > 0 && RevenueRegress_YoYEst_b2 > 0)
                RevenueRegress_YoYEst_Trend = "成長趨快";
        else if (RevenueRegress_YoYEst > 0 && RevenueRegress_YoYEst_b2 <= 0)
                RevenueRegress_YoYEst_Trend = "成長趨緩";
        else if (RevenueRegress_YoYEst <= 0 && RevenueRegress_YoYEst_b2 > 0)
                RevenueRegress_YoYEst_Trend = "衰退趨緩";
        else if (RevenueRegress_YoYEst <= 0 && RevenueRegress_YoYEst_b2 <= 0)
                RevenueRegress_YoYEst_Trend = "衰退趨快";
        else
                RevenueRegress_YoYEst_Trend = "-";
        '''

        return RevenueRegress_YoYEst