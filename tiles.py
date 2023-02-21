import pygame

from config import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups, surface = pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.image = surface
        #self.rect = self.image.get_rect(topleft = position)
        #self.rect = self.image.fill('white')
        # if flag == 0:
        #     self.rect = self.image.fill('white')
        #     self.rect.topleft = position
        # else:
        self.rect = self.image.get_rect(topleft = position)

        #bug here with tile placement w/ respect to actual bounding box position