import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    # @brief A function for initializing the Player
    def __init__(self, position):
        super().__init__()
        self.import_character_assets() # Importing the animation images
        self.frame_index     = 0
        self.animation_speed = 0.15
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft = position)
        
        # Player Movement
        self.direction              = pygame.math.Vector2(0, 0)     # A vector that allows our player to move - arguments (x, y)
        self.movement_multiplier_x  = 6     # Movement multiplier that multiplies the movement in update(self)
        self.gravity                = 0.8
        self.jump_speed             = -13   # Remember that to move up in the y-direction, it needs to be negative

    # @brief A function for importing all of the character animation frames
    def import_character_assets(self):
        character_path = "graphics/character/"
        # Creating a dictionary of animations: we have a folder with folders named idle, run, jump and fall
        self.animations = {"idle":[], "run":[], "jump":[], "fall":[]}

        # Using our dictionary we can just access the full character path to those files
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    # @brief A function for animating the player
    def animate(self):
        animation = self.animations['run']

        # Loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]

    # @brief A function for getting player input
    def get_input(self):
        # This method of getting input may cause slight delay, look into a more
        # responsive way to get player input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1  # We move in the x direction because right is a movement along the x axis
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1 # We move in the x direction because left is a movement along the x axis
        else:
            # We need to slow the player down to a halt when they stop pressing keys to move
            # This should slow the player down to 0 movement instead of instantly stopping
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.jump()

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
        self.animate()
