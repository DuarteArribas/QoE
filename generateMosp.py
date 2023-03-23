import numpy as np
from scipy.optimize import curve_fit
import math
import os
import pandas as pd

# MOSP function (iqm == metric result)
def mosp_function(iqm,a,b,c,d):
    return a * iqm**3 + b * iqm**2 + c * iqm + d

# Opens the three csvs and makes a 1 dimensional list out of them
# Basically this organizes the dataframes data in a 1 dimensional list 
def get_metric_values(metric_path):
    csv_list = os.listdir(metric_path)

    result_list = []
    for csv in csv_list:
        df = pd.read_csv(f'{metric_path}/{csv}', index_col= 0)
        if(metric_path == 'mos_results'):
            df = df[:-1]

        result_list += list(df.values.flatten())

    return result_list

# This function generates a dataframe of mosp values and then saves them in 
def generate_mosp(objective_metric_values, mos_values, metric_name):
    popt, _ = curve_fit(mosp_function, objective_metric_values, mos_values, maxfev=500000)

    # Initialize the dataframes
    csv_list = os.listdir(f'objective_results/{metric_name}')

    # For each codec
    for i in range(3):
        mosp_df = pd.DataFrame(index = ["bitrate-1", "bitrate-2", "bitrate-3", "bitrate-4"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])
        objective_df = pd.read_csv(f'objective_results/{metric_name}/{csv_list[i]}', index_col=0)

        # Iterate the whole dataframe and get its MOSp value
        for y in range(len(objective_df.values)):
            for x in range(len(objective_df.values[0])):
                mosp_df.values[y][x] = round(mosp_function(objective_df.values[y][x], popt[0], popt[1], popt[2], popt[3]), 3)
        
        mosp_df.to_csv(f'mosp_results/{metric_name}/{csv_list[i]}')

if __name__ == '__main__':
    # Get the proper values of the metrics in lists
    mos_values = get_metric_values('mos_results')
    psnr_values = get_metric_values('objective_results/PSNR')
    ssim_values = get_metric_values('objective_results/SSIM')
    vifp_values = get_metric_values('objective_results/VIFp')

    # Generate folders
    if not os.path.exists('mosp_results'):
        os.mkdir('mosp_results')
        os.mkdir('mosp_results/PSNR')
        os.mkdir('mosp_results/SSIM')
        os.mkdir('mosp_results/VIFp')

    generate_mosp(psnr_values, mos_values, 'PSNR')
    generate_mosp(ssim_values, mos_values, 'SSIM')
    generate_mosp(vifp_values, mos_values, 'VIFp')

    