import pygame
from turtle     import Vec2D
from tiles      import Tile, StaticTile, Crate, Coin, Palm
from settings   import tile_size, screen_width, screen_height
from support    import import_csv_layout, import_cut_graphics
from enemy      import Enemy
from decoration import Sky, Water, Clouds
from player     import Player
from particles  import ParticleEffect
from game_data  import levels

class Level:
    # @brief A function for initializing the Level
    def __init__(self, current_level, surface, create_overworld, change_coins):
        # Level setup
        self.display_surface = surface
        self.world_shift     = 0
        self.current_x       = None

        # Overworld connection
        self.create_overworld   = create_overworld
        self.current_level      = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data["unlock"]

        # Player setup
        player_layout   = import_csv_layout(level_data["player"])
        self.player     = pygame.sprite.GroupSingle()
        self.goal       = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # User Interface
        self.change_coins = change_coins

        # Dust setup
        self.dust_sprite        = pygame.sprite.GroupSingle()
        self.player_on_ground   = False

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
        self.sky    = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water  = Water(screen_height - 40, level_width)
        self.clouds = Clouds(400, level_width, 30)

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
                            sprite = Coin(tile_size, x, y, "../graphics/coins/gold", 5)
                        else:
                            sprite = Coin(tile_size, x, y, "../graphics/coins/silver", 1)
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
                    x       = col_index * tile_size
                    y       = row_index * tile_size
                    sprite  = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                if val == "1": # "0" represents the goal
                    x           = col_index * tile_size
                    y           = row_index * tile_size
                    hat_surface = pygame.image.load("../graphics/character/hat.png").convert_alpha()
                    sprite      = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)                

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

    # @brief A function for changing the direction of the Enemy class
    def enemy_collision_reverse(self):
        # Check all of the enemy sprites and check if any of the sprites are colliding with any of the constraints
        #   if they are, then make them run the other direction
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    # @brief A function for horizontal movement collision
    def horizontal_movement_collision(self):
        player              = self.player.sprite
        player.rect.x       += player.direction.x * player.speed
        collidable_sprites  = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.foreground_sprites.sprites()

        # Testing for all the possible sprites we could collide with (crates, foreground palm trees, coins)
        for sprite in collidable_sprites:
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
        player              = self.player.sprite
        collidable_sprites  = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.foreground_sprites.sprites()
        player.apply_gravity()

        # Testing for all the possible sprites we could collide with (crates, foreground palm trees, coins)
        for sprite in collidable_sprites:  
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
        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    # @brief A function that checks if the player fell off the screen
    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    # @brief A function that checks if the player won by collecting the hat
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    # @brief A function that checks for coin collisions between the player
    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True) # In case a player hits two coins at one time
        if collided_coins:
            for coin in collided_coins:
                self.change_coins(coin.value)

    # @brief A function for running the Level
    def run(self):

        # Sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # Background palm tiles
        self.background_sprites.update(self.world_shift)
        self.background_sprites.draw(self.display_surface)

        # Terrain tiles
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # Enemy tiles
        self.enemies_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift) # These exist but cannot be seen, they allow us to change the direction of the Enemy class
        self.enemy_collision_reverse()
        self.enemies_sprites.draw(self.display_surface)

        # Crate tiles
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # Grass tiles
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # Coin tiles
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # Palm tiles
        self.foreground_sprites.update(self.world_shift)
        self.foreground_sprites.draw(self.display_surface)

        # Dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # Player sprites
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.check_death()
        self.check_win()
        self.check_coin_collisions()

        # Water
        self.water.draw(self.display_surface, self.world_shift)
