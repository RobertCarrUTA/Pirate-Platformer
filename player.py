import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = position)
        self.direction = pygame.math.Vector2(0, 0) # A vector that allows our player to move - arguments (x, y)
    
        # Movement multipliers that multiply the movement in update(self)
        self.movement_multiplier_x = 6
        self.movement_multiplier_y = 6

    def get_input(self):
        # This method of getting input may cause slight delay, look into a more
        # responsive way to get player input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1  # We move in the x direction because right is a movement along the x axis
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1 # We move in the x direction because left is a movement along the x axis
        elif keys[pygame.K_UP]:
            self.direction.y = -1 # We move in the y direction because up is a movement along the y axis   - -1 moves up
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1  # We move in the y direction because down is a movement along the y axis - 1 moves up
        else:
            # We need to slow the player down to a halt when they stop pressing keys to move
            # This should slow the player down to 0 movement instead of instantly stopping
            if self.direction.y > 0:
                self.direction.y -= 0.1
            if self.direction.y < 0:
                self.direction.y += 0.1
            if self.direction.x > 0:
                self.direction.x -= 0.1
            if self.direction.x < 0:
                self.direction.x += 0.1

    def update(self):
        self.get_input()
        self.rect.x += self.direction.x * self.movement_multiplier_x
        self.rect.y += self.direction.y * self.movement_multiplier_y
