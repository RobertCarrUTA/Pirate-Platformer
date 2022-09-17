import pygame
from tiles import Tile
from settings import tile_size

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

        for row_index, row in enumerate(layout): # enumerate() lets us know what row we are on
            for col_index, cell in enumerate(row):
                # If we find a cell in the row that has X, add a tile to that cell
                if cell == "X":
                    x    = col_index * tile_size
                    y    = row_index * tile_size
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
