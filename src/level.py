import pygame
from turtle import Vec2D
from tiles import Tile, StaticTile, Crate, Coin, Palm
from settings import tile_size, screen_width
from support import import_csv_layout, import_cut_graphics

class Level:
    # @brief A function for initializing the Level
    def __init__(self, level_data, surface):
        # Level setup
        self.display_surface = surface
        self.world_shift = -1

        # Terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # Grass setup
        grass_layout = import_csv_layout(level_data["grass"])
        self.grass_sprites = self.create_tile_group(grass_layout, "grass")

        # Crates setup
        crate_layout = import_csv_layout(level_data["crates"])
        self.crate_sprites = self.create_tile_group(crate_layout, "crates")

        # Coin setup
        coin_layout = import_csv_layout(level_data["coins"])
        self.coin_sprites = self.create_tile_group(coin_layout, "coins")

        # Foreground palm setup
        foreground_palm_layout = import_csv_layout(level_data["foreground palms"])
        self.foreground_sprites = self.create_tile_group(foreground_palm_layout, "foreground palms")


    # @brief A function to create Tile groups
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):   # Use enumerate to track the index of each row
            for col_index, val in enumerate(row):
                if val != "-1": # When terrain_layout is imported, all the numbers are strings
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "terrain":
                        terrain_tile_list   = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
                        tile_surface        = terrain_tile_list[int(val)] # Selecting the right tile based on what value we are currently looping over
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == "grass":
                        grass_tile_list     = import_cut_graphics('../graphics/decoration/grass/grass.png')
                        tile_surface        = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == "crates":
                        sprite = Crate(tile_size, x, y) # There is no image to split up
                    if type == "coins":
                        if val == "0":
                            sprite = Coin(tile_size, x, y, "../graphics/coins/gold")
                        else:
                            sprite = Coin(tile_size, x, y, "../graphics/coins/silver")
                    if type == "foreground palms":
                        sprite = Palm(tile_size, x, y, "../graphics/terrain/palm_small")

                    sprite_group.add(sprite)

        return sprite_group

    # @brief A function for running the Level
    def run(self):

        # Displaying the terrain tiles
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # Displaying the grass tiles
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # Displaying the crate tiles
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # Displaying the coin tiles
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # Foreground palm setup
        self.foreground_sprites.update(self.world_shift)
        self.foreground_sprites.draw(self.display_surface)


