import numpy as np
from sklearn.linear_model import LinearRegression
import math
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import mean_squared_error

# Returns the values of the metric in a format of list of lists, where each inside list will have all the values for image i
def get_metric_values(metric_path):
    csv_list = os.listdir(metric_path)

    result_list = []
    for csv in csv_list:
        df = pd.read_csv(f'{metric_path}/{csv}', index_col= 0)
        if(metric_path == 'mos_results'):
            df = df[:-1]

        result_list += list(df.values.flatten())

    return result_list

if __name__ == '__main__':
    # Get the proper values of the metrics in lists
    mos_values = get_metric_values('mos_results')
    mosp_psnr_values = get_metric_values('mosp_results/PSNR')
    mosp_ssim_values = get_metric_values('mosp_results/SSIM')
    mosp_vifp_values = get_metric_values('mosp_results/VIFp')

    
    print('Pearson:')
    psnr_pearson = pearsonr(mos_values, mosp_psnr_values)
    ssim_pearson = pearsonr(mos_values, mosp_ssim_values)
    vifp_pearson = pearsonr(mos_values, mosp_vifp_values)
    print('PSNR: ', round(psnr_pearson[0], 4))
    print('SSIM: ', round(ssim_pearson[0], 4))
    print('VIFp: ', round(vifp_pearson[0], 4))

    print('\nSpearman:')
    psnr_spearman = spearmanr(mos_values, mosp_psnr_values)
    ssim_spearman = spearmanr(mos_values, mosp_ssim_values)
    vifp_spearman = spearmanr(mos_values, mosp_vifp_values)
    print('PSNR: ', round(psnr_spearman[0], 4))
    print('SSIM: ', round(ssim_spearman[0], 4))
    print('VIFp: ', round(vifp_spearman[0], 4))
    
    print('\nMean Square Root Error:')
    psnr_pearson = mean_squared_error(mos_values, mosp_psnr_values, squared=False)
    ssim_pearson = mean_squared_error(mos_values, mosp_ssim_values, squared=False)
    vifp_pearson = mean_squared_error(mos_values, mosp_vifp_values, squared=False)
    print('PSNR: ', round(psnr_pearson, 4))
    print('SSIM: ', round(ssim_pearson, 4))
    print('VIFp: ', round(vifp_pearson, 4))