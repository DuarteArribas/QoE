from mos import MOS
import os
import shutil

def isOutlier(userDir,mosCharacteristics):
  areAbove5 = mosCharacteristics.countValuesOutsideCI(
    userDir,
    mosCharacteristics.getConfidenceIntervals()
  ) > (0.05 * mosCharacteristics.countOfAllScores())
  areBelow30 = abs(
    mosCharacteristics.countValuesAboveCI(
      userDir,
      mosCharacteristics.getConfidenceIntervals()
    ) - mosCharacteristics.countValuesBelowCI(
      userDir,
      mosCharacteristics.getConfidenceIntervals()
    )
  ) < (.3 * mosCharacteristics.countOfAllScores())
  return areAbove5 and areBelow30


def removeOutliers(mosCharacteristics):
  for userDir in os.listdir(MOS.SUBJECTIVE_RESULTS_DIR):
    if isOutlier(userDir,mosCharacteristics):
      print(f"User {userDir} is an outlier 🤣🤣...removing...")
      shutil.rmtree(os.path.join(MOS.SUBJECTIVE_RESULTS_DIR,userDir))
    
def main():
  mosCharacteristics = MOS()
  removeOutliers(mosCharacteristics)

if __name__ == "__main__":
  main()