# This code could be heavily commented, it is for me to learn
# and I want to remember why I did what I did. I have done a bit of
# Pygame already, so comments for those basic things could be found here: https://github.com/RobertCarrUTA/Pixel-Runner-Python/blob/main/run.py

import pygame
import sys                          # Allows for sys.exit()
from settings   import *            # Allows for us to access variables in settings.py
from level      import Level        # Allows us to access the Level class
from game_data  import level_0      # Allows us to use the data from our exported level_0 on Tiled
from overworld  import Overworld

class Game:
    def __init__(self):
        self.max_level  = 1 # Remember, level number starts at 0, then goes 1, 2, 3, etc. So level 3 is 4 levels
        self.overworld  = Overworld(1, self.max_level, screen, self.create_level) # Arguments - start_level, max_level, surface)
        self.status     = "overworld"

    # @brief A function to create the current level from when a player enters it on the Overworld
    def create_level(self, current_level):
        self.level  = Level(current_level, screen, self.create_overworld)
        self.status = "level"

    # @brief A function that creates teh overworld based on a player exiting a level
    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld  = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status     = "overworld"

    def run(self):
        if self.status == "overworld":
            self.overworld.run()
        else:
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
    
    screen.fill("grey")
    game.run()

    pygame.display.update()
    clock.tick(60)
