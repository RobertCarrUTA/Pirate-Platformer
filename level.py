import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player

class Level:
    def __init__(self, level_data, surface):
        
        # Level setup
        self.display_surface = surface
        self.setup_level(level_data)

        # Moving the level left or right
        self.world_shift = 0

    # A function that draws our tiles anywhere it finds an X in level_map
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout): # enumerate() lets us know what row we are on
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                # If we find a cell in the row that has X, add a tile to that cell
                if cell == "X":
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                # If we find a cell in the row that has P, add a player sprite to that cell
                if cell == "P":
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
    
    # Scroll the level in the x direction
    def scroll_x(self):
        player      = self.player.sprite    # Lets us know of the player
        player_x    = player.rect.centerx   # Lets us know where the player is located
        direction_x = player.direction.x    # Lets us know what direction the player is going to move

        # If they player is moving out of the left side of the screen
        #
        # To simulate the background moving as a camera following the player, we need to shift the world by the players movement speed, and set the player
        # movement to 0. This makes it look like a camera is following them. We do "if player_x < (screen_width / 4) and direction_x < 0" because if we just
        # did "if player_x < (screen_width / 4)" we would never get out of that condition and we would scroll left forever. direction_x < 0 means we are moving
        # to the left. (screen_width / 4) allows the scrolling to be applied to any screen width and says if the player is within a quarter of the screen width
        # to the leftmost edge of the window
        if player_x < (screen_width / 4) and direction_x < 0:
            self.world_shift = player.movement_multiplier_x # player.movement_multiplier_x is defined in the Player class
            player.speed = 0
        # TODO: When the player goes to the right of the screen, it keeps going until the player moves back outside of the 
        elif player_x > (screen_width - (screen_width / 4)) and direction_x > 0:
            self.world_shift = -player.movement_multiplier_x
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = player.movement_multiplier_x

    def run(self):
        # Displaying the level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        # Displaying the player
        self.player.update()
        self.player.draw(self.display_surface)
        self.scroll_x()
