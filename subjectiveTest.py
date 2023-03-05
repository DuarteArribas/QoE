import pygame

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

SCREEN_WIDTH   = 1920
SCREEN_HEIGHT  = 1080
NUM_OF_BUTTONS = 5
buttonWidth    = SCREEN_WIDTH // NUM_OF_BUTTONS
buttonHeight   = 50


def init():
  pygame.init()
  pygame.display.set_caption("Subjective test")
  return pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.FULLSCREEN)

def createButtons():
  # Attributes
  font       = pygame.font.Font(None,30)
  color      = (255,255,255)
  # Render the font
  b1 = font.render("1",True,color)
  b2 = font.render("2",True,color)
  b3 = font.render("3",True,color)
  b4 = font.render("4",True,color)
  b5 = font.render("5",True,color)
  # Set the position of the buttons
  bY = SCREEN_HEIGHT - buttonHeight
  b1Pos = (0,bY)
  b2Pos = (buttonWidth    ,bY)
  b3Pos = (buttonWidth * 2,bY)
  b4Pos = (buttonWidth * 3,bY)
  b5Pos = (buttonWidth * 4,bY)  

def updateImage(img):
  image = pygame.image.load(f"images/{img}")
  image = pygame.transform.scale(image,(SCREEN_WIDTH,SCREEN_HEIGHT))
  return image

def loop():
  # Run the game loop
  while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # Draw the image
    screen.blit(image, (0, 0))
    
    # Draw the buttons
    mouse_pos = pygame.mouse.get_pos()
    if button1_pos[0] < mouse_pos[0] < button1_pos[0] + button_width and button1_pos[1] < mouse_pos[1] < button1_pos[1] + button_height:
        pygame.draw.rect(screen, hover_color, pygame.Rect(button1_pos, (button_width, button_height)))
    else:
        pygame.draw.rect(screen, button_color, pygame.Rect(button1_pos, (button_width, button_height)))
    screen.blit(button1, button1_pos)
    
    if button2_pos[0] < mouse_pos[0] < button2_pos[0] + button_width and button2_pos[1] < mouse_pos[1] < button2_pos[1] + button_height:
        pygame.draw.rect(screen, hover_color, pygame.Rect(button2_pos, (button_width, button_height)))
    else:
        pygame.draw.rect(screen, button_color, pygame.Rect(button2_pos, (button_width, button_height)))
    screen.blit(button2, button2_pos)
    
    if button3_pos[0] < mouse_pos[0] < button3_pos[0] + button_width and button3_pos[1] < mouse_pos[1] < button3_pos[1] + button_height:
        pygame.draw.rect(screen, hover_color, pygame.Rect(button3_pos, (button_width, button_height)))
    else:
        pygame.draw.rect(screen, button_color, pygame.Rect(button3_pos, (button_width, button_height)))
    screen.blit(button3, button3_pos)
    
def a():
  # Define the colors of the buttons
  button_color = (255, 255, 255)
  hover_color = (200, 200, 200)

  # Define the font and size of the text on the buttons
  font = pygame.font.Font(None, 30)

  # Create the buttons
  button1 = font.render("Button 1", True, button_color)
  button2 = font.render("Button 2", True, button_color)
  button3 = font.render("Button 3", True, button_color)
  button4 = font.render("Button 4", True, button_color)
  button5 = font.render("Button 5", True, button_color)

  # Set the position of the buttons
  button_width = screen_width // 5
  button_height = 50
  button1_pos = (0, screen_height - button_height)
  button2_pos = (button_width, screen_height - button_height)
  button3_pos = (button_width * 2, screen_height - button_height)
  button4_pos = (button_width * 3, screen_height - button_height)
  button5_pos = (button_width * 4, screen_height - button_height)
    
def main():
  screen = init()
  loop()
  
if __name__ == "__main__":
  main()