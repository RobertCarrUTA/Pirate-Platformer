import pygame
from turtle import Vec2D
from tiles import Tile, StaticTile
from settings import tile_size, screen_width
from support import import_csv_layout, import_cut_graphics

class Level:
    # @brief A function for initializing the Level
    def __init__(self, level_data, surface):
        # Level setup
        self.display_surface = surface

        # Terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # Moving the level left or right
        self.world_shift = -1
        self.current_x   = 0

    # @brief A function to create Tile groups
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        print(layout)

        for row_index, row in enumerate(layout):   # Use enumerate to track the index of each row
            for col_index, val in enumerate(row):
                if val != "-1": # When terrain_layout is imported, all the numbers are strings
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "terrain":
                        terrain_tile_list   = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
                        print(terrain_tile_list[int(val)])
                        tile_surface        = terrain_tile_list[int(val)] # Selecting the right tile based on what value we are currently looping over
                        sprite              = StaticTile(tile_size, x, y, tile_surface)
                    
                    sprite_group.add(sprite)

        return sprite_group

    # @brief A function for running the Level
    def run(self):

        # Displaying the level tiles
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)