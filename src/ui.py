import pygame

class UI:
    def __init__(self, surface):
        # Setup
        self.display_surface = surface

        # Health
        self.health_bar = pygame.image.load("../graphics/ui/health_bar.png").convert_alpha()


        # Coins
        self.coin = pygame.image.load("../graphics/ui/coin.png").convert_alpha()

    # @brief A function that shows the health of the player
    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar, (20, 10))

    # @brief A function to show how many coins the player has
    def show_coins(self, amount):
        pass


