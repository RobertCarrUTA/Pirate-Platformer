import pygame

class UI:
    # @brief A function for initializing the UI
    def __init__(self, surface):
        # Setup
        self.display_surface = surface

        # Health
        self.health_bar           = pygame.image.load("../graphics/ui/health_bar.png").convert_alpha()
        self.health_bar_topleft   = (54, 39) # Actually have to find the top left of the health bar, if you move the health bar, you have to move this
        self.health_bar_max_width = 152      # The health bar is 152 pixels wide
        self.health_bar_height    = 4        # The health bar is 4 pixels tall

        # Coins
        self.coin      = pygame.image.load("../graphics/ui/coin.png").convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (50, 61))
        self.font      = pygame.font.Font("../graphics/ui/ARCADEPI.TTF", 30)

    # @brief A function that shows the health of the player
    def show_health(self, current_health, full_health):
        # Displaying the health bar PNG image
        self.display_surface.blit(self.health_bar, (20, 10))
        
        # Displaying a health bar on top of the PNG image
        current_health_ratio     = current_health / full_health
        current_health_bar_width = self.health_bar_max_width * current_health_ratio
        health_bar_rect          = pygame.Rect((self.health_bar_topleft), (current_health_bar_width, self.health_bar_height))
        pygame.draw.rect(self.display_surface, "#dc4949", health_bar_rect)

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
