import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (20, 20)

from pygame import *
import random

init()
size = width, height = 800, 600
screen = display.set_mode(size)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (24, 176, 34)
BLUE = (14, 133, 237)

# Text font
menuFont = font.SysFont("Times New Roman",40)
ScoreMenu = font.SysFont("Times New Roman", 30)
HighScoreMenu = font.SysFont("Times New Roman", 70)
ScoreFont = font.SysFont("Times New Roman", 20)

#states in the Game
STATE_MENU = 0
STATE_GAME = 1
STATE_HELP = 2
STATE_QUIT = 3

# Images
Runningpic = image.load("Running1.png")
Runningpic2 = image.load("Running2.png")
Flyingpic = image.load("Flying.png")
Laserpicture = image.load("Laser1.png")
Laserpic = transform.scale(Laserpicture, (70, 125))
Deathpic1 = image.load("Dead1.png")
Deathpic2 = image.load("Dead2.png")
Viruspicture = image.load("ComputerVirusImage.png")
Viruspic = transform.scale(Viruspicture, (20, 20))
VirsuWarninigpicture = image.load("RocketWarning.png")
VirsuWarninigpic = transform.scale(VirsuWarninigpicture, (40, 40))
Backgroundpic = image.load("MatrixBackground.png")
GameOverpicture= image.load("GameOver.png")
GameOverpic= transform.scale(GameOverpicture, (250, 250))
Controlspicture = image.load("Controls.png")
Controlspic = transform.scale(Controlspicture, (850, 600))
GameNamepic = image.load("GameTittle.png")

# Functions
# Draws character Running
def DrawRunning1(screen):
    Running = (50, 450, Runningpic.get_width(), Runningpic.get_height())
    screen.blit(Runningpic, Running)

    # Creates rectangle to act as character hit box
    HitBox = Rect(70, 465, Runningpic.get_width() - 55, Runningpic.get_height() - 10)
    return HitBox

# Draws character Running
def DrawRunning2(screen):
    Running2 = (50, 450, Runningpic2.get_width(), Runningpic2.get_height())
    screen.blit(Runningpic2, Running2)

    # Creates rectangle to act as character hit box
    HitBox = Rect(70, 465, Runningpic.get_width() - 55, Runningpic.get_height() - 10)
    return HitBox

# Draws character Flying
def DrawFlying(screen, y):
    Flying = (50, y, Flyingpic.get_width(), Flyingpic.get_height())
    screen.blit(Flyingpic, Flying)

    # Creates rectangle to act as character hit box
    HitBox = Rect(75, y + 15, Flyingpic.get_width() - 45, Flyingpic.get_height() - 25)
    return HitBox

# Draws stationary Laser
def DrawLaser(screen):  # Draws numerous stationary laser obstacles /// Used code form Multiple Missiles in a List, on google doc file: Example Game Code Reference ///
    global LaserListX, LaserListY, LaserTime, ScrollSpeed
    Obstacles = []
    for i in range(len(LaserListX) - 1, -1, -1):
        LaserX = LaserListX[i]
        LaserY = LaserListY[i]

        # Draws Laser Image
        Laser = (LaserX, LaserY, Laserpic.get_width(), Laserpic.get_height())
        screen.blit(Laserpic, Laser)

        LaserListX[i] -= ScrollSpeed

        if LaserListX[i] < -20:
            del LaserListX[i]
            del LaserListY[i]
        else:
            Obstacle = Rect(LaserX + 20, LaserY + 15, 15, 90)
            Obstacles.append(Obstacle)

    if time.get_ticks() - LaserTime >= GenerationRate:
        LaserListX.append(800)
        LaserTime = time.get_ticks()
        LaserY = random.randint(0, 450)
        LaserListY.append(LaserY)

    return Obstacles

# Draws moving Missile
def DrawMissile(screen):  # Draws numerous moving missile obstacles /// Used code form Multiple Missiles in a List, on google doc file: Example Game Code Reference ///
    global MissileListX, MissileListY, MissileTime
    Obstacles2 = []  # VR - always start empty, that's how we had so many
    for i in range(len(MissileListX) - 1, -1, -1):
        MissileX = MissileListX[i]
        MissileY = MissileListY[i]

        # Draws incoming virus warning
        if MissileX > 770:
          VirsuWarninig = (760, MissileY + 12, VirsuWarninigpic.get_width(), VirsuWarninigpic.get_height())
          screen.blit(VirsuWarninigpic, VirsuWarninig)

        # Draws Virus      
        Virus = (MissileX + 17, MissileY + 12, Viruspic.get_width(), Viruspic.get_height())
        screen.blit(Viruspic, Virus)

        MissileListX[i] -= 10
      
        if MissileListX[i] < -15:
            del MissileListX[i]
            del MissileListY[i]
        else:
            Obstacle = Rect(MissileX + 20, MissileY + 15, 15, 15)
            Obstacles2.append(Obstacle)

    if time.get_ticks() - MissileTime >= 2000:
        MissileListX.append(1500)
        MissileTime = time.get_ticks()
        MissileY = random.randint(0, 525)
        MissileListY.append(MissileY)
  
    return Obstacles2

# Draws Background image
def DrawBackground(screen):
    Background = (0, 0, Backgroundpic.get_width(), Backgroundpic.get_height())
    screen.blit(Backgroundpic, Background)
    draw.rect(screen, GREEN, (0, 540, 800, 125))

# Draws 'Game Over' graphic and player score information
def DrawGameOver(screen, Score, HighScore):
    # 'Game Over' graphic
    GameOver = (265, 130, GameOverpic.get_width(), GameOverpic.get_height())
    screen.blit(GameOverpic, GameOver)
    # Checks for new highscore
    if Score > HighScore:
      numFile = open ("highscore.dat", "w")
      Score = int(Score)
      numFile.write(str(Score)) 
      numFile.close()
      HighScore = Score
    # Displays player and highscore
    draw.rect(screen, BLACK, (240, 335, 325, 25))
    text = ScoreFont.render("Your Score: %i High Score: %i" % (Score, HighScore), True, (BLUE))
    screen.blit(text, (240, 335, 50, 50))

# Function to draw main menue
def DrawMenu(screen, button, mx, my, state, HighScore): # /// Used code form Creating a Menu, on google doc file: Example Game Code Reference ///
  blockWidth = width//3
  blockHeight = height//7    
  rectList = [Rect(blockWidth - 150, blockHeight, blockWidth, blockHeight), # game choice
              Rect(blockWidth - 200, 3*blockHeight, blockWidth, blockHeight), #help choice
              Rect(blockWidth - 150, 5*blockHeight, blockWidth, blockHeight)] # quite choice
  stateList = [STATE_GAME, STATE_HELP, STATE_QUIT]
  titleList = ["Play Game", "Controls", "Close Game"]
  draw.rect(screen, BLACK, (0, 0, width, height))
  
  for i in range(len(rectList)):
    rect = rectList[i] # get the current Rect
    draw.rect(screen, GREEN, rect)  # draw the Rect
    text = menuFont.render(titleList[i] , 1, BLACK)	# make the font
    textWidth, textHeight = menuFont.size(titleList[i]) # get the font size
    useW = (blockWidth - textWidth)//2  #use for centering
    useH = (blockHeight - textHeight)//2
    # getting a centered Rectangle
    textRect = Rect(rect[0] + useW, rect[1] + useH, textWidth, textHeight)
    screen.blit(text, textRect)	# draw to screen

    # Displays highscroce in circle
    draw.circle(screen, GREEN, (550, 300), 150)
    ScoreHeader = ScoreMenu.render("HighScore: " , 1, BLACK)
    Circle = Rect(460, 220, 5,5)
    screen.blit(ScoreHeader, (Circle))

    Score = HighScoreMenu.render("%i" % (HighScore), 1, BLACK)
    ScoreWidth = Score.get_width()/2
    Circle = Rect(550 - ScoreWidth, 280, 5,5)
    screen.blit(Score, (Circle))

    # Displays Game Name
    GameName = (25, 8, GameNamepic.get_width(), GameNamepic.get_height())
    screen.blit(GameNamepic, GameName)
    
    if rect.collidepoint(mx, my):
      draw.rect(screen, WHITE, rect, 2)
      if button == 1:
        state = stateList[i]
  return state

# Function to draw controls
def DrawControls(screen, button, mx, my, state):
  screen.fill(BLACK)
  # Displays image with game controls
  Controls = (10, -30, Controlspic.get_width(), Controlspic.get_height())
  screen.blit(Controlspic, Controls)

  # Code for back to menu button
  rect = Rect(0, 5, 60, 25)
  draw.rect(screen, GREEN, (0, 5, 60, 25))
  text = ScoreFont.render("Back", True, (BLACK))
  screen.blit(text, (5, 5, 60, 25))
  if rect.collidepoint(mx, my):
    draw.rect(screen, WHITE, rect, 2)
    if button == 1:
      state = STATE_MENU
  return state

running = True
myClock = time.Clock()
# initializing variables
state = STATE_MENU
mx = my = 0

# Game Loop ------------------------------
while running:
  # File system that stores and reads current highscore
  numFile = open("highscore.dat", "r")
  HighScore = numFile.readline()
  HighScore = int(HighScore)
  numFile.close()
  
  button = 0
  for e in event.get():
      if e.type == QUIT:
          running = False
      if e.type == MOUSEBUTTONDOWN:
          mx, my = e.pos          
          button = e.button
      elif e.type == MOUSEMOTION:
          mx, my = e.pos          
          
  if state == STATE_MENU: # Draws main menu screen              
      state = DrawMenu(screen, button, mx, my, state, HighScore)
  
  elif state == STATE_GAME: # Draws game screen
    # initializing variables for game
    Playing = True
    RunningFrame = 1
    Fly = False
    y = 450
    myClock = time.Clock()
    Timer = 0
    Score = 0
    
    ScoreCount = time.get_ticks()
    RunningTime = time.get_ticks()
    RunCount = 0
    
    # initializing variables for Laser function
    LaserTime = time.get_ticks()
    LaserListX = []
    LaserY = random.randint(0, 500)
    LaserListY = [LaserY]
    Obstacles = []
    ScrollSpeed = 3
    GenerationRate = 2000
    
    # initializing variables for missile function
    MissileTime = time.get_ticks()
    MissileListX = []
    MissileY = random.randint(0, 500)
    MissileListY = [MissileY]
    Obstacles2 = []

    while Playing == True:
      # Creates background and initial obstacles
      DrawBackground(screen)
      Obstacles = DrawLaser(screen)
  
      # score keeper
      Timer += 1
      Score = Timer/60
  
      # Displays Score at top right of screen
      draw.rect(screen, BLACK, (675, 10, 125, 20))
      text = ScoreFont.render("Score: %i" % (Score), True, (WHITE))
      screen.blit(text, (675, 10, 50, 50))
  
      # increases game difficulty based off player score
      if Score >= 30:
        Obstacles2 = DrawMissile(screen)
      if Score >= 60:
        ScrollSpeed = 5
        GenerationRate = 1750
      if Score >= 100:
        ScrollSpeed = 7
        GenerationRate = 1500
      if Score >= 150:
        GenerationRate = 1000
  
      # games gravity physics
      if Fly == False:
        y += 3
        if y < 450:
          Hitbox = DrawFlying(screen, y)
        if y >= 450:
          y = 450
          # Character Running Animation
          if RunningFrame == 1:
            Hitbox = DrawRunning1(screen)
            RunCount += 1
            if RunCount == 10:
              RunningFrame = 2
              RunCount = 0
          elif RunningFrame == 2:
            Hitbox = DrawRunning2(screen)
            RunCount += 1
            if RunCount == 10:
              RunningFrame = 1
              RunCount = 0
  
      # games jumping physics
      if Fly == True:
        Hitbox = DrawFlying(screen, y)
        y -= 3
        if y < -10:
          y = -10

      display.flip()
      myClock.tick(60)
      
      # Collision detection and Death Animations
      if Hitbox.collidelist(Obstacles) > -1:
        DrawBackground(screen)
        Dead2 = (60, y, Deathpic2.get_width(), Deathpic2.get_height())
        screen.blit(Deathpic2, Dead2)
        DrawLaser(screen)
        DrawMissile(screen)
        DrawGameOver(screen, Score, HighScore)
        display.flip()
        time.wait(2500)
        Playing = False
  
      if Hitbox.collidelist(Obstacles2) > -1:
        DrawBackground(screen)
        Dead1 = (60, y, Deathpic1.get_width(), Deathpic1.get_height())
        screen.blit(Deathpic1, Dead1)
        DrawLaser(screen)
        DrawMissile(screen)
        DrawGameOver(screen, Score, HighScore)
        display.flip()
        time.wait(2500)
        Playing = False
      
      # input events -----------------------------
      for evnt in event.get():
        if evnt.type == QUIT:
          running = False

        # determines weather space is pressed
        if evnt.type == KEYDOWN:
          if evnt.key == K_SPACE:
            Fly = True

        if evnt.type == KEYUP:
          if evnt.key == K_SPACE:
            Fly = False
    
    state = STATE_MENU

  elif state == STATE_HELP: # Draws controls screen
    state = DrawControls(screen, button, mx, my, state)
    
  else:
      running = False
      
  display.flip()
  myClock.tick(60)
quit()
