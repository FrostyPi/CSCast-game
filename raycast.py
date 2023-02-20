import pygame
import math
from config import *

class RayCast(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        #self.floor_mask = self.game.floor_mask
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def ray_cast(self):
        x_player, y_player = self.game.player.position
        x_player_tile, y_player_tile = self.game.player.tile_position
        ray_angle = self.game.player.angle - HALF_FOV + 0.00001

        list_of_intersections = [[HALF_WIDTH, HALF_HEIGHT]]
        for ray in range(RAY_COUNT):
            ray_angle = ray_angle + d_ANGLE
            self.cos_a = math.cos(ray_angle)
            self.sin_a = math.sin(ray_angle)

            flag_1 = False
            flag_2 = False

            #vertical
            if self.cos_a > 0:
                x_vert = x_player_tile + 1
                dx = 1
            else: 
                x_vert = x_player_tile - 1e-7
                dx = -1  
            
            length_vert = (x_vert - x_player) / self.cos_a
            y_vert = self.sin_a * length_vert + y_player
            d_length_v = dx / self.cos_a
            dy = d_length_v * self.sin_a

            for i in range(VISION_RANGE):
                y_intersection = (int(x_vert), int(y_vert))
                if y_intersection in self.game.map.world_map:
                    flag_1 = True
                    break
                y_vert = y_vert + dy
                x_vert = x_vert + dx
                length_vert = length_vert + d_length_v

            #horizontal
            if self.sin_a > 0:
                y_horizontal = y_player_tile + 1
                dy = 1
            else: 
                y_horizontal = y_player_tile - 1e-7
                dy = -1
            
            length_horizontal = (y_horizontal - y_player) / self.sin_a
            x_horizontal = self.cos_a * length_horizontal + x_player
            d_length_h = dy / self.sin_a
            dx = d_length_h * self.cos_a

            for i in range(VISION_RANGE):
                tile_horizontal = (int(x_horizontal), int(y_horizontal))
                if tile_horizontal in self.game.map.world_map:
                    break
                x_horizontal = x_horizontal + dx
                y_horizontal = y_horizontal + dy
                length_horizontal = length_horizontal + d_length_h
            

            if length_vert >= length_horizontal and length_horizontal < VISION_RANGE_ARC:
                self.length = length_horizontal
            elif length_vert < length_horizontal and length_vert < VISION_RANGE_ARC:
                self.length = length_vert
            else:
                self.length = VISION_RANGE_ARC

            list_of_intersections.append([HALF_WIDTH + TILE_SIZE*self.length*self.cos_a, HALF_HEIGHT + TILE_SIZE *self.length*self.sin_a])
            #draw test
            # pygame.draw.line(self.game.screen, 'yellow', (HALF_WIDTH, HALF_HEIGHT),
            #                             (HALF_WIDTH + TILE_SIZE*self.length*self.cos_a, HALF_HEIGHT + TILE_SIZE *self.length*self.sin_a), 2)
        self.draw_polygon_alpha(self.game.display_surf, (200, 200, 174, 128), list_of_intersections)   # this could definitely be optimised
        #self.game.screen
        #print(self.rect)
    
    def draw_polygon_alpha(self, surface, color, points):
        lx, ly = zip(*points)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        pygame.draw.polygon(self.image, color, [(x - min_x, y - min_y) for x, y in points])
        mouse = pygame.mouse.get_pressed(num_buttons=3)
        self.mask = pygame.mask.from_surface(self.image)
        # self.offset_x = self.game.enemy.rect.left - self.rect.left
        # self.offset_y = self.game.enemy.rect.right - self.rect.right


        # if self.game.enemy.mask.overlap_area(self.mask, (self.offset_x, self.offset_y)):
        #     print('wow')
        #print(self.game.enemy.rect.x, self.game.enemy.rect.y)
        #print(self.rect.x, self.rect.y)
        #if not mouse[2]:
        surface.blit(self.image, self.rect)
        # else:
        #     surface.blit(self.mask.to_surface(unsetcolor=(255, 255, 255, 255), setcolor= (0, 0, 0, 0)), self.rect)
        #     surface.blit(self.game.enemy.mask.to_surface(unsetcolor=(255, 255, 255, 255), setcolor= (0, 0, 0, 0)), self.game.enemy.rect)

        #new_mask = self.mask.overlap_mask(self.game.darkness_mask, (offset_x, offset_y))
        # new_mask = self.game.darkness_mask.overlap_mask(self.mask, (offset_x, offset_y))
        # new_surf = new_mask.to_surface(unsetcolor=(255, 255, 255, 255), setcolor= (0, 0, 0, 0))
        # new_surf.set_colorkey((0,0,0))
        #surface.blit(new_surf, self.game.floor_rect)
        # new_mask = self.game.floor_mask.overlap_mask(self.mask, (offset_x, offset_y))
        # new_mask.invert()
        #new_surf = new_mask.to_surface()
        #surface.blit(new_surf, self.game.floor_rect)
        #new_surf.set_colorkey((0, 0, 0))        
        #surface.blit(new_surf, self.rect)
        #self.game.floor_mask
        # if not mouse[2]:
        #     surface.blit(self.image, self.rect)
        # else:
        #     surface.blit(self.mask.to_surface(unsetcolor=(255, 255, 255, 255), setcolor= (0, 0, 0, 0)), self.rect)


    def update (self):
        self.ray_cast()
        