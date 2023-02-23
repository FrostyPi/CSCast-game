import pygame

from config import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups, type = 'standard', surface = pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = position)
        if type == 'door':
            self.hitbox = self.rect.inflate(96,96)
