import pygame

class Player(pygame.sprite.Sprite):
    # @brief A function for initializing the Player
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = position)
        
        # Player Movement
        self.direction              = pygame.math.Vector2(0, 0)     # A vector that allows our player to move - arguments (x, y)
        self.movement_multiplier_x  = 6     # Movement multiplier that multiplies the movement in update(self)
        self.gravity                = 0.8
        self.jump_speed             = -13   # Remember that to move up in the y-direction, it needs to be negative

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
        self.apply_gravity()
