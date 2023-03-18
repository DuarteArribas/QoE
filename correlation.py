import numpy as np
from scipy.optimize import curve_fit
import math
import os
import pandas as pd

# MOSP function (iqm == metric result)
# def get_mosp(a,b,c, iqm):
#     return a / (1 + math.e(-b * (iqm - c)))    
def get_mosp(iqm,a,b,c,d):
    return a + b * np.exp(-c * iqm) + d * iqm

def get_metric_values(metric_path):
    csv_list = os.listdir(metric_path)

    result_list = []
    for csv in csv_list:
        df = pd.read_csv(f'{metric_path}/{csv}', index_col= 0)
        if(metric_path == 'mos_results'):
            df = df[:-1]
        result_list += list(df.values.flatten())
    
    return result_list

# Fit the MOSP function to the data using curve_fit

mos_values = get_metric_values('mos_results')
psnr_values = get_metric_values('objective_results/PSNR')
ssim_values = get_metric_values('objective_results/PSNR')
vifp_values = get_metric_values('objective_results/PSNR')

print(len(mos_values))
print(len(psnr_values))

# PSNR correlation
popt, pcov = curve_fit(get_mosp, psnr_values, mos_values)

a,b,c,d = popt

# # AV1
# v = 20.0

# Initialize the dataframes
csv_list = os.listdir('objective_results/PSNR')

# Generate folders
if not os.path.exists('mosp_results'):
    os.mkdir('mosp_results')
    os.mkdir('mosp_results/PSNR')
    os.mkdir('mosp_results/SSIM')
    os.mkdir('mosp_results/VIFp')


for i in range(3):
    mosp_df = pd.DataFrame(index = ["bitrate-1", "bitrate-2", "bitrate-3", "bitrate-4"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])
    objective_df = pd.read_csv(f'objective_results/PSNR/{csv_list[i]}', index_col=0)

    for y in range(len(objective_df.values)):
        for x in range(len(objective_df.values[0])):
            mosp_df.values[y][x] = round(get_mosp(objective_df.values[y][x], a, b, c, d), 3)
    
    mosp_df.to_csv(f'mosp_results/PSNR/{csv_list[i]}')

    
        
# print(df_list[0])
# print(get_mosp(v,a,b,c,d))
