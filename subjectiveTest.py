import pygame
import random
import enum
import os
import pandas as pd
from screeninfo import get_monitors
from enum import Enum

AVAILABLE_CODECS     = ["jpg","jpg2000"]
IMAGES_DIR           = "images"
REFERENCE_IMAGES_DIR = "References"
CODED_DIRS           = {
  "jpg"     : "JPG",
  "jpg2000" : "JPG2000",
  "av1"     : "AV1"
}
BITRATE_DIRS         = {
  "1" : "bitrate-1",
  "2" : "bitrate-2",
  "3" : "bitrate-3",
  "4" : "bitrate-4"
}
CODEC_EXTENSION_MAP = {
  "jpg"     : "jpg",
  "jpg2000" : "png",
  "av1"     : "png"
}

GameState = Enum("GameState","FirstTimeReference Reference FirstTimeCoded Coded")
ButtonStates = Enum("ButtonStates","Idle Hover Active")

WAIT_TIME           = 3000
WAIT_TIME_BLANK     = 1500

SCREEN_WIDTH            = 1920
SCREEN_HEIGHT           = 1080
NUM_OF_BUTTONS          = 5
SCREEN_COLOR            = (120,120,120)
BUTTON_COLOR            = (255,255,255)
BUTTON_HOVER_COLOR      = (70,70,70)
BUTTON_ACTIVE_COLOR     = (50,50,50)
BUTTON_FOREGROUND_COLOR = (0,0,0)
TEXT_COLOR              = (255,255,255)
BUTTON_WIDTH            = SCREEN_WIDTH // NUM_OF_BUTTONS
BUTTON_HEIGHT           = 50
    
def getUserID():
  temp = input(f"What is your id?")
  while temp == "":
    temp = input(f"What is your id?")
  return temp
  
def getDebug():
  temp = input(f"Debug mode? (y/n)")
  while temp not in ("y","n"):
    temp = input(f"Debug mode? (y/n)")
  return temp == "y"  
  
def getCodec():
  temp = input(f"Please choose the codec: {[codec for codec in AVAILABLE_CODECS]}")
  while temp not in AVAILABLE_CODECS:
    temp = input(f"Invalid codec! Please choose the codec: {[codec for codec in AVAILABLE_CODECS]}")
  return temp

def getNumImgs():
  temp = input(f"How many images?: ")
  while not checkInt(temp):
    temp = input(f"How many images?: ")
  return int(temp)

def checkInt(str):
  try:
    _ = int(str)
    return True
  except Exception:
    return False
    
def getReferenceImgs(numOfImgs):
  return [f"{IMAGES_DIR}/{REFERENCE_IMAGES_DIR}/{imgNum}.png" for imgNum in range(1,numOfImgs + 1)]

def getCodedImgs(numOfImgs,codec):
  keys   =  [str(imgNum) for imgNum in range(1,numOfImgs + 1)]
  values =  [f"{IMAGES_DIR}/{CODED_DIRS[codec]}/{BITRATE_DIRS[str(bitrate)]}" for bitrate in range(1,5)]
  codedImgs = {}
  for i in range(numOfImgs):
    codedImgs[keys[i]] = [f"{values[j]}/{i + 1}.{CODEC_EXTENSION_MAP[codec]}" for j in range(4)]
    codedImgs[keys[i]].append(f"{IMAGES_DIR}/{REFERENCE_IMAGES_DIR}/{i + 1}.{CODEC_EXTENSION_MAP[codec]}")
  return codedImgs
  
def init(id):
  pygame.init()
  pygame.display.set_caption(f"Subjective test for user {id}")
  mainMonitor = get_monitors()[0]
  width  = mainMonitor.width
  height = mainMonitor.height
  return (pygame.display.set_mode((width,height),pygame.FULLSCREEN),width,height)

def updateImage(img):
  image = pygame.image.load(img)
  return (image,img)

def chooseNext(previousImage,refImgs,codedImgs,isRef):
  if not previousImage:
    return random.choice(refImgs)
  imgNum = getImgNumFromPath(previousImage)
  if isRef:
    newImg = random.choice(codedImgs[imgNum])
    codedImgs[imgNum].pop(codedImgs[imgNum].index(newImg))
    if len(codedImgs[imgNum]) == 0:
      for count,refImg in enumerate(refImgs):
        if getImgNumFromPath(newImg) == getImgNumFromPath(refImg):
          refImgs.pop(count)
          break
  else:
    maxLength    = max([len(value) for value in codedImgs.values()])
    newReference = [reference for reference in refImgs if len(codedImgs[getImgNumFromPath(reference)]) == maxLength]
    newImg       = random.choice(newReference)
    while getImgNumFromPath(newImg) == imgNum:
      newImg = random.choice(newReference)
  return newImg
  
def getImgNumFromPath(img):
  return os.path.basename(img).split(".")[0]

def createButtons():
  font     = pygame.font.Font(None,30)
  b1       = font.render("1",True,BUTTON_FOREGROUND_COLOR)
  b2       = font.render("2",True,BUTTON_FOREGROUND_COLOR)
  b3       = font.render("3",True,BUTTON_FOREGROUND_COLOR)
  b4       = font.render("4",True,BUTTON_FOREGROUND_COLOR)
  b5       = font.render("5",True,BUTTON_FOREGROUND_COLOR)
  bNext    = font.render("Continue",True,BUTTON_FOREGROUND_COLOR)
  bY       = SCREEN_HEIGHT - BUTTON_HEIGHT
  bYNext   = SCREEN_HEIGHT - 2 * BUTTON_HEIGHT
  b1Pos    = (0               ,bY)
  b2Pos    = (BUTTON_WIDTH    ,bY)
  b3Pos    = (BUTTON_WIDTH * 2,bY)
  b4Pos    = (BUTTON_WIDTH * 3,bY)
  b5Pos    = (BUTTON_WIDTH * 4,bY)
  bNextPos = (BUTTON_WIDTH * 3.5,bYNext)
  return [[b1Pos,b1,ButtonStates.Idle],[b2Pos,b2,ButtonStates.Idle],[b3Pos,b3,ButtonStates.Idle],[b4Pos,b4,ButtonStates.Idle],[b5Pos,b5,ButtonStates.Idle],[bNextPos,bNext,ButtonStates.Idle]]

def loop(screen,img,name,buttons,codec,userID,gameState,refImgs,codedImgs,prevCoded,debug,results,isRef):
  while True:
    screen.fill(SCREEN_COLOR)
    if gameState == GameState.FirstTimeReference:
      screen.blit(img,(0,0))
      drawText(screen,"Reference Image",30,30,80,(255,255,255),(0,0,0))
      pygame.display.update()
      if not debug:
        pygame.time.wait(WAIT_TIME)
      gameState = GameState.Reference
    elif gameState == GameState.Reference:
      screen.blit(img,(0,0))
      drawText(screen,"Reference Image",30,30,80,(255,255,255),(0,0,0))
      for event in pygame.event.get():
        if event.type == pygame.QUIT: #or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
          print("Test not saved!")
          pygame.quit()
          exit()
        elif event.type == pygame.MOUSEMOTION:
          pos,text,buttonState = buttons[5]
          if pos[0] < event.pos[0] < pos[0] + BUTTON_WIDTH and pos[1] < event.pos[1] < pos[1] + BUTTON_HEIGHT:
            buttons[5][2] = ButtonStates.Hover
          else:
            buttons[5][2] = ButtonStates.Idle
        elif event.type == pygame.MOUSEBUTTONDOWN:
          pos,text,buttonState = buttons[5]
          if pos[0] < event.pos[0] < pos[0] + BUTTON_WIDTH and pos[1] < event.pos[1] < pos[1] + BUTTON_HEIGHT:
            buttons[2][2] = ButtonStates.Active
            if prevCoded:
              gameState = GameState.Coded
            else:
              gameState = GameState.FirstTimeCoded
              prevCoded = True
            img,name = updateImage(chooseNext(name,refImgs,codedImgs,isRef))
            isRef = not isRef
          else:
            buttons[2][2] = ButtonStates.Idle
      pos,text,buttonState = buttons[5]
      pygame.draw.rect(screen,getColorFromState(buttonState),(pos[0],pos[1],BUTTON_WIDTH,BUTTON_HEIGHT))
      screen.blit(text,pos)
      pygame.display.update()
    elif gameState == GameState.FirstTimeCoded:
      pygame.display.update()
      if not debug:
        pygame.time.wait(WAIT_TIME_BLANK)
      gameState = GameState.Coded  
    elif gameState == GameState.Coded:
      screen.blit(img,(0,0))
      drawText(screen,"Coded Image. Rate it in a 1-5 scale according to the reference image",30,30,50,(255,255,255),(0,0,0))
      if debug:
        drawText(screen,f"Current image: {name}",30,100,50,(255,255,255),(0,0,0))  
      for event in pygame.event.get():
        if event.type == pygame.QUIT: #or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
          print("Test not saved!")
          pygame.quit()
          exit()
        elif event.type == pygame.MOUSEMOTION:
          for i in range(5):
            pos,text,buttonState = buttons[i]
            if pos[0] < event.pos[0] < pos[0] + BUTTON_WIDTH and pos[1] < event.pos[1] < pos[1] + BUTTON_HEIGHT:
              buttons[i][2] = ButtonStates.Hover
            else:
              buttons[i][2] = ButtonStates.Idle
        elif event.type == pygame.MOUSEBUTTONDOWN:
          for i in range(5):
            pos,text,buttonState = buttons[i]
            if pos[0] < event.pos[0] < pos[0] + BUTTON_WIDTH and pos[1] < event.pos[1] < pos[1] + BUTTON_HEIGHT:
              buttons[i][2] = ButtonStates.Active
              gameState = GameState.FirstTimeReference
              updateResults(results,name,i + 1)
              checkResults(results,codedImgs,codec,userID)
              img,name = updateImage(chooseNext(name,refImgs,codedImgs,isRef))
              isRef = not isRef
              prevCoded = False
            else:
              buttons[i][2] = ButtonStates.Idle
      for i in range(5):
        pos,text,buttonState = buttons[i]
        pygame.draw.rect(screen,getColorFromState(buttonState),(pos[0],pos[1],BUTTON_WIDTH,BUTTON_HEIGHT))
        screen.blit(text,pos)
      pygame.display.update()

def getColorFromState(state):
  if state == ButtonStates.Idle:
    return BUTTON_COLOR
  elif state == ButtonStates.Hover:
    return BUTTON_HOVER_COLOR
  else:
    return BUTTON_ACTIVE_COLOR

def drawText(surface,text,x,y,fontSize,fontColor,bgColor):
  font = pygame.font.Font(None,fontSize)
  textSurface = font.render(text,True,fontColor)
  paddingValue = 10
  bgRect = pygame.Rect(x - paddingValue,y - paddingValue,textSurface.get_width() + 2 * paddingValue,textSurface.get_height() + 2 * paddingValue)
  pygame.draw.rect(surface,bgColor,bgRect)
  surface.blit(textSurface,(x,y))

def updateResults(results,previousImage,score):
  if "References" in previousImage:
    results[f"Image {getImgNumFromPath(previousImage)}"]["Image Reference"] = score
  else:
    results[f"Image {getImgNumFromPath(previousImage)}"][previousImage.split("/")[2]] = score

def checkResults(results,codedImgs,codec,userID):
  maxLength = max([len(value) for value in codedImgs.values()])
  if maxLength == 0:
    if not os.path.exists(f"subjective_results/{userID}"):
      os.makedirs(f"subjective_results/{userID}")
    results.to_csv(f"subjective_results/{userID}/{codec}Results.csv")
    pygame.quit()
    exit()
    
def main():
  userID              = getUserID()
  debug               = getDebug()
  codec               = getCodec()
  numImgs             = getNumImgs()
  results             = pd.DataFrame(index = ["bitrate-1","bitrate-2","bitrate-3","bitrate-4","Image Reference"],columns = [f"Image {imgNum}" for imgNum in range(1,numImgs + 1)])
  refImgs             = getReferenceImgs(numImgs)
  codedImgs           = getCodedImgs(numImgs,codec)
  screen,width,height = init(userID)
  initialImg,name     = updateImage(chooseNext(None,refImgs,codedImgs,False))
  buttons             = createButtons()
  gameState           = GameState.FirstTimeReference
  loop(screen,initialImg,name,buttons,codec,userID,gameState,refImgs,codedImgs,False,debug,results,True)
  
if __name__ == "__main__":
  main()