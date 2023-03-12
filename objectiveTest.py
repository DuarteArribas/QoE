'''
TODO:
PSNR/MSR

SSIM

VIFp/VIF
'''
# Imports
import cv2
import numpy as np
from skimage.metrics import structural_similarity as SSIM
from sewar.full_ref import psnr, ssim, vifp # TODO: É possível usar esta biblioteca para todos mas decidi não o fazer. Discutir se o devo fazer ou não

reference_img = cv2.imread('images/1.png')
encoded_img = cv2.imread('images/1_coded.png')

# PSNR
# psnr_score = cv2.PSNR(reference_img, encoded_img)
psnr_score = psnr(encoded_img, reference_img)
print("PSNR score: ", psnr_score)

# SSIM
reference_gray = cv2.cvtColor(reference_img, cv2.COLOR_BGR2GRAY)
encoded_gray = cv2.cvtColor(encoded_img, cv2.COLOR_BGR2GRAY)
ssim_score, _ = SSIM(reference_gray, encoded_gray, full=True)
print("SSIM score: ", ssim_score)

# VIFp
vifp_score = vifp(encoded_img, reference_img)
print("VIF score: ", vifp_score)