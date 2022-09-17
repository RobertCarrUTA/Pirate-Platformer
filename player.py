import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = position)
        self.direction = pygame.math.Vector2(0, 0) # A vector that allows our player to move - arguments (x, y)
    
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

    def update(self):
        self.get_input()
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y
