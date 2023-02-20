import pygame
from player import *
from config import *


class YCameraGroup(pygame.sprite.Group):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.display_surf = self.game.display_surf# self.display_surf = pygame.display.get_surface()
        self.camera_set = self.game.camera_set

        self.floor_surf = self.game.floor_surf# self.floor_surf = pygame.Surface((5632, 5632))
        self.floor_rect = self.game.floor_rect # self.floor_surf.fill('black')      #image.load('graphics/map.png').convert() #self.floor_surf = pygame.image.load('graphics/ground.png').convert()
        # self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))
        #self.darkness_surf = self.game.darkness_surf
    
    def new_draw(self, player):

        self.camera_set.y = player.rect.centery - HALF_HEIGHT
        self.camera_set.x = player.rect.centerx - HALF_WIDTH

        self.floor_rect_offset = self.floor_rect.topleft - self.camera_set
        self.display_surf.blit(self.floor_surf, self.floor_rect_offset)
        #self.floor_surf.blit(self.darkness_surf, self.floor_rect_offset)
        
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): #centery
            if "Player" in str(sprite):
                camera_set_pos = sprite.rect.topleft - self.camera_set 
                #print(camera_set_pos)
                self.display_surf.blit(sprite.image, camera_set_pos)      # can perhaps try to optimise this
            elif "Enemy" in str(sprite):
                camera_set_pos = sprite.rect.topleft - self.camera_set
                
                self.offset_x = camera_set_pos[0] - self.game.raycast.rect.left
                self.offset_y = camera_set_pos[1] - self.game.raycast.rect.top

                #print(camera_set_pos)
                if self.game.raycast.mask.overlap_area(sprite.mask, (self.offset_x, self.offset_y)) > ENEMY_DRAW_OVERLAP:
                    self.display_surf.blit(sprite.image, camera_set_pos)
                else:
                    pass #self.display_surf.blit(sprite.image, camera_set_pos)
            elif "Portable" in str(sprite):
                camera_set_pos = sprite.rect.topleft - self.camera_set

                # circle_surface = pygame.Surface((sprite.effect_radius*2, sprite.effect_radius*2)).convert_alpha()
                # circle_surface.fill((0, 0, 0, 0))
                
                #pygame.draw.circle(circle_surface, 'green', camera_set_pos, sprite.effect_radius)
                self.display_surf.blit(sprite.image, camera_set_pos)
               # self.display_surf.blit(circle_surface, (camera_set_pos[0] - sprite.effect_radius, camera_set_pos[1] - sprite.effect_radius))
                #print('true')
            else: 
                camera_set_pos = sprite.rect.topleft - self.camera_set         #if you sprite.rect.topleft player is centered properly, but not tiles. if use sprite.rect.center, tile sprites are centered instead
                self.display_surf.blit(sprite.image, camera_set_pos)

    # def draw_transparent_circle(self, surface, color, points):
    #     lx, ly = zip(*points)
    #     min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    #     self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    #     self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
    #     self.image.convert_alpha()

    #     pygame.draw.polygon(self.image, color, [(x - min_x, y - min_y) for x, y in points])
    #     mouse = pygame.mouse.get_pressed(num_buttons=3)
    #     self.mask = pygame.mask.from_surface(self.image)