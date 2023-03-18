from mos import MOS

def isOutlier(mosCharacteristics,userDir):
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
  
  if areAbove5 and areBelow30 :
    print("It's outlier")

def main():
  mosCharacteristics = MOS()
  isOutlier(mosCharacteristics,"9")

if __name__ == "__main__":
  main()