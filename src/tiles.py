import pygame
from support import import_folder

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
#   The StaticTile does not move, it has no animations
class StaticTile(Tile):
    # @brief A function for initializing the StaticTile
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

# Inherits the StaticTile class
#   This is because a crate does not move, so it will share the attributes of StaticTile
class Crate(StaticTile):
    # @brief A function for initializing the Crate
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load("../graphics/terrain/crate.png").convert_alpha())

        # We need to give an offset so the tile is not floating above the ground.
        #   Remember our tiles are 64x64
        offset_y  = y + size
        self.rect = self.image.get_rect(bottomleft = (x, offset_y))

# Inherits the Tile class but contains additional attributes that make the Tile animated
class AnimatedTile(Tile):
    # @brief A function for initializing the AnimatedTile
    def __init__(self, size, x, y, path): # Now that we have multiple images, we now need a path to loop over those images
        super().__init__(size, x, y)
        self.frames      = import_folder(path)
        self.frame_index = 0
        self.image       = self.frames[self.frame_index]
    
    # @brief A function that animates the AnimatedTile
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    # @brief A function that updates the animation of AnimatedTile and makes sure the Tile shifts with the simulated camera
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift

# At this point, what is happening with each class is probably clear
class Coin(AnimatedTile):
    # @brief A function for initializing the Coin
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        center_x   = x + int(size / 2) # We have a 64x64 square, find the middle by (size/2), then add x to it to get the center of the square
        center_y   = y + int(size / 2)
        self.rect  = self.image.get_rect(center = (center_x, center_y))
        self.value = value

class Palm(AnimatedTile):
    # @brief A function for initializing the Palm
    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        offset_y          = y - offset
        self.rect.topleft = (x, offset_y)
