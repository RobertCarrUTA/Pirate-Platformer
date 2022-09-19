import pygame
from tiles  import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    # @brief A function for initializing the Enemy
    def __init__(self, size, x, y):
        super().__init__(size, x, y, "../graphics/enemy/run")
        # To stop the enemy from floating above the ground, we need to take the size the enemy covers and lower them based on that.
        #   We can do this by taking the size of the tile (64) and subtracting the height of the enemy image
        #   self.image.get_size()[1] will give us the y value of the image size
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3, 5)

    # @brief A function to make the Enemy move at a random speed
    def move(self):
        self.rect.x += self.speed

    # @brief A function to turn the Enemy in the right direction based on the direction they are moving
    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)
    
    # @brief A function that reverse the direction the Enemy is moving
    def reverse(self):
        self.speed *= -1

    # @brief A function that updates the Enemy
    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate() # From AnimatedTile
        self.move()
        self.reverse_image()
