from turtle import position
import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    # @brief A function for initializing the Player
    def __init__(self, position, surface, create_jump_particles):
        super().__init__()
        self.import_character_assets() # Importing the animation images
        self.frame_index        = 0
        self.animation_speed    = 0.15
        self.image              = self.animations["idle"][self.frame_index]
        self.rect               = self.image.get_rect(topleft = position)
        
        # Dust particles
        self.import_dust_run_particles()        # Importing the dust run particles
        self.dust_frame_index        = 0
        self.dust_animation_speed    = 0.15
        self.display_surface         = surface  # surface is passed inside level.py in setup_level()
        self.create_jump_particles = create_jump_particles

        # Player movement
        self.direction              = pygame.math.Vector2(0, 0)     # A vector that allows our player to move - arguments (x, y)
        self.movement_multiplier_x  = 6     # Movement multiplier that multiplies the movement in update(self)
        self.gravity                = 0.8
        self.jump_speed             = -16   # Remember that to move up in the y-direction, it needs to be negative

        # Player status
        self.status         = "idle"
        self.facing_right   = True  # Player defaults to face right, gets changed in get_input() in player.py based on player movement
        self.on_ground      = False # Determined in level.py during vertical_movement_collision()
        self.on_ceiling     = False # Determined in level.py during vertical_movement_collision()
        self.on_left        = False # Determined in level.py during horizontal_movement_collision()
        self.on_right       = False # Determined in level.py during horizontal_movement_collision()

    # @brief A function for importing all of the character animation frames
    def import_character_assets(self):
        character_path = "graphics/character/"
        # Creating a dictionary of animations: we have a folder with folders named idle, run, jump and fall
        self.animations = {"idle":[], "run":[], "jump":[], "fall":[]}

        # Using our dictionary we can just access the full character path to those files
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    # @brief A function to import the running dust particle animation frames
    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder("graphics/character/dust_particles/run/")

    # @brief A function for animating the player
    def animate(self):
        animation = self.animations[self.status]

        # Loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image   = pygame.transform.flip(image, True, False) # Arguments - (surface, do you want to flip it horizontally, do you want to flip it vertically)
            self.image      = flipped_image
        
        # Set the player rectangle
        #   This stops our player from levitating on the floor. This happens because our animations without this can have the wrong origin point.
        #       The animations can be different sizes, so each surface has a different dimension but our rect stays the same. Pygame alsways puts the surface on
        #       the top left point of the rect, so it will look like the animation is floating a little bit.
        #
        #   We combat this by finding out what the player is colliding with, on_ground, etc., the we create a new rect on a new animation frame and set the
        #       origin point to the collision point. We do the latter below.
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        # Collisions with the ceiling
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    # @brief A function to animate the dust animations when the player is running
    def run_dust_animation(self):
        if self.status == "run" and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                position = self.rect.bottomleft - pygame.math.Vector2(6, 10) # Spawn the dust particles on the bottom left of the player
                self.display_surface.blit(dust_particle, position)
            else:
                position = self.rect.bottomright - pygame.math.Vector2(6, 10) # Spawn the dust particles on the bottom left of the player
                flipped_dust_image   = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_image, position)

    # @brief A function for getting player input
    def get_input(self):
        # This method of getting input may cause slight delay, look into a more
        # responsive way to get player input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x    = 1         # We move in the x direction because right is a movement along the x axis
            self.facing_right   = True      # We have hit the right key, so we are now facing right
        elif keys[pygame.K_LEFT]:
            self.direction.x    = -1        # We move in the x direction because left is a movement along the x axis
            self.facing_right   = False     # We have hit the left key, so we are now facing left
        else:
            # We need to slow the player down to a halt when they stop pressing keys to move
            # This should slow the player down to 0 movement instead of instantly stopping
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_ground: # Only allow the player to jump while on the ground
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    # @brief A function to get the status of the player (are they jumping, running, falling, etc.?)
    def get_status(self):
        # Just to do a brief overview of the logic here, we can find out the following states:
        #   Jumping: We know a player is jumping when their direction.y is negative
        #   Falling: We know a player is falling when their direction.y is positive
        #   Running: We know a player is running when their direction.x is not 0
        #   Idle:    We know a player is idle when both direction.x and direction.y are 0
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1: # We do > 1 because our player is never really has direction.y = 0, this is because our
            self.status = "fall"   # player is always being moved back on top of the tile if they are standing on it
        else:
            if self.direction.x != 0:
                self.status = "run"
            else:
                self.status = "idle"

    # @brief A function for applying gravity to the player
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y      += self.direction.y

    # @brief A function that allows the player to jump
    def jump(self):
        self.direction.y = self.jump_speed

    # @brief A function for updating the player
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
