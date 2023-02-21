import pygame
import math
from config import *



class Item(pygame.sprite.Sprite):
    def __init__(self, groups, type, position):
        super().__init__(groups)
        # self.game = game
        # self.player = player

        self.image = pygame.image.load(f'graphics/items/{type}.png')
        self.rect = self.image.get_rect(topleft = (position[0] * TILE_SIZE, position[1] * TILE_SIZE))
