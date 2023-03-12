'''
TODO:
PSNR/MSR

SSIM

VIFp/VIF
'''
# Imports
import cv2
import numpy as np
from skimage.metrics import structural_similarity as SSIM, peak_signal_noise_ratio as PSNR1
from sewar.full_ref import psnr, ssim, vifp # TODO: É possível usar esta biblioteca para todos mas decidi não o fazer. Discutir se o devo fazer ou não
import pandas as pd
import os
from tqdm import tqdm

SCORES_DIR = {}
CODEC_LIST = {'JPG':'jpg', 'JPG2000':'jp2', 'AV1':'png'} # Name followed by extension
BITRATE_LIST = ['bitrate-1', 'bitrate-2', 'bitrate-3', 'bitrate-4']


# reference_img = cv2.imread('images/1.png')
# encoded_img = cv2.imread('images/1_coded.png')

# # PSNR
# psnr_score = cv2.PSNR(reference_img, encoded_img)
# print("PSNR score: ", psnr_score)
# psnr_score = PSNR1(reference_img, encoded_img)
# print("PSNR score: ", psnr_score)

# # SSIM
# reference_gray = cv2.cvtColor(reference_img, cv2.COLOR_BGR2GRAY)
# encoded_gray = cv2.cvtColor(encoded_img, cv2.COLOR_BGR2GRAY)
# ssim_score, _ = SSIM(reference_gray, encoded_gray, full=True)
# # ssim_score = ssim(encoded_img, reference_img)
# print("SSIM score: ", ssim_score)

# # VIFp
# vifp_score = vifp(encoded_img, reference_img)
# print("VIF score: ", vifp_score)

def initialize_dict():
    empty_dataframe = pd.DataFrame(index = ["bitrate-1", "bitrate-2", "bitrate-3", "bitrate-4"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])
    SCORES_DIR['PSNR'] = {}
    SCORES_DIR['SSIM'] = {}
    SCORES_DIR['VIFp'] = {}
    
    for codec in CODEC_LIST:
        SCORES_DIR['PSNR'][codec] = empty_dataframe.copy()
        SCORES_DIR['SSIM'][codec] = empty_dataframe.copy()
        SCORES_DIR['VIFp'][codec] = empty_dataframe.copy()    

def psnr_evaluation():
    if not os.path.exists('objective_results/PSNR'):
        os.mkdir('objective_results/PSNR')

    for codec in tqdm(CODEC_LIST, desc=f'Codecs'):
        for i in tqdm(range(1,6), leave=False, desc=f'Images'):
            reference_img = cv2.imread(f'images/References/{i}.png')
            for bitrate in os.listdir(f'images/{codec}'):
                SCORES_DIR['PSNR'][codec][f'Image {i}'][bitrate] = round(cv2.PSNR(reference_img, cv2.imread(f'images/{codec}/{bitrate}/{i}.{CODEC_LIST[codec]}')),3)

    print(SCORES_DIR['PSNR'])

    for codec in CODEC_LIST:
        SCORES_DIR['PSNR'][codec].to_csv(f'objective_results/PSNR/{codec}-Results.csv')
                
def ssim_evaluation():
    if not os.path.exists('objective_results/SSIM'):
        os.mkdir('objective_results/SSIM')

    for codec in tqdm(CODEC_LIST, desc=f'Codecs'):
        for i in tqdm(range(1,6), leave=False, desc=f'Images'):
            reference_img = cv2.imread(f'images/References/{i}.png')
            reference_gray = cv2.cvtColor(reference_img, cv2.COLOR_BGR2GRAY)
            for bitrate in os.listdir(f'images/{codec}'):
                encoded_img = cv2.imread(f'images/{codec}/{bitrate}/{i}.{CODEC_LIST[codec]}')
                encoded_gray = cv2.cvtColor(encoded_img, cv2.COLOR_BGR2GRAY)
                SCORES_DIR['SSIM'][codec][f'Image {i}'][bitrate],_ = SSIM(reference_gray, encoded_gray, full=True)
                SCORES_DIR['SSIM'][codec][f'Image {i}'][bitrate] = round(SCORES_DIR['SSIM'][codec][f'Image {i}'][bitrate], 3)
    print(SCORES_DIR['SSIM'])

    for codec in CODEC_LIST:
        SCORES_DIR['SSIM'][codec].to_csv(f'objective_results/SSIM/{codec}-Results.csv')

def vifp_evaluation():
    if not os.path.exists('objective_results/VIFp'):
        os.mkdir('objective_results/VIFp')

    for codec in tqdm(CODEC_LIST, desc=f'Codecs'):
        for i in tqdm(range(1,6), leave=False, desc=f'Images'):
            reference_img = cv2.imread(f'images/References/{i}.png')
            for bitrate in os.listdir(f'images/{codec}'):
                encoded_img = cv2.imread(f'images/{codec}/{bitrate}/{i}.{CODEC_LIST[codec]}')
                SCORES_DIR['VIFp'][codec][f'Image {i}'][bitrate] = round(vifp(encoded_img, reference_img),3)

    print(SCORES_DIR['VIFp'])

    for codec in CODEC_LIST:
        SCORES_DIR['VIFp'][codec].to_csv(f'objective_results/VIFp/{codec}-Results.csv')

if __name__ == "__main__":
    initialize_dict()

    print('______________________________________')
    print('Analysing PSNR metric:')
    psnr_evaluation()
    print('\n______________________________________\n')
    print('Analysing SSIM metric:')
    ssim_evaluation()
    print('\n______________________________________\n')
    print('Analysing VIFp metric:')
    vifp_evaluation()
    print('______________________________________')

