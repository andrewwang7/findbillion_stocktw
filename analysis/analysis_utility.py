import numpy as np
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import json
import os
from math import sqrt

def dict_to_csv(dict_result, filename_csv, save_path=''):
    with open(os.path.join(save_path, filename_csv), 'w') as f:
        f.write('stock, y_true, y_pred, error(%) \n')
        for dict_result_ in dict_result:
            y_true, y_pred, y_error = dict_result_
            key = list(y_true.keys())[0]
            if y_true[key] is not None and y_pred[key] is not None and y_error[key] is not None:
                f.write("%s, %s, %s, %s\n"%(key, y_true[key], y_pred[key], y_error[key]))


def stat_dict(dict_result, filename_save, up_bound_pa, low_bound_pa, save_path=''):
    # dict to list
    list_error = []
    for dict_result_ in dict_result:
        y_true, y_pred, y_error = dict_result_
        key = list(y_true.keys())[0]
        if y_error[key] is not None:
            list_error.append(y_error[key])

    # stat
    rmse = sqrt((np.array(list_error)**2).mean())
    std = np.std(list_error)

    # the ratio between +- 10%
    np_error = np.array(list_error)
    np_error_sel = np_error[np_error < up_bound_pa]
    np_error_sel = np_error_sel[np_error_sel > low_bound_pa]
    if len(np_error)>0:
        ratio_error_pa = len(np_error_sel)/len(np_error) * 100
    else:
        ratio_error_pa = None

    print('rmse: {:6.4f}'.format(rmse))
    print('std of error: {:6.4f}'.format(std))
    print('The ratio of error in {:2f}~{:2f}: {:6.4f}'.format(low_bound_pa, up_bound_pa, ratio_error_pa))
    dict_error = {'rmse': rmse,
                  'std of error': std,
                  'The ratio of error in {:2f}~{:2f}'.format(low_bound_pa, up_bound_pa): ratio_error_pa}
    with open(os.path.join(save_path, filename_save+'.json'), 'w') as outfile:
        json.dump(dict_error, outfile)

    # plot hist
    bin_step = int((up_bound_pa-low_bound_pa)/10)
    if bin_step <1:
        bin_step = 1
    bins = [i for i in range(low_bound_pa*5, up_bound_pa*5, bin_step)]  # about 50 bins
    plt.hist(list_error, bins=bins)
    plt.xlabel('est. error (%)')
    plt.savefig(os.path.join(save_path, filename_save+'.png'))
    plt.close()



def cal_retrun(stockid, price_buy, price_sell, year_start, year_hold, fs_dividendpolicy):
    dividend_cash = fs_dividendpolicy.get_Dividend_Cash(stockid, year_start)
    dividend_stoch = 1 + fs_dividendpolicy.get_Dividend_Stock(stockid, year_start) / 10
    for idx in range(1, year_hold):
        dividend_cash_this = fs_dividendpolicy.get_Dividend_Cash(stockid, year_start + idx)
        dividend_stoch_this = fs_dividendpolicy.get_Dividend_Stock(stockid, year_start + idx)

        dividend_cash += dividend_cash_this
        dividend_stoch *= (1 + dividend_stoch_this / 10)

    if price_buy is not None and price_sell is not None:
        return_buyin = (price_sell - price_buy + dividend_cash) / price_buy * dividend_stoch
    else:
        return_buyin = None

    return return_buyin
