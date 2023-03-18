from mos import MOS

def main():
  mosCharacteristics = MOS()
  mosCharacteristics.printResultsArray(mosCharacteristics.av1ArrayResults)
  print(mosCharacteristics.countOfAllScores()[2])

if __name__ == "__main__":
  main()