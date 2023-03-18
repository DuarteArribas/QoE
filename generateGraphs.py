import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import cv2

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
        X_t[0].append(get_bpp(f'images/AV1/bitrate-{i+1}/{int(image_index[-1]) + 1}.{codec_list["AV1"]}'))
        
        # JPG
        X_t[1].append(get_bpp(f'images/JPG/bitrate-{i+1}/{int(image_index[-1]) + 1}.{codec_list["JPG"]}'))
        
        # JPG2000
        X_t[2].append(get_bpp(f'images/JPG2000/bitrate-{i+1}/{int(image_index[-1]) + 1}.{codec_list["JPG2000"]}'))
        
    return X_t
               
def create_graph(file_path, results_list, codecs):
    # Reset plot
    plt.clf()

    X = get_bitrate_values(file_path.split('/')[-1].split('.')[0])
    for i,codec_results in enumerate(results_list):
        plt.plot(X[i], codec_results, label=codecs[i])
    
    plt.xlabel("Bitrate")
    plt.ylabel(f"{file_path.split('/')[1]} score")
    plt.title(f"{file_path.split('/')[1]} results for image {file_path.split('/')[2].split('.')[0][-1]}")

    plt.legend()
    plt.savefig(file_path)
    
def create_graph_mos(file_path, results_list, codecs):
    # Reset plot
    plt.clf()

    X = get_bitrate_values(file_path.split('/')[-1].split('.')[0])
    marker_list = ['o', 'x', '^']
    for i,codec_results in enumerate(results_list):
        codec_results = codec_results[:-1]
        plt.plot(X[i], codec_results, label=codecs[i], marker=marker_list[i])
    
    plt.xlabel("Bitrate")
    plt.ylabel(f"{file_path.split('/')[1]} score")
    plt.title(f"{file_path.split('/')[1]} results for image {file_path.split('/')[2].split('.')[0][-1]}")

    plt.legend()
    plt.savefig(file_path)

def create_objective_graphs():
    # Get the objective evaluation metrics results
    objective_metrics = os.listdir('objective_results')
    codecs_dir = os.listdir(f'objective_results/{objective_metrics[0]}')
    codecs = [codec.split('-')[0] for codec in codecs_dir]
    create_dir(objective_metrics)

    for metric in tqdm(objective_metrics,desc='Metrics'):
        # Each csv represents a codec
        df_list = [pd.read_csv(f'objective_results/{metric}/{codec}', index_col=0) for codec in codecs_dir]

        # For each image
        for i in tqdm(range(len(df_list[0].columns)), desc='Images', leave=False):
            image_results = []
            # For each codec
            for codec_df in df_list:
                image_results.append(list(codec_df[f'Image {i+1}'])) # This list contains the bitrates values for each codec
            
            create_graph(f'graphs/{metric}/Image{i + 1}.png', image_results, codecs)

def create_mos_graphs():
    # Get the mos evaluation metrics results
    codec_dir = os.listdir('mos_results')
    df_list = [pd.read_csv(f'mos_results/{codec}', index_col=0) for codec in codec_dir]
    codecs = [codec.split('Results')[0].upper() for codec in codec_dir]
    
    # For each image
    for i in tqdm(range(len(df_list[0].columns)), desc='Images', leave=False):
        image_results = []
        '''
        Each image_results is an image;
        Each list inside image_result is a codec
        Each value inside the list that is inside the list is a bitrate value, in ascending order, the last being the reference value
        '''
        # TODO: There's a problem here! Since the reference is in the list it counts as the fifth element (find a way to deal with this situation)
        for codec_df in df_list:
            image_results.append(list(codec_df[f'Image {i+1}'])) # This list contains the bitrates values for each codec
        
        create_graph_mos(f'graphs/MOS/Image{i + 1}.png', image_results, codecs)
    

if __name__ == '__main__':    
    print("Generating graphs for objective evaluation")
    create_objective_graphs()
    print('\n__________________________________________\n')
    print("Generating graphs for subjective evaluation")
    create_mos_graphs()
