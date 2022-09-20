import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        self.image.fill("red")
        self.rect = self.image.get_rect(center = position)

class Overworld:
    def __init__(self, start_level, max_level, surface):
        # Setup
        self.display_surface = surface
        self.max_level       = max_level
        self.current_level   = start_level

        # Sprites
        self.setup_nodes()

    # @brief A function that goes through the node positions in game_data.py
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        
        for node_data in levels.values():
            node_sprite = Node(node_data["node_position"])
            self.nodes.add(node_sprite)

    def run(self):
        self.nodes.draw(self.display_surface)
