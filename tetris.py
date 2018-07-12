import sys
import pygame
import random
from pygame.locals import *

# all positions inside the games are represented by this type
class Vector2:
  def __init__(self, x, y):
    self.x=x
    self.y=y

TILE_SIZE=32  # width and height of one tile in screen pixels
TILE_COUNT=Vector2(16, 24) # size of screen in tiles
SCREEN=Vector2(TILE_COUNT.x*TILE_SIZE, TILE_COUNT.y*TILE_SIZE)# size of screen in tiles
FPS=14.0# frames per second

# types of tetris pieces appearing in game
TETROMINOS=[
[[1, 1, 1, 1]]
,
[[1, 0, 0],
 [1, 1, 1]]
,
[[0, 0, 1],
 [1, 1, 1]]
,
[[1, 1],
 [1, 1]]
,
[[0, 1, 1],
 [1, 1, 0]]
,
[[0, 1, 0],
 [1, 1, 1]]
,
[[1, 1, 0],
 [0, 1, 1]]
]

# NES  palette with blacks removed
# each color is a rgb tuple
COLORS=[
  (124,124,124),
  (0,0,252),
  (0,0,188),
  (68,40,188),
  (148,0,132),
  (168,0,32),
  (168,16,0),
  (136,20,0),
  (80,48,0),
  (0,120,0),
  (0,104,0),
  (0,88,0),
  (0,64,88),
  (188,188,188),
  (0,120,248),
  (0,88,248),
  (104,68,252),
  (216,0,204),
  (228,0,88),
  (248,56,0),
  (228,92,16),
  (172,124,0),
  (0,184,0),
  (0,168,0),
  (0,168,68),
  (0,136,136),
  (248,248,248),
  (60,188,252),
  (104,136,252),
  (152,120,248),
  (248,120,248),
  (248,88,152),
  (248,120,88),
  (252,160,68),
  (248,184,0),
  (184,248,24),
  (88,216,84),
  (88,248,152),
  (0,232,216),
  (120,120,120),
  (252,252,252),
  (164,228,252),
  (184,184,248),
  (216,184,248),
  (248,184,248),
  (248,164,192),
  (240,208,176),
  (252,224,168),
  (248,216,120),
  (216,248,120),
  (184,248,184),
  (184,248,216),
  (0,252,252),
  (248,216,248),
]

# "Game Over" text written as blocks array
GAME_OVER_TEXT=[
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0],
[0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0],
[0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0],
[0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
[0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# draw array of blocks on screen
def drawBlocks(display, blocks, position=Vector2(0, 0)):
  for y in range(0,  len(blocks)):
    for x in range(0, len(blocks[y])):
      if blocks[y][x]:
        color=(255,)*3  # default color is white
        if isinstance(blocks[y][x], tuple):  # if block contains color information as tuple use it
          color=blocks[y][x]
        pygame.draw.rect(display, color, tuple(i*TILE_SIZE for i in (x+position.x, y+position.y, 1,1)))

# rotates array of blocks 90 degrees right
def rotate(blocks):
  return list(zip(*blocks[::-1]))

# change color of all blocks inside array
def colorBlocks(blocks, color):
  for y in range(0,  len(blocks)):
    for x in range(0, len(blocks[y])):
      if blocks[y][x]:  # if tile is nonempty change it to color tuple
        blocks[y][x]=color
  return blocks

# move tiles from target to destination array, target array is moved by position vector
def move(target, destination, position):
  for y in range(0,  len(target)):
    for x in range(0, len(target[y])):
      if target[y][x]:
        destination[y+position.y][x+position.x]=target[y][x]
  return destination

# do blocks in both arrays collide, blocks array is moved by position vector
def collision(blocks, board, position):
  if position.x<0 or position.y<0 or position.y+len(blocks)>len(board) or position.x+len(blocks[0])>len(board[0]):  # bounds check
    return True
  for y in range(0, len(blocks)):
    for x in range(0, len(blocks[y])):
      if blocks[y][x] and board[y+position.y][x+position.x]:# check if both blocks and board array on this index are nonempty
        return True
  return False

class Tetris:
  def start(self):# starts game
    self.board = [[0 for x in range(TILE_COUNT.x)] for y in range(TILE_COUNT.y)]  # array containing all not lying
    self.gameOver=False
    self.blockPosition=Vector2(0,0)# position of active block
    self.newBlock()

  def run(self):# initializes pygame and starts game loop
    pygame.init()
    self.start()
    fpsClock = pygame.time.Clock()
    display = pygame.display.set_mode((SCREEN.x, SCREEN.y))
    dt = 1/FPS
    while True:
      for event in pygame.event.get():
        self.handleEvent(event)
      self.update(dt)
      self.draw(display)
      dt = fpsClock.tick(FPS)

  def newBlock(self):# adds new falling and movable block to the game world
    self.block=colorBlocks(random.choice(TETROMINOS), random.choice(COLORS))
    self.blockPosition.x=random.randint(0, TILE_COUNT.x-len(self.block[0]))
    self.blockPosition.y=0
  
  def handleEvent(self, event):
    if event.type == KEYDOWN:
      if self.gameOver:# restart game when any key is pressed
        self.start()
    if event.type == QUIT:# quit game when 'x' button on window is pressed
      pygame.quit()
      sys.exit()

  # check if there's a filled line in the game board, if it exists remove it
  def removedFilledLines(self):
    for y in range(0,  len(self.board)):
      hole=False# is any hole present in the line
      for x in range(0, len(self.board[y])):
        if not self.board[y][x]:
          hole=True
          break
      if not hole:
          self.removeLine(y)

  def removeLine(self, height):
    for y in range(height, 0, -1):
      self.board[y]=self.board[y-1]
  
  def update(self, dt):
    if not self.gameOver:
      keys=pygame.key.get_pressed()
      newX=self.blockPosition.x
      newY=self.blockPosition.y+1
      if newY>TILE_COUNT.y-len(self.block):# felt on the ground
        self.board=move(self.block, self.board, self.blockPosition)
        self.removedFilledLines()
        self.newBlock()
        return
      else:
        if keys[K_UP]:
          rotatedBlock=rotate(self.block)
          if not collision(rotatedBlock, self.board, self.blockPosition):  # check if block after rotating would collide with rest
            self.block=rotatedBlock  # rotate the block
        if keys[K_LEFT] and not collision(self.block, self.board, Vector2(newX-1, newY)):
          newX -= 1
        if keys[K_RIGHT] and not collision(self.block, self.board, Vector2(newX+1, newY)):
          newX += 1
        if collision(self.block, self.board, Vector2(newX, newY)):# felt on the other block
          if newY<=1:
            self.gameOver=True
          else:
            self.board=move(self.block, self.board, Vector2(self.blockPosition.x, self.blockPosition.y))
            self.removedFilledLines()
            self.newBlock()
        else:  
          self.blockPosition=Vector2(newX, newY)
 
  def draw(self, display):
    display.fill((0, 0, 0))
    drawBlocks(display, self.board)
    drawBlocks(display, self.block, self.blockPosition)
    if self.gameOver:
      drawBlocks(display, GAME_OVER_TEXT)
    pygame.display.flip()

if __name__ == "__main__":
  Tetris().run()