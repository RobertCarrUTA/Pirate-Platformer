import pygame

class Tile(pygame.sprite.Sprite):
    # @brief A function for initializing the Tile
    def __init__ (self, position, size):
        super().__init__()
        self.image  = pygame.Surface((size, size))
        self.image.fill("grey")
        self.rect   = self.image.get_rect(topleft = position)

    # @brief A function for updating the Tile
    def update(self, x_shift):
        self.rect.x += x_shift
