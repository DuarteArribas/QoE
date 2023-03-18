from mos import MOS

def main():
  mosCharacteristics = MOS()
  mosCharacteristics.printResultsArray(mosCharacteristics.getConfidenceIntervals()[0])

if __name__ == "__main__":
  main()