import pygame
from tiles import AnimatedTile

class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, "../graphics/enemy/run")
        # To stop the enemy from floating above the ground, we need to take the size the enemy covers and lower them based on that.
        #   We can do this by taking the size of the tile (64) and subtracting the height of the enemy image
        #   self.image.get_size()[1] will give us the y value of the image size
        self.rect.y += size - self.image.get_size()[1]
