import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import cv2
from mos import MOS 


# Auxiliary functions
def create_dir(objective_metrics):
    if not os.path.exists('graphs'):
        os.mkdir('graphs')
        for metric in objective_metrics:
            os.mkdir(f'graphs/{metric}')
    
        os.mkdir('graphs/MOS')
        
def get_bpp(img_path):
    resolution = 563000
    size = os.stat(img_path).st_size * 8

    return size / resolution
    
def get_bitrate_values(image_index):
    codec_list = {'JPG':'jpg', 'JPG2000':'jp2', 'AV1':'mp4'} 

    # Para cada bitrate [1,..,n], encontrar o bpp para a imagem i+1
    # Criar três listas, uma para cada codec
    X_t = [[],[],[]]
    for i in range(4):
        # AV1
        X_t[0].append(get_bpp(f'images/AV1/bitrate-{i+1}/{int(image_index[-1])}.{codec_list["AV1"]}'))
        
        # JPG
        X_t[1].append(get_bpp(f'images/JPG/bitrate-{i+1}/{int(image_index[-1])}.{codec_list["JPG"]}'))
        
        # JPG2000
        X_t[2].append(get_bpp(f'images/JPG2000/bitrate-{i+1}/{int(image_index[-1])}.{codec_list["JPG2000"]}'))
        
    return X_t


# Objective Metrics                   
def create_graph(file_path, results_list, codecs):
    # Reset plot
    plt.clf()

    # Go through every image
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20,7))
    for j in range(len(results_list)):
        X = get_bitrate_values(f'Image{j+1}')
        for i,codec_results in enumerate(results_list[j]):
            if j == 0:
                axes[0][j].plot(X[i], codec_results, label=codecs[i])
                axes[0][j].set_title(f"image {j + 1}")
            elif j < 3:
                axes[0][j].plot(X[i], codec_results, label='_nolegend_')
                axes[0][j].set_title(f"image {j + 1}")
            else: 
                axes[1][j - 3].plot(X[i], codec_results, label='_nolegend_')
                axes[1][j - 3].set_title(f"image {j + 1}")

    fig.suptitle(f"{file_path.split('/')[-1]} results", fontsize=26)
    fig.delaxes(axes[1][2])
    fig.text(0.5, 0.04, 'Bitrate', ha='center', va='center', fontsize=20)
    fig.text(0.06, 0.5, f"{file_path.split('/')[-1]} score", ha='center', va='center', rotation='vertical', fontsize=20)
    fig.legend(fontsize=16)
    fig.savefig(file_path)

def create_objective_graphs():
    # Get the objective evaluation metrics results
    objective_metrics = os.listdir('objective_results')
    codecs_dir = os.listdir(f'objective_results/{objective_metrics[0]}')
    codecs = [codec.split('-')[0] for codec in codecs_dir]
    create_dir(objective_metrics)

    for metric in tqdm(objective_metrics,desc='Metrics'):
        # Each csv represents a codec
        df_list = [pd.read_csv(f'objective_results/{metric}/{codec}', index_col=0) for codec in codecs_dir]

        img_all_results = []
        
        # For each image
        for i in tqdm(range(len(df_list[0].columns)), desc='Images', leave=False):
            image_results = []
            # For each codec
            for codec_df in df_list:
                image_results.append(list(codec_df[f'Image {i+1}'])) # This list contains the bitrates values for each codec
            img_all_results.append(image_results)
        create_graph(f'graphs/{metric}', img_all_results, codecs)
            

# MOS graphs
def create_graph_mos(file_path, results_list, confidence_intervals, codecs):
    # Reset plot
    plt.clf()
    
    # Go through every image
    marker_list = ['o', 'x', '^']
    
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20,7))
    for j in range(len(results_list)):
        X = get_bitrate_values(f'Image{j+1}')
        X = [X[0], X[2], X[1]]
        for i,codec_results in enumerate(results_list[j]):
            # Plot the results with error bars for the confidence intervals            
            yerr = np.array(confidence_intervals[j][i]).reshape(2, -1)
            if j == 0:
                axes[0][j].errorbar(X[i], codec_results, yerr=yerr, label=codecs[i], 
                        marker=marker_list[i], capsize=5, capthick=2, alpha=0.7, linestyle='')
                axes[0][j].set_title(f"image {j + 1}")
            elif j < 3:
                axes[0][j].errorbar(X[i], codec_results, yerr=yerr, label='_nolegend_', 
                        marker=marker_list[i], capsize=5, capthick=2, alpha=0.7, linestyle='')
                axes[0][j].set_title(f"image {j + 1}")
            else: 
                axes[1][j - 3].errorbar(X[i], codec_results, yerr=yerr, label='_nolegend_', 
                        marker=marker_list[i], capsize=5, capthick=2, alpha=0.7, linestyle='')
                axes[1][j - 3].set_title(f"image {j + 1}")

    
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.suptitle('MOS results', fontsize=26)
    fig.delaxes(axes[1][2])
    fig.text(0.5, 0.04, 'Bitrate', ha='center', va='center', fontsize=20)
    fig.text(0.06, 0.5, 'MOS score', ha='center', va='center', rotation='vertical', fontsize=20)
    fig.legend(fontsize=16)
    fig.savefig(file_path)

def create_mos_graphs():
    # Get the mos evaluation metrics results
    codec_dir = os.listdir('mos_results')
    df_list = [pd.read_csv(f'mos_results/{codec}', index_col=0)[:-1] for codec in codec_dir]
    mos_c = MOS()
    ci = mos_c.getConfidenceIntervals_dataframe()[::-1]
    codecs = [codec.split('Results')[0].upper() for codec in codec_dir]
    
    img_all_results = []
    ci_all_results = []
    
    # For each image
    for i in tqdm(range(len(df_list[0].columns)), desc='Images'):
        image_results = []
        confidence_intervals = []
        '''
        Each image_results is an image;
        Each list inside image_result is a codec
        Each value inside the list that is inside the list is a bitrate value, in ascending order, the last being the reference value
        '''
        for j in range(len(df_list)):
            image_results.append(list(df_list[j][f'Image {i+1}'])) # This list contains the bitrates values for each codec
            confidence_intervals.append(list(ci[j][f'Image {i+1}'])) # This list contains the bitrates values for each codec
            
        img_all_results.append(image_results)
        ci_all_results.append(confidence_intervals)
        
    create_graph_mos(f'graphs/MOS', img_all_results, ci_all_results, codecs)
    

if __name__ == '__main__':    
    print("Generating graphs for objective evaluation")
    create_objective_graphs()
    print('\n__________________________________________\n')
    print("Generating graphs for subjective evaluation")
    create_mos_graphs()
