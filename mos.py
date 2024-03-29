import pandas as pd
import os
import numpy as np
import scipy.stats as st
import math

class MOS:
  # == Class Variables ==
  SUBJECTIVE_RESULTS_DIR = "subjective_results"
    
  # == Methods ==
  def __init__(self):
    self.jpgArrayResults     = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
    self.jpg2000ArrayResults = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
    self.av1ArrayResults     = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
    self.initializeResultArrays()
    
  def initializeResultArrays(self):
    for userDir in os.listdir(MOS.SUBJECTIVE_RESULTS_DIR):
      for result in os.listdir(os.path.join(MOS.SUBJECTIVE_RESULTS_DIR,userDir)):
        csvTemp = os.path.join(os.path.join(MOS.SUBJECTIVE_RESULTS_DIR,userDir),result)
        if result == "jpgResults.csv":
          temp = pd.read_csv(csvTemp,index_col = 0)
          for i in range(5):
            for j in range(5):
              self.jpgArrayResults[i][j].append(temp.iloc[i,j])
        if result == "jpg2000Results.csv":
          temp = pd.read_csv(csvTemp,index_col = 0)
          for i in range(5):
            for j in range(5):
              self.jpg2000ArrayResults[i][j].append(temp.iloc[i,j])
        if result == "av1Results.csv":
          temp = pd.read_csv(csvTemp,index_col = 0)
          for i in range(5):
            for j in range(5):
              self.av1ArrayResults[i][j].append(temp.iloc[i,j])

  def getMeans(self):
    jpgMean     = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0,],[0,0,0,0,0,],[0,0,0,0,0]]
    jpg2000Mean = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0,],[0,0,0,0,0,],[0,0,0,0,0]]
    av1Mean     = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    for i in range(5):
      for j in range(5):
        jpgMean[i][j]     = np.mean(np.array(self.jpgArrayResults[i][j]))
        jpg2000Mean[i][j] = np.mean(np.array(self.jpg2000ArrayResults[i][j]))
        av1Mean[i][j]     = np.mean(np.array(self.av1ArrayResults[i][j]))
    return (jpgMean,jpg2000Mean,av1Mean)

  def getStddevs(self):
    jpgStdev     = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    jpg2000Stdev = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    av1Stdev     = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    for i in range(5):
      for j in range(5):
        jpgStdev[i][j]     = np.std(np.array(self.jpgArrayResults[i][j]))
        jpg2000Stdev[i][j] = np.std(np.array(self.jpg2000ArrayResults[i][j]))
        av1Stdev[i][j]     = np.std(np.array(self.av1ArrayResults[i][j]))
    return (jpgStdev,jpg2000Stdev,av1Stdev)

  def getConfidenceIntervals(self):
    jpgCI     = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    jpg2000CI = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    av1CI     = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    means   = self.getMeans()
    stddevs = self.getStddevs()
    for i in range(5):
      for j in range(5):
        jpgCI[i][j]     = (
          means[0][i][j] - (st.t.ppf(1 - 0.05 / 2,len(self.jpgArrayResults[i][j]) - 1) * (stddevs[0][i][j] / math.sqrt(len(self.jpgArrayResults[i][j])))),
          means[0][i][j] + (st.t.ppf(1 - 0.05 / 2,len(self.jpgArrayResults[i][j]) - 1) * (stddevs[0][i][j] / math.sqrt(len(self.jpgArrayResults[i][j]))))
        )
        jpg2000CI[i][j] = (
          means[1][i][j] - (st.t.ppf(1 - 0.05 / 2,len(self.jpg2000ArrayResults[i][j]) - 1) * (stddevs[1][i][j] / math.sqrt(len(self.jpg2000ArrayResults[i][j])))),
          means[1][i][j] + (st.t.ppf(1 - 0.05 / 2,len(self.jpg2000ArrayResults[i][j]) - 1) * (stddevs[1][i][j] / math.sqrt(len(self.jpg2000ArrayResults[i][j]))))
        )
        av1CI[i][j]     = (
          means[2][i][j] - (st.t.ppf(1 - 0.05 / 2,len(self.av1ArrayResults[i][j]) - 1) * (stddevs[2][i][j] / math.sqrt(len(self.av1ArrayResults[i][j])))),
          means[2][i][j] + (st.t.ppf(1 - 0.05 / 2,len(self.av1ArrayResults[i][j]) - 1) * (stddevs[2][i][j] / math.sqrt(len(self.av1ArrayResults[i][j]))))
        )
    return (jpgCI,jpg2000CI,av1CI)
  
  def getConfidenceIntervalsOutlier(self,value):
    jpgCI     = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    jpg2000CI = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    av1CI     = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    means   = self.getMeans()
    stddevs = self.getStddevs()
    for i in range(5):
      for j in range(5):
        jpgCI[i][j]     = (means[0][i][j] - stddevs[0][i][j] * value,means[0][i][j] + stddevs[0][i][j] * value)
        jpg2000CI[i][j] = (means[1][i][j] - stddevs[1][i][j] * value,means[1][i][j] + stddevs[1][i][j] * value)
        av1CI[i][j]     = (means[2][i][j] - stddevs[2][i][j] * value,means[2][i][j] + stddevs[2][i][j] * value)
    return (jpgCI,jpg2000CI,av1CI)
  
  def getConfidenceIntervals_dataframe(self):
    jpgCI     = pd.DataFrame(index = ["bitrate-1", "bitrate-2", "bitrate-3", "bitrate-4"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])
    jpg2000CI = pd.DataFrame(index = ["bitrate-1", "bitrate-2", "bitrate-3", "bitrate-4"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])
    av1CI     = pd.DataFrame(index = ["bitrate-1", "bitrate-2", "bitrate-3", "bitrate-4"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])
    means   = self.getMeans()
    stddevs = self.getStddevs()
    for i in range(5):
      for j in range(4):
        jpgCI.values.T[i][j]     = (
          means[0][i][j] - (st.t.ppf(1 - 0.05 / 2,len(self.jpgArrayResults[i][j]) - 1) * (stddevs[0][i][j] / math.sqrt(len(self.jpgArrayResults[i][j])))),
          means[0][i][j] + (st.t.ppf(1 - 0.05 / 2,len(self.jpgArrayResults[i][j]) - 1) * (stddevs[0][i][j] / math.sqrt(len(self.jpgArrayResults[i][j]))))
        )
        jpg2000CI.values.T[i][j] = (
          means[1][i][j] - (st.t.ppf(1 - 0.05 / 2,len(self.jpg2000ArrayResults[i][j]) - 1) * (stddevs[1][i][j] / math.sqrt(len(self.jpg2000ArrayResults[i][j])))),
          means[1][i][j] + (st.t.ppf(1 - 0.05 / 2,len(self.jpg2000ArrayResults[i][j]) - 1) * (stddevs[1][i][j] / math.sqrt(len(self.jpg2000ArrayResults[i][j]))))
        )
        av1CI.values.T[i][j]     = (
          means[2][i][j] - (st.t.ppf(1 - 0.05 / 2,len(self.av1ArrayResults[i][j]) - 1) * (stddevs[2][i][j] / math.sqrt(len(self.av1ArrayResults[i][j])))),
          means[2][i][j] + (st.t.ppf(1 - 0.05 / 2,len(self.av1ArrayResults[i][j]) - 1) * (stddevs[2][i][j] / math.sqrt(len(self.av1ArrayResults[i][j]))))
        )
    return [jpgCI,jpg2000CI,av1CI]

  def printResultsArray(self,threeDArray):
    for i in range(5):
      for j in range(5):
        print(threeDArray[i][j],end="|")
      print()
  
  def countOfAllScores(self):
    countJpg     = 0
    countJpg2000 = 0
    countAv1     = 0
    for i in range(5):
      for j in range(5):
        countJpg     += len(self.jpgArrayResults[i][j])
        countJpg2000 += len(self.jpg2000ArrayResults[i][j])
        countAv1     += len(self.av1ArrayResults[i][j])
    return countJpg + countJpg2000 + countAv1
  
  def countValuesOutsideCI(self,userDir,CIs):
    jpgCI     = CIs[0]
    jpg2000CI = CIs[1]
    av1CI     = CIs[2]
    countValuesOutside = 0
    for result in os.listdir(os.path.join(MOS.SUBJECTIVE_RESULTS_DIR,userDir)):
      csvTemp = os.path.join(os.path.join(MOS.SUBJECTIVE_RESULTS_DIR,userDir),result)
      if result == "jpgResults.csv":
        temp = pd.read_csv(csvTemp,index_col = 0)
        for i in range(5):
          for j in range(5):
            if temp.iloc[i,j] < jpgCI[i][j][0] or temp.iloc[i,j] > jpgCI[i][j][1]:
              countValuesOutside += 1
      if result == "jpg2000Results.csv":
        temp = pd.read_csv(csvTemp,index_col = 0)
        for i in range(5):
          for j in range(5):
            if temp.iloc[i,j] < jpg2000CI[i][j][0] or temp.iloc[i,j] > jpg2000CI[i][j][1]:
              countValuesOutside += 1
      if result == "av1Results.csv":
        temp = pd.read_csv(csvTemp,index_col = 0)
        for i in range(5):
          for j in range(5):
            if temp.iloc[i,j] < av1CI[i][j][0] or temp.iloc[i,j] > av1CI[i][j][1]:
              countValuesOutside += 1
    return countValuesOutside

  def countValuesAboveCI(self,userDir,CIs):
    jpgCI     = CIs[0]
    jpg2000CI = CIs[1]
    av1CI     = CIs[2]
    countValuesAbove = 0
    for result in os.listdir(os.path.join(MOS.SUBJECTIVE_RESULTS_DIR,userDir)):
      csvTemp = os.path.join(os.path.join(MOS.SUBJECTIVE_RESULTS_DIR,userDir),result)
      if result == "jpgResults.csv":
        temp = pd.read_csv(csvTemp,index_col = 0)
        for i in range(5):
          for j in range(5):
            if temp.iloc[i,j] > jpgCI[i][j][1]:
              countValuesAbove += 1
      if result == "jpg2000Results.csv":
        temp = pd.read_csv(csvTemp,index_col = 0)
        for i in range(5):
          for j in range(5):
            if temp.iloc[i,j] > jpg2000CI[i][j][1]:
              countValuesAbove += 1
      if result == "av1Results.csv":
        temp = pd.read_csv(csvTemp,index_col = 0)
        for i in range(5):
          for j in range(5):
            if temp.iloc[i,j] > av1CI[i][j][1]:
              countValuesAbove += 1
    return countValuesAbove

  def countValuesBelowCI(self,userDir,CIs):
    jpgCI     = CIs[0]
    jpg2000CI = CIs[1]
    av1CI     = CIs[2]
    countValuesBelow = 0
    for result in os.listdir(os.path.join(MOS.SUBJECTIVE_RESULTS_DIR,userDir)):
      csvTemp = os.path.join(os.path.join(MOS.SUBJECTIVE_RESULTS_DIR,userDir),result)
      if result == "jpgResults.csv":
        temp = pd.read_csv(csvTemp,index_col = 0)
        for i in range(5):
          for j in range(5):
            if temp.iloc[i,j] < jpgCI[i][j][0]:
              countValuesBelow += 1
      if result == "jpg2000Results.csv":
        temp = pd.read_csv(csvTemp,index_col = 0)
        for i in range(5):
          for j in range(5):
            if temp.iloc[i,j] < jpg2000CI[i][j][0]:
              countValuesBelow += 1
      if result == "av1Results.csv":
        temp = pd.read_csv(csvTemp,index_col = 0)
        for i in range(5):
          for j in range(5):
            if temp.iloc[i,j] < av1CI[i][j][0]:
              countValuesBelow += 1
    return countValuesBelow

  def checkDistributionNormal(self,userDir):
    allData = []
    for result in os.listdir(os.path.join(MOS.SUBJECTIVE_RESULTS_DIR,userDir)):
      csvTemp = os.path.join(os.path.join(MOS.SUBJECTIVE_RESULTS_DIR,userDir),result)
      temp = pd.read_csv(csvTemp,index_col = 0)
      for i in range(5):
        for j in range(5):
          allData.append(temp.iloc[i,j])
    return st.shapiro(allData)[1] > 0.05