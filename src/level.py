import pygame
from turtle     import Vec2D
from tiles      import Tile, StaticTile, Crate, Coin, Palm
from settings   import tile_size, screen_width, screen_height
from support    import import_csv_layout, import_cut_graphics
from enemy      import Enemy
from decoration import Sky, Water, Clouds
from player     import Player
from particles  import ParticleEffect

class Level:
    # @brief A function for initializing the Level
    def __init__(self, level_data, surface):
        # Level setup
        self.display_surface = surface
        self.world_shift = 0

        # Player setup
        player_layout   = import_csv_layout(level_data["player"])
        self.player     = pygame.sprite.GroupSingle()
        self.goal       = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Dust setup
        self.dust_sprite = pygame.sprite.GroupSingle()

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

    # @brief A function for changing the direction of the Enemy class
    def enemy_collision_reverse(self):
        # Check all of the enemy sprites and check if any of the sprites are colliding with any of the constraints
        #   if they are, then make them run the other direction
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    # @brief A function for horizontal movement collision
    def horizontal_movement_collision(self):
        player          = self.player.sprite
        player.rect.x   += player.direction.x * player.movement_multiplier_x

        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.foreground_sprites.sprites()

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
        player = self.player.sprite
        player.apply_gravity()
        
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.foreground_sprites.sprites()

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

        # Player sprites
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # Water
        self.water.draw(self.display_surface, self.world_shift)
