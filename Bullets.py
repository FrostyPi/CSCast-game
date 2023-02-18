import pygame
import math
from config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.image = pygame.Surface((7, 2)).convert_alpha()
        self.image.fill((255, 0, 0)) 
        
        self.origin = player.rect.center
        self.rect = self.image.get_rect(center = player.rect.center)      

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
        self.speed = 7
        self.range = 230

    def bullet_move(self):
        self.pos = (self.pos[0]+self.direction[0]*self.speed, 
                    self.pos[1]+self.direction[1]*self.speed)
        
        self.rect.y = self.pos[1]
        self.rect.x = self.pos[0]

    
    def update(self):
        self.bullet_move()
        if math.hypot(self.rect.x - self.origin[0], self.rect.y - self.origin[1]) >= self.range:
            self.kill()