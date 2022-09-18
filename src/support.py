import pygame
from os import walk     # Used in import_folder()
from csv import reader  # Used in import_csv_layout()

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

