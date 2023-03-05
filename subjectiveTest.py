import pygame
import random
import enum
import os
import pandas as pd

AVAILABLE_CODECS = ["jpg","jpg2000"]

REFERENCE_IMAGES_JPG     = ["1ref.jpg","2ref.jpg","3ref.jpg","4ref.jpg","5ref.jpg"]
CODED_IMAGES_JPG         = {
  "1" : ["1-1.jpg","1-2.jpg","1-3.jpg","1-4.jpg"],
  "2" : ["2-1.jpg","2-2.jpg","2-3.jpg","2-4.jpg"],
  "3" : ["3-1.jpg","3-2.jpg","3-3.jpg","3-4.jpg"],
  "4" : ["4-1.jpg","4-2.jpg","4-3.jpg","4-4.jpg"],
  "5" : ["5-1.jpg","5-2.jpg","5-3.jpg","5-4.jpg"]
}

REFERENCE_IMAGES_JPG2000 = ["1ref.jpg2000","2ref.jpg2000","3ref.jpg2000","4ref.jpg2000","5ref.jpg2000"]
CODED_IMAGES_JPG2000     = {
  "1" : ["1-1.jpg2000","1-2.jpg2000","1-3.jpg2000","1-4.jpg2000"],
  "2" : ["2-1.jpg2000","2-2.jpg2000","2-3.jpg2000","2-4.jpg2000"],
  "3" : ["3-1.jpg2000","3-2.jpg2000","3-3.jpg2000","3-4.jpg2000"],
  "4" : ["4-1.jpg2000","4-2.jpg2000","4-3.jpg2000","4-4.jpg2000"],
  "5" : ["5-1.jpg2000","5-2.jpg2000","5-3.jpg2000","5-4.jpg2000"]
}

MAPPER_REFERENCE = {
  "jpg"     : REFERENCE_IMAGES_JPG,
  "jpg2000" : REFERENCE_IMAGES_JPG2000,
}

MAPPER_CODED = {
  "jpg"     : CODED_IMAGES_JPG,
  "jpg2000" : CODED_IMAGES_JPG2000,
}

SCREEN_WIDTH            = 1920
SCREEN_HEIGHT           = 1080
NUM_OF_BUTTONS          = 5
BUTTON_COLOR            = (255,255,255)
BUTTON_HOVER_COLOR      = (100,100,100)
BUTTON_ACTIVE_COLOR     = (50,50,50)
BUTTON_FOREGROUND_COLOR = (0,0,0)
BUTTON_WIDTH            = SCREEN_WIDTH // NUM_OF_BUTTONS
BUTTON_HEIGHT           = 50
class BUTTON_STATES(enum.Enum):
  IDLE   = 0
  HOVER  = 1
  ACTIVE = 2
  
results = pd.DataFrame(index = ["1","2","3","4","Refs"],columns = ["Image 1","Image 2","Image 3","Image 4","Image 5"])

def init():
  pygame.init()
  pygame.display.set_caption("Subjective test")
  return pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.FULLSCREEN)

def createButtons():
  # Attributes
  font = pygame.font.Font(None,30)
  
  # Render the font
  b1 = font.render("1",True,BUTTON_FOREGROUND_COLOR)
  b2 = font.render("2",True,BUTTON_FOREGROUND_COLOR)
  b3 = font.render("3",True,BUTTON_FOREGROUND_COLOR)
  b4 = font.render("4",True,BUTTON_FOREGROUND_COLOR)
  b5 = font.render("5",True,BUTTON_FOREGROUND_COLOR)
  # Set the position of the buttons
  bY = SCREEN_HEIGHT - BUTTON_HEIGHT
  b1Pos = (0,bY)
  b2Pos = (BUTTON_WIDTH    ,bY)
  b3Pos = (BUTTON_WIDTH * 2,bY)
  b4Pos = (BUTTON_WIDTH * 3,bY)
  b5Pos = (BUTTON_WIDTH * 4,bY)
  return [[b1Pos,b1,BUTTON_STATES.IDLE],[b2Pos,b2,BUTTON_STATES.IDLE],[b3Pos,b3,BUTTON_STATES.IDLE],[b4Pos,b4,BUTTON_STATES.IDLE],[b5Pos,b5,BUTTON_STATES.IDLE]]

def updateImage(img):
  image = pygame.image.load(f"images/{img}")
  image = pygame.transform.scale(image,(SCREEN_WIDTH,SCREEN_HEIGHT))
  return (image,img)

def loop(screen,img,name,buttons,codec,meanRefs,userID):
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: #or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        print("Test not saved!")
        pygame.quit()
        exit()
      elif event.type == pygame.MOUSEMOTION:
        for button in buttons:
          pos,text,buttonState = button
          if pos[0] < event.pos[0] < pos[0] + BUTTON_WIDTH and pos[1] < event.pos[1] < pos[1] + BUTTON_HEIGHT:
            button[2] = BUTTON_STATES.HOVER
          else:
            button[2] = BUTTON_STATES.IDLE
      elif event.type == pygame.MOUSEBUTTONDOWN:
        for count,button in enumerate(buttons):
          pos,text,buttonState = button
          if pos[0] < event.pos[0] < pos[0] + BUTTON_WIDTH and pos[1] < event.pos[1] < pos[1] + BUTTON_HEIGHT:
            button[2] = BUTTON_STATES.ACTIVE
            updateResults(name,count + 1,meanRefs)
            checkResults(codec,meanRefs,userID)
            img,name = updateImage(chooseNext(name,codec))
          else:
            button[2] = BUTTON_STATES.IDLE
    screen.blit(img,(0,0))
    for button in buttons:
      pos,text,buttonState = button
      pygame.draw.rect(screen,getColorFromState(buttonState),(pos[0],pos[1],BUTTON_WIDTH,BUTTON_HEIGHT))
      screen.blit(text,pos)
    pygame.display.flip()

def getColorFromState(state):
  if state == BUTTON_STATES.IDLE:
    return BUTTON_COLOR
  elif state == BUTTON_STATES.HOVER:
    return BUTTON_HOVER_COLOR
  else:
    return BUTTON_ACTIVE_COLOR

def chooseNext(previousImage,codec):
  if not previousImage:
    return random.choice(MAPPER_REFERENCE[codec])
  imgNum = previousImage[0]
  if "ref" in previousImage:
    newImg = random.choice(MAPPER_CODED[codec][imgNum])
    MAPPER_CODED[codec][imgNum].pop(MAPPER_CODED[codec][imgNum].index(newImg))
    if len(MAPPER_CODED[codec][imgNum]) == 0:
      MAPPER_REFERENCE[codec].pop(MAPPER_REFERENCE[codec].index(f"{imgNum}ref.jpg"))  
  else:
    maxLength    = max([len(value) for value in MAPPER_CODED[codec].values()])
    newReference = [reference for reference in MAPPER_REFERENCE[codec] if len(MAPPER_CODED[codec][reference[0]]) == maxLength]
    newImg = random.choice(newReference)
    while newImg[0] == imgNum:
      newImg = random.choice(newReference)
  return newImg

def updateResults(previousImage,score,meanRefs):
  if not "ref" in previousImage:
    results[f"Image {previousImage[0]}"][previousImage[2]] = score
  else:
    meanRefs[int(previousImage[0]) - 1] += score
    
def checkResults(codec,meanRefs,userID):
  maxLength = max([len(value) for value in CODED_IMAGES_JPG.values()])
  if maxLength == 0:
    meanRefs = [ref / 4 for ref in meanRefs]
    for i in range(1,6):
      results[f"Image {i}"]["Refs"] = meanRefs[i - 1]
    if not os.path.exists(f"results/{userID}"):
      os.makedirs(f"results/{userID}")
    results.to_csv(f"results/{userID}/{codec}Results.csv")
    pygame.quit()
    exit()
    
def main():
  userID = input(f"What is your id?")
  codec  = input(f"Please choose the codec: {[codec for codec in AVAILABLE_CODECS]}")
  while codec not in AVAILABLE_CODECS:
    codec = input(f"Please choose the codec: {[codec for codec in AVAILABLE_CODECS]}")
  screen          = init()
  initialImg,name = updateImage(chooseNext(None,codec))
  buttons         = createButtons()
  meanRefs = [0,0,0,0,0]
  loop(screen,initialImg,name,buttons,codec,meanRefs,userID)
  
if __name__ == "__main__":
  main()