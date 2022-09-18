import pygame
from os import walk
from csv import reader          # Used in import_csv_layout()
from settings import tile_size  # Used in import_cut_graphic()

# @brief Import an animation folder and return the images back as a list
def import_folder(path):
    surface_list = []

    for _, _, img_files in walk(path): # _'s indicate we don't care about what is being returned in that part, we don't care about directory path or subfolders
        for image in img_files:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list

# @brief Import the CSV layout of a level
def import_csv_layout(path):
    terrain_map = []

    with open(path) as map:
        level = reader(map, delimiter = ",")    # Arguments - (csv, delimiter)
        for row in level:
            terrain_map.append(list(row))       # Putting row as a list makes it easier for us
        
        return terrain_map

# @brief A function for cutting a tile image into separate tiles as they would appear on Tiled
def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)
    cut_tiles = []

    # This for loop cuts our tiles into pieces like they would be in Tiled
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x           = col * tile_size
            y           = row * tile_size
            new_surface = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))  # We use (0, 0), because we always want to put the graphic on the top left of the new surface
            cut_tiles.append(new_surface)
    
    return cut_tiles
