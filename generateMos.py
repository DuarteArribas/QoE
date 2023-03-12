import pandas as pd
import os
import numpy as np

SUBJECTIVE_RESULTS_DIR = "subjective_results"
MOS_RESULTS_DIR        = "mos_results"

jpgMosResults     = pd.DataFrame(np.zeros((5,5)), index = ["bitrate-1", "bitrate-2", "bitrate-3", "bitrate-4","Image Reference"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])
jpg2000MosResults = pd.DataFrame(np.zeros((5,5)), index = ["bitrate-1", "bitrate-2", "bitrate-3", "bitrate-4","Image Reference"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])
av1MosResults     = pd.DataFrame(np.zeros((5,5)), index = ["bitrate-1", "bitrate-2", "bitrate-3", "bitrate-4","Image Reference"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])
jpgCount          = 0
jpg2000Count      = 0
av1Count          = 0


for userDir in os.listdir(SUBJECTIVE_RESULTS_DIR):
  for result in os.listdir(os.path.join(SUBJECTIVE_RESULTS_DIR,userDir)):
    if result == "jpgResults.csv":
      jpgMosResults += pd.read_csv(os.path.join(os.path.join(SUBJECTIVE_RESULTS_DIR,userDir),result),index_col=0)
      jpgCount += 1
    if result == "jpg2000Results.csv":
      jpg2000MosResults += pd.read_csv(os.path.join(os.path.join(SUBJECTIVE_RESULTS_DIR,userDir),result),index_col=0)
      jpg2000Count += 1
    if result == "av1Results.csv":
      av1MosResults += pd.read_csv(os.path.join(os.path.join(SUBJECTIVE_RESULTS_DIR,userDir),result),index_col=0)
      av1Count += 1

if jpgCount != 0:
  jpgMosResults.div(jpgCount).to_csv(f"{MOS_RESULTS_DIR}/jpgResults.csv")
if jpg2000Count != 0:
  jpg2000MosResults.div(jpg2000Count).to_csv(f"{MOS_RESULTS_DIR}/jpg2000Results.csv")
if av1Count != 0:
  av1MosResults.div(av1Count).to_csv(f"{MOS_RESULTS_DIR}/av1Results.csv")