# This code could be heavily commented, it is for me to learn
# and I want to remember why I did what I did. I have done a bit of
# Pygame already, so comments for those basic things could be found here: https://github.com/RobertCarrUTA/Pixel-Runner-Python/blob/main/run.py

import pygame
import sys                          # Allows for sys.exit()
from settings   import *            # Allows for us to access variables in settings.py
from overworld  import Overworld
from level      import Level

class Game:
    def __init__(self):
        self.max_level = 2 # Remember, level number starts at 0, then goes 1, 2, 3, etc. So level 3 is 4 levels
        self.overworld = Overworld(0, self.max_level, screen) # Arguments - start_level, max_level, surface)
        self.level = Level(1, screen)

    def run(self):
        self.level.run()

pygame.init()
pygame.display.set_caption("Platformer") 
screen          = pygame.display.set_mode((screen_width, screen_height))
clock           = pygame.time.Clock()
game            = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill("black")
    game.run()

    pygame.display.update()
    clock.tick(60)
