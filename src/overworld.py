import pygame
from game_data  import levels
from support    import import_folder
from decoration import Sky

# @brief A class that shows the level nodes in the Overworld
class Node(pygame.sprite.Sprite):
    # @brief A function for initializing the Node
    def __init__(self, position, status, icon_speed, path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
        # Showing which levels are available and which aren't
        if status == "available":
            self.status = "available"
        else:
            self.status = "locked"
        
        self.rect = self.image.get_rect(center = position)

        # detection_node is used for us to have collision detection with the center of a Node
        #   The below pygame.Rect() has to be relative to the speed because if we go too fast, we could skip the detection zone entirely
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2), self.rect.centery - (icon_speed / 2), icon_speed, icon_speed)

    # @brief A function that animates the Node
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    # @brief A function for updating the Node
    def update(self):
        if self.status == "available":
            self.animate()
        else:
            tint_surface = self.image.copy()
            tint_surface.fill("black", None, pygame.BLEND_RGB_MULT)
            self.image.blit(tint_surface, (0, 0))

# @brief A class that shows the player icon in the Overworld
class Icon(pygame.sprite.Sprite):
    # @brief A function for initializing the Icon
    def __init__(self, position):
        super().__init__()
        self.position   = position
        self.image      = pygame.image.load("../graphics/overworld/hat.png").convert_alpha()
        self.rect       = self.image.get_rect(center = position)

    # @brief A function for updating the Icon
    def update(self):
        self.rect.center = self.position # This allows us to have the right position of the center of the rectangle (with doubles, not int's)

# @brief A class that  
class Overworld:
    # @brief A function for initializing the Overworld
    def __init__(self, start_level, max_level, surface, create_level):
        # Setup
        self.display_surface = surface
        self.max_level       = max_level
        self.current_level   = start_level
        self.create_level    = create_level

        # Movement logic
        self.moving         = False
        self.speed          = 8
        self.move_direction = pygame.math.Vector2(0, 0)

        # Sprites
        self.setup_nodes()
        self.setup_icon()
        self.sky = Sky(8, "overworld")

        # Time
        self.start_time   = pygame.time.get_ticks()
        self.allow_input  = False
        self.timer_length = 350 # Milliseconds

    # @brief A function that goes through the node positions in game_data.py
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        # We need to loop over our dictionaries and look for the node positions.
        #   If we find a node that is above or max_level, we want to grey it out.
        #   index allows us to do this easily.
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data["node_position"], "available", self.speed, node_data["node_graphics"])
            else:
                node_sprite = Node(node_data["node_position"], "locked", self.speed, node_data["node_graphics"])
            self.nodes.add(node_sprite)

    # @brief A function that draws the paths between levels in the Overworld
    def draw_paths(self):
        if self.max_level > 0:
            # We need list comprehension that gets the node positions if they are below max_level, and draws lines between them if they are below max_level
            points = [node["node_position"] for index, node in enumerate(levels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, "#A04F45", False, points, 6) # Arguments - (surface, color, fill, points, line_width)

    # @brief A function that displays the Icon on the current level
    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    # @brief A function that allows the Icon to move between the levels
    def input(self):
        keys = pygame.key.get_pressed()

        # I want to note 2 issues with the movement before they were fixed. This is for me to remember so I am going to put it down.
        # 
        # 1. The issue is if we press right, Pygame sees the first level node, then we go straight to the next level node really fast.
        #       So our Icon movement will be something close to the last vector we needed in the path to move to that node.
        #       To fix this, we have to make sure that we are stopping our keyboard input once we reach the next level node.
        #
        #       So if we put our keyboard input if statements inside another if that checks for if the icon is moving, we can fix this.
        # 
        # 2. The second issue is that if we fix issue #1, our Icon still misses the center of the rectangle that represented the level we are moving to.
        #       This is because in Pygame, rect's are represented by int's, not doubles. The position of a rect would look something like
        #       (100, 150). If we do get_movement_data() and it needs to go to (100.2, 150.5), it can't, so it will miss the center.
        #       In the line, self.move_direction = self.get_movement_data(), two doubles are returned. So of move_direction is (0.7, 1.2),
        #       Pygame will convert it to (0, 1) to represent the position of a rectangle because rectangles are represented by ints in Pygame
        #    
        #       So to fix this, we create a new Icon attribute called self.position. This will be in the form of doubles. We use it in update_icon_position().
        #       We use self.icon.sprite.position inside the function to allow us to get the position in the form of two doubles instead of two ints. We then
        #       do self.rect.center = self.position inside of update() in the Icon class. This allows us to have the right position of the center of the rectangle
        #       (with doubles, not int's). So then this issue is now fixed cause we can now move exactly to the point we want to move to.
        #           [self.icon.sprite.position += self.move_direction * self.speed] vs [sprite.rect.center += self.move_direction * self.speed], former is more precise
        #
        if not self.moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level: # If the player is on max_level, they shouldn't be able to go right
                self.move_direction = self.get_movement_data("next")
                self.current_level += 1
                self.moving         = True # We are moving along a path to another level node
            elif keys[pygame.K_LEFT] and self.current_level > 0:             # If the player is on level 0, they shouldn't be able to go left
                self.move_direction = self.get_movement_data("previous")
                self.current_level -= 1
                self.moving         = True
            elif keys[pygame.K_SPACE]:  # User presses space in the Overworld and goes into that level
                self.create_level(self.current_level)

    # @brief A function that determines the arrow the Icon has to move to the next level
    def get_movement_data(self, target):
        start   = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center) # Look at the center of the Icon, set it to one of the current nodes, which once is determined by the current level
        if target == "next":
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        # Just to explain what is happening here, for example, the end node is position (300, 220) and the start node is (110, 400).
        #   We subtract the end from the start, (300, 220) - (110, 400) and get (190, -180). This is the vector we use to move.
        #   We just want the direction, so we have to normalize the vector.
        return (end - start).normalize()

    # @brief A function to update the Icon position
    def update_icon_position(self):
        if self.moving and self.move_direction:
            self.icon.sprite.position += self.move_direction * self.speed # Using position from Icon allows us to get the position in the form of two doubles instead of two ints
            target_node = self.nodes.sprites()[self.current_level]

            # This blocks the Icon from moving forever, it stops once it reaches the center of the level node it moves to
            if target_node.detection_zone.collidepoint(self.icon.sprite.position):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    # @brief A function that determines the time until a player can input in the Overworld
    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True

    # @brief A function for running the Overworld
    def run(self):
        self.input_timer()
        self.input()
        self.update_icon_position()
        self.icon.update()
        self.nodes.update()

        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
