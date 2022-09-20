import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):
    def __init__(self, position, status):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        
        # Showing which levels are available and which aren't
        if status == "available":
            self.image.fill("red")
        else:
            self.image.fill("grey")
        
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
        
        # We need to loop over our dictionaries and look for the node positions.
        #   If we find a node that is above or max_level, we want to grey it out.
        #   index allows us to do this easily.
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data["node_position"], "available")
                self.nodes.add(node_sprite)
            else:
                self.nodes.add(node_sprite)
                node_sprite = Node(node_data["node_position"], "locked")

    # @brief A function that draws the paths between levels in the Overworld
    def draw_paths(self):
        # We need list comprehension that gets the node positions if they are below max_level
        points = [node["node_position"] for node in levels.values()]
        pygame.draw.lines(self.display_surface, "red", False, points, 6) # Arguments - (surface, color, fill, points, line_width)

    def run(self):
        self.nodes.draw(self.display_surface)
        self.draw_paths()
