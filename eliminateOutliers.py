from mos import MOS

def main():
  mosCharacteristics = MOS()
  print(mosCharacteristics.countValuesOutsideCI("1",mosCharacteristics.getConfidenceIntervals()))
  print(mosCharacteristics.countValuesAboveCI("1",mosCharacteristics.getConfidenceIntervals()))
  print(mosCharacteristics.countValuesBelowCI("1",mosCharacteristics.getConfidenceIntervals()))

if __name__ == "__main__":
  main()