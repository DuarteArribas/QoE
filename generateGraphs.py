import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from tqdm import tqdm

def create_dir():
    if not os.path.exists('graphs'):
        os.mkdir('graphs')
        for metric in objective_metrics:
            os.mkdir(f'graphs/{metric}')

def create_graph(file_path, results_list, codecs):
    # Reset plot
    plt.clf()

    X = [i for i in range(len(results_list[0]))]
    for i,codec_results in enumerate(results_list):
        plt.plot(X, codec_results, label=codecs[i])
    
    plt.xlabel("Bitrate")
    plt.ylabel(f"{file_path.split('/')[1]} score")
    plt.title(f"{file_path.split('/')[1]} results for image {file_path.split('/')[2].split('.')[0][-1]}")

    plt.legend()
    plt.savefig(file_path)
        
if __name__ == '__main__':
    # Get the objective evaluation metrics results
    objective_metrics = os.listdir('objective_results')
    codecs_dir = os.listdir(f'objective_results/{objective_metrics[0]}')
    bitrates = list(pd.read_csv(f'objective_results/{objective_metrics[0]}/{codecs_dir[0]}', index_col=0).index)
    codecs = [codec.split('-')[0] for codec in codecs_dir]
    create_dir()

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
