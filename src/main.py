# This code could be heavily commented, it is for me to learn
# and I want to remember why I did what I did. I have done a bit of
# Pygame already, so comments for those basic things could be found here: https://github.com/RobertCarrUTA/Pixel-Runner-Python/blob/main/run.py

import pygame
import sys                          # Allows for sys.exit()
from settings   import *            # Allows for us to access variables in settings.py
from level      import Level        # Allows us to access the Level class
from game_data  import level_0      # Allows us to use the data from our exported level_0 on Tiled

pygame.init()
pygame.display.set_caption("Platformer") 
screen          = pygame.display.set_mode((screen_width, screen_height))
clock           = pygame.time.Clock()
level           = Level(level_0, screen) # This allows us to load different levels as arguments very easily

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill("grey")
    level.run()

    pygame.display.update()
    clock.tick(60)
