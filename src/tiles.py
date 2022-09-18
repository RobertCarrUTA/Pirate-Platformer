import pygame

# Inherits the pygame.sprite.Sprite class
class Tile(pygame.sprite.Sprite):
    # @brief A function for initializing the Tile
    def __init__ (self, size, x, y):
        super().__init__()
        self.image  = pygame.Surface((size, size))
        self.rect   = self.image.get_rect(topleft = (x, y))

    # @brief A function for updating the Tile
    def update(self, x_shift):
        self.rect.x += x_shift

# Inherits the Tile class
#   We want this because a lot of our tiles will share the same attributes
class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface
