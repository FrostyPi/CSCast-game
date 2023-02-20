import pygame
import math
from config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, groups, enemy_group, obstacle_group):
        super().__init__(groups)
        self.image = pygame.Surface((7, 2)).convert_alpha()
        self.image.fill((255, 0, 0)) 
        
        self.origin = player.rect.center
        self.rect = self.image.get_rect(center = player.rect.center)      

        # for collision checks
        self.enemy_sprites = enemy_group
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

        # for sprite in self.enemy_sprites:
        #         if self.rect.colliderect(sprite.hitbox):
        #             sprite.get_state(knocked = True)
        #             sprite.apply_knockback(pygame.math.Vector2(self.rect.x, self.rect.y))
        #             if self.dy < 0: # up
        #                 self.rect.top = sprite.rect.bottom
        #             elif self.dy > 0: # down
        #                 self.rect.bottom = sprite.rect.top

    def update(self):
        self.bullet_move()
        self.collisions()
        if math.hypot(self.rect.x - self.origin[0], self.rect.y - self.origin[1]) >= self.range:
            self.kill()




class PortableSpeaker(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.image = pygame.Surface(64, 64).convert_alpha()
        self.image.fill('red')

        self.rect = self.image.get_rect(center = player.rect.center)

        #whether the speaker is on the floor or in the hands of the player 

        self.possession_state = 0
        self.level = player.ps_level