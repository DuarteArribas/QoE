import pandas as pd
import os
import shutil
import numpy as np


SUBJECTIVE_RESULTS_DIR = "subjective_results"

jpgArrayResults     = pd.DataFrame(np.zeros((5,5)), index = ["bitrate-1", "bitrate-2", "bitrate-3", "bitrate-4","Image Reference"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])
jpg2000ArrayResults = pd.DataFrame(np.zeros((5,5)), index = ["bitrate-1", "bitrate-2", "bitrate-3", "bitrate-4","Image Reference"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])
av1ArrayResults     = pd.DataFrame(np.zeros((5,5)), index = ["bitrate-1", "bitrate-2", "bitrate-3", "bitrate-4","Image Reference"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])

def generateArrayResults():
  for userDir in os.listdir(SUBJECTIVE_RESULTS_DIR):
    for result in os.listdir(os.path.join(SUBJECTIVE_RESULTS_DIR,userDir)):
      if result == "jpgResults.csv":
        temp = pd.read_csv(os.path.join(os.path.join(SUBJECTIVE_RESULTS_DIR,userDir),result),index_col=0)
        for i in range(5):
          for j in range(5):
          
        
        jpgArrayResults
      if result == "jpg2000Results.csv":
        temp = pd.read_csv(os.path.join(os.path.join(SUBJECTIVE_RESULTS_DIR,userDir),result),index_col=0)
      if result == "av1Results.csv":
        temp = pd.read_csv(os.path.join(os.path.join(SUBJECTIVE_RESULTS_DIR,userDir),result),index_col=0)
        print(temp)

def removeUser(user):
  shutil.rmtree(f"subjective_results/{user}")

def main():
  generateArrayResults()
  
if __name__ == "__main__":
  main()