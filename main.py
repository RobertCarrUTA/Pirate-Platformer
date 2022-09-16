# This code could be heavily commented, it is for me to learn
# and I want to remember why I did what I did. I have done a bit of
# Pygame already, so comments for those basic things could be found here: https://github.com/RobertCarrUTA/Pixel-Runner-Python/blob/main/run.py

import pygame
import sys              # Allows for sys.exit()
from settings import *  # Allows for us to access variables in settings.py

pygame.init()
screen          = pygame.display.set_mode((screen_width, screen_height))
clock           = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill("black")

    pygame.display.update()
    clock.tick(60)
