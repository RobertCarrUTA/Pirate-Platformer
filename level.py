import pygame
from tiles import Tile

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)

    # A function that draws our tiles anywhere it finds an X in level_map
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()

        for row in layout:
            print(row)

    def run(self):
        self.tiles.draw(self.display_surface)
