import pygame

class UI:
    def __init__(self, surface):
        # Setup
        self.display_surface = surface

        # Health
        self.health_bar = pygame.image.load("../graphics/ui/health_bar.png").convert_alpha()


        # Coins
        self.coin      = pygame.image.load("../graphics/ui/coin.png").convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (50, 61))
        self.font      = pygame.font.Font("../graphics/ui/ARCADEPI.TTF", 30)


    # @brief A function that shows the health of the player
    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar, (20, 10))

    # @brief A function to show how many coins the player has
    def show_coins(self, amount):
        # Unlike the health bar (where we can just place it somewhere in the top left of the screen),
        #   the coins and the text displaying the number of coins have to have the same center position
        #   so they are displayed nicely next to each other. We need to track where the center of these two are.
        #   Using rectangles, this will be easy. We want to get the middle of the right side of the coin image,
        #   then go a few pixels right, and place the text there by using the left middle side of the text rectangle
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surface = self.font.render(str(amount), False, "#33323d")
        coin_amount_rect    = coin_amount_surface.get_rect(midleft = (self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surface, coin_amount_rect)
