import pygame
from player import *
from config import *


class YCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surf = pygame.display.get_surface()
        self.camera_set = pygame.math.Vector2(100, 200)

        self.floor_surf = pygame.Surface((5120, 2880)) #self.floor_surf = pygame.image.load('graphics/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))
    
    def new_draw(self, player):

        self.camera_set.y = player.rect.centery - HALF_HEIGHT
        self.camera_set.x = player.rect.centerx - HALF_WIDTH

        self.floor_rect_offset = self.floor_rect.topleft - self.camera_set
        self.display_surf.blit(self.floor_surf, self.floor_rect_offset)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): #centery
            if "Player" in str(sprite):
                camera_set_pos = sprite.rect.topleft - self.camera_set       # can perhaps try to optimise this
            else: 
                camera_set_pos = sprite.rect.topleft - self.camera_set         #if you sprite.rect.topleft player is centered properly, but not tiles. if use sprite.rect.center, tile sprites are centered instead
            self.display_surf.blit(sprite.image, camera_set_pos)