from scipy import ndimage
import cv2
import numpy as np
import os

def getLumaValues(image):
  return cv2.imread(image,cv2.IMREAD_GRAYSCALE)

def normalize(value,b):
  return float(value / (2 ** b - 1))

def eotfSdr(value):
  gamma = 2.4
  lMin = 0.1
  lMax = 300
  value = np.maximum(value,0.0)
  value = np.minimum(value,1.0)
  a     = np.power(
    np.power(lMax,1.0 / gamma) - np.power(lMin,1.0 / gamma),
    gamma
  )
  b = np.power(lMin, 1.0 / gamma) / (
      np.power(lMax, 1.0 / gamma) - np.power(lMin, 1.0 / gamma)
  )
  return a * np.power(np.maximum(value + b,0),gamma)

def oetf(value):
  m1 = 0.1593017578125
  m2 = 78.84375
  c1 = 0.8359375
  c2 = 18.8515625
  c3 = 18.6875
  Y = value / 10000
  return np.power((c1 + c2 * np.power(Y,m1)) / (1 + c3 * np.power(Y,m1)),m2)
  
def denormalize(value,b):
  return float(value * (2 ** b - 1))

imagesDict = {}

for image in os.listdir("images/InitialReferences"):
  luma = getLumaValues(f"images/InitialReferences/{image}")
  luma = luma.astype(float)
  for rowNum,row in enumerate(luma):
    for colNum,value in enumerate(row):
      luma[rowNum][colNum] = float(normalize(value,32))
  for rowNum,row in enumerate(luma):
    for colNum,value in enumerate(row):
      luma[rowNum][colNum] = float(eotfSdr(value))
  for rowNum,row in enumerate(luma):
    for colNum,value in enumerate(row):
      luma[rowNum][colNum] = float(oetf(value))

  result = ndimage.sobel(luma)
  si     = np.array(result).std()
  imagesDict[image] = denormalize(si,32)
  
print("== SI of the images ==\n")
print(imagesDict)
print("\n\n")
print("== Sorted values ==\n")
print(sorted(imagesDict,key=imagesDict.get,reverse=True))
print("\n\n")