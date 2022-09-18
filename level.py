import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player

class Level:
    # @brief A function for initializing the Level
    def __init__(self, level_data, surface):
        # Level setup
        self.display_surface = surface
        self.setup_level(level_data)

        # Moving the level left or right
        self.world_shift = 0
        self.current_x   = 0

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
                    player_sprite = Player((x, y), self.display_surface)
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
        # Displaying the level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # Displaying the player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
