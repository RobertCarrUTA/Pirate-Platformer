from re import X
import pygame
from settings import vertical_tile_number, tile_size, screen_width

class Sky:
    # @brief A function to initialize the Sky
    def __init__(self, horizon):
        #super().__init__
        self.top     = pygame.image.load("../graphics/decoration/sky/sky_top.png").convert()
        self.bottom  = pygame.image.load("../graphics/decoration/sky/sky_bottom.png").convert()
        self.middle  = pygame.image.load("../graphics/decoration/sky/sky_middle.png").convert()
        self.horizon = horizon # At what point do we want to switch between the tiles?

        # Stretch tiles
        self.top    = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))

    # @brief A function to draw the sky
    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            surface.blit(self.top, (0, y))
