import pygame
from settings   import screen_width, screen_height
from game_data  import levels


class Level:
    # @brief A function for initializing the Level
    def __init__(self, current_level, surface):
        # Level setup
        self.display_surface = surface
        self.current_level = current_level
        level_data = levels[current_level]
        level_content = level_data["content"]
        self.new_max_level = level_data["unlock"]

        # Level display
        self.font = pygame.font.Font(None, 40)
        self.text_surface = self.font.render(level_content, True, "White")
        self.text_rect = self.text_surface.get_rect(center = (screen_width / 2, screen_height / 2))

    def run(self):
        self.display_surface.blit(self.text_surface, self.text_rect)
