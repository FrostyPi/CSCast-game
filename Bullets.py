import pygame
import math
from config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, groups, obstacle_group):
        super().__init__(groups)
        self.image = pygame.Surface((7, 2)).convert_alpha()
        self.image.fill((255, 0, 0)) 
        
        self.origin = player.rect.center
        self.rect = self.image.get_rect(center = player.rect.center)      

        # for collision checks
        self.obstacle_sprites = obstacle_group

        self.pos = player.rect.center
        mx, my = pygame.mouse.get_pos()
        self.direction = (mx - HALF_WIDTH, my - HALF_HEIGHT)
        length = math.hypot(*self.direction)
        if length == 0.0:
            self.direction = (0, 1)
        else:
            self.direction = (self.direction[0]/length, self.direction[1]/length)
        angle = math.degrees(math.atan2(-self.direction[1], self.direction[0]))

        self.image = pygame.transform.rotate(self.image, angle)
        self.speed = 8
        self.range = 230
        self.bullet_vector = pygame.math.Vector2(self.rect.x, self.rect.y)
        

    def bullet_move(self):
        self.dx = self.direction[0]*self.speed
        self.dy = self.direction[1]*self.speed
        self.pos = (self.pos[0]+self.dx, 
                    self.pos[1]+self.dy)
        
        self.rect.y = self.pos[1]
        self.rect.x = self.pos[0]

    def collisions(self): 
        for sprite in self.obstacle_sprites:
                if self.rect.colliderect(sprite.rect):
                    self.kill()

    def update(self):
        self.bullet_move()
        self.collisions()
        if math.hypot(self.rect.x - self.origin[0], self.rect.y - self.origin[1]) >= self.range:
            self.kill()



class PortableSpeaker(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.image = pygame.Surface((24, 24)).convert_alpha()
        self.image.fill('red')

        self.rect = self.image.get_rect(center = player.rect.center)
        self.effect_radius = 300
        self.vibe_radius = 160
        #pygame.draw.circle(self.image, (100, 200, 100, [32]), (self.rect.x, self.rect.y), self.effect_radius)

    
    #def update(self):


        # increased radius with higher ps_level?
        #self.level = player.ps_level