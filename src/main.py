# This code could be heavily commented, it is for me to learn
# and I want to remember why I did what I did. I have done a bit of
# Pygame already, so comments for those basic things could be found here: https://github.com/RobertCarrUTA/Pixel-Runner-Python/blob/main/run.py

import pygame
import sys                          # Allows for sys.exit()
from settings   import *            # Allows for us to access variables in settings.py
from level      import Level        # Allows us to access the Level class
from overworld  import Overworld
from ui         import UI

class Game:
    # @brief A function for initializing the Game
    def __init__(self):
        # Game Attributes
        self.max_level      = 0
        self.current_health = 100   # Health, max health, and coin amount need to be in the Game class cause Player and Level are created over and over
        self.max_health     = 100   #   Game stays persistent, so it allows us to keep track of these values across levels
        self.coins          = 0

        # Overworld Creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level) # Arguments - (start_level, max_level, surface)
        self.status    = "overworld"

        # User Interface
        self.ui = UI(screen)

    # @brief A function to create the current level from when a player enters it on the Overworld
    def create_level(self, current_level):
        self.level  = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = "level"

    # @brief A function that creates teh overworld based on a player exiting a level
    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld  = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status     = "overworld"

    # @brief A function that updates the current coins held by the player
    def change_coins(self, amount):
        self.coins += amount

    # @brief A function that changes the health of the Player
    def change_health(self, amount):
        self.current_health += amount

    # @brief A function for checking whether the game is over
    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.coins          = 0
            self.max_level      = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level) # Arguments - (start_level, max_level, surface)
            self.status    = "overworld"

    # @brief A function to run the game
    def run(self):
        if self.status == "overworld":
            self.overworld.run()
        else:
            # Possibly add a death screen here
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)   # Arguments: (current_health, full_health)
            self.ui.show_coins(self.coins) # Argument: (amount of coins)
            self.check_game_over()

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
