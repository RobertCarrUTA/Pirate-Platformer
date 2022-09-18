import pygame
from os import walk

# @brief import an animation folder and return the images back as a list
def import_folder(path):
    surface_list = []

    for _, _, img_files in walk(path): # _'s indicate we don't care about what is being returned in that part, we don't care about directory path or subfolders
        for image in img_files:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)

    return surface_list
