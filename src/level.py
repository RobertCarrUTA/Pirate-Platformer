import pygame
from turtle import Vec2D
from tiles import Tile, StaticTile, Crate, Coin, Palm
from settings import tile_size, screen_width
from support import import_csv_layout, import_cut_graphics
from enemy import Enemy
from decoration import Sky

class Level:
    # @brief A function for initializing the Level
    def __init__(self, level_data, surface):
        # Level setup
        self.display_surface = surface
        self.world_shift = -3

        # Player setup
        player_layout   = import_csv_layout(level_data["player"])
        self.player     = pygame.sprite.GroupSingle()
        self.goal       = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Terrain setup
        terrain_layout          = import_csv_layout(level_data["terrain"])
        self.terrain_sprites    = self.create_tile_group(terrain_layout, "terrain")

        # Grass setup
        grass_layout        = import_csv_layout(level_data["grass"])
        self.grass_sprites  = self.create_tile_group(grass_layout, "grass")

        # Crates setup
        crate_layout        = import_csv_layout(level_data["crates"])
        self.crate_sprites  = self.create_tile_group(crate_layout, "crates")

        # Coin setup
        coin_layout         = import_csv_layout(level_data["coins"])
        self.coin_sprites   = self.create_tile_group(coin_layout, "coins")

        # Foreground palm setup
        foreground_palm_layout  = import_csv_layout(level_data["foreground palms"])
        self.foreground_sprites = self.create_tile_group(foreground_palm_layout, "foreground palms")

        # Background palm setup
        background_palm_layout  = import_csv_layout(level_data["background palms"])
        self.background_sprites = self.create_tile_group(background_palm_layout, "background palms")

        # Enemies setup
        enemy_layout            = import_csv_layout(level_data["enemies"])
        self.enemies_sprites    = self.create_tile_group(enemy_layout, "enemies")

        # Constraint setup
        constraint_layout       = import_csv_layout(level_data["constraints"])
        self.constraint_sprites = self.create_tile_group(constraint_layout, "constraints")

        # Decoration setup
        self.sky = Sky(8)

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
                        if val == "0":
                            sprite = Palm(tile_size, x, y, "../graphics/terrain/palm_small", 38)
                        if val == "1":
                            sprite = Palm(tile_size, x, y, "../graphics/terrain/palm_large", 64)
                    if type == "background palms":
                        sprite = Palm(tile_size, x, y, "../graphics/terrain/palm_bg", 64)
                    if type == "enemies":
                        sprite = Enemy(tile_size, x, y)
                    if type == "constraints":
                        sprite = Tile(tile_size, x, y) # Being a Tile doesn't matter because it will not be shown to the player

                    sprite_group.add(sprite)

        return sprite_group

    # @brief A function to set up the player and the end goal for the player
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):   # Use enumerate to track the index of each row
            for col_index, val in enumerate(row):
                if val == "0": # "0" represents the player
                    x = col_index * tile_size
                    y = row_index * tile_size
                if val == "1": # "0" represents the goal
                    x           = col_index * tile_size
                    y           = row_index * tile_size
                    hat_surface = pygame.image.load("../graphics/character/hat.png").convert_alpha()
                    sprite      = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)                

    # @brief A function for changing the direction of the Enemy class
    def enemy_collision_reverse(self):
        # Check all of the enemy sprites and check if any of the sprites are colliding with any of the constraints
        #   if they are, then make them run the other direction
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    # @brief A function for running the Level
    def run(self):

        # Displaying the sky
        self.sky.draw(self.display_surface)

        # Displaying the background palm tiles
        self.background_sprites.update(self.world_shift)
        self.background_sprites.draw(self.display_surface)

        # Displaying the terrain tiles
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # Displaying the enemy tiles
        self.enemies_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift) # These exist but cannot be seen, they allow us to change the direction of the Enemy class
        self.enemy_collision_reverse()
        self.enemies_sprites.draw(self.display_surface)

        # Displaying the crate tiles
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # Displaying the grass tiles
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # Displaying the coin tiles
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # Displaying the foreground palm tiles
        self.foreground_sprites.update(self.world_shift)
        self.foreground_sprites.draw(self.display_surface)

        # Displaying the player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
