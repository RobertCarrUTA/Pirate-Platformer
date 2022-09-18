import pygame
from turtle import Vec2D
from particles import ParticleEffect
from tiles import Tile, StaticTile
from settings import tile_size, screen_width
from player import Player 
from support import import_csv_layout, import_cut_graphics

class Level:
    # @brief A function for initializing the Level
    def __init__(self, level_data, surface):
        # Level setup
        self.display_surface = surface
        self.setup_level(level_data)

        # Terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # Moving the level left or right
        self.world_shift = 0
        self.current_x   = 0

        # Dust
        self.dust_sprite      = pygame.sprite.GroupSingle()
        self.player_on_ground = False

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

    # @brief A function that creates the jump particles
    def create_jump_particles(self, position):
        if self.player.sprite.facing_right:
            position -= pygame.math.Vector2(10, 5)
        else:
            position -= pygame.math.Vector2(10, -5)

        jump_particle_sprite = ParticleEffect(position, "jump")
        self.dust_sprite.add(jump_particle_sprite)

    # @brief A function to determine weather a player is on the ground
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    # @brief A function to create the landing dust particles
    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(fall_dust_particle)

    # @brief A function that draws our tiles anywhere it finds an X in level_map
    def setup_level(self, layout):
        self.tiles  = pygame.sprite.Group()
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
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(player_sprite)
    
    # @brief A function that scrolls the level in the x direction based on player position
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

    # @brief A function for horizontal movement collision
    def horizontal_movement_collision(self):
        player          = self.player.sprite
        player.rect.x   += player.direction.x * player.movement_multiplier_x

        # Testing for all the possible tiles we could collide with
        for sprite in self.tiles.sprites():
            # The is player colliding with the rectangle of a tile
            if sprite.rect.colliderect(player.rect): # Using .colliderect() rather than .spritecollide() makes this easier
                
                # In Pygame we cannot directly detect where the collision is taking place, so to work around this we have to
                #   separate our collision and movement into vertical and horizontal movements as well as collisions.
                #
                # To do this we use the below if condition. If we detect a the player colliding with a rectangle of a tile,
                #   we can use the direction of the player to determine if the collision is happening on the left or the right.
                #   Lets say we detect a collision while the player is moving left, after that we need to move the player to the
                #   right side of the obstacle it collided with. This will allow us to work around this issue in Pygame.
                
                if player.direction.x < 0:      # Player is moving left and is colliding with the wall to the left
                    player.rect.left    = sprite.rect.right
                    player.on_left      = True
                    self.current_x      = player.rect.left
                elif player.direction.x > 0:     # Player is moving right and is colliding with the wall to the right
                    player.rect.right   = sprite.rect.left
                    player.on_right     = True
                    self.current_x      = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):   # If the player is touching a wall to the left and stopped moving to the left
            player.on_left  = False                                                             #   or moving to the right, we know we are not touching the left wall anymore
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0): # If the player is touching a wall to the right and stopped moving to the left
            player.on_right = False                                                             #   or moving to the right, we know we are not touching the right wall anymore
    
    # @brief A function for vertical movement collision
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():             # Testing for all the possible tiles we could collide with
            if sprite.rect.colliderect(player.rect):    # The is player colliding with the rectangle of a tile
                if player.direction.y > 0:              # Player is moving downward
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0              # We need to cancel gravity increasing if we are standing on top of a tile
                    player.on_ground = True
                elif player.direction.y < 0:            # Player is moving upward
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0              # Make the player fall back down if we hit a ceiling
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1: # If the player is jumping or falling, the player cannot be on the floor anymore
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0: # If the player is falling, they are no longer on the ceiling
            player.on_ceiling = False

    # @brief A function for running the Level
    def run(self):
        # Displaying the dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # Displaying the level tiles
        self.tiles.update(self.world_shift)
        self.terrain_sprites.draw(self.world_shift)
        self.scroll_x()

        # Displaying the player
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)

        # Displaying the dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # Displaying the level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # Displaying the player
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)
