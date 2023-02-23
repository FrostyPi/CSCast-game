import pygame
import math
from config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, groups, obstacle_group):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/nerf-bullet.png').convert_alpha()
    
        
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

        if player.gun_upgrade == True:
            self.range = 560
            self.speed = 10
        

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
    def __init__(self, game, player, groups):
        super().__init__(groups)
        self.game = game
        self.player = player

        self.image = pygame.image.load('graphics/speaker.png').convert_alpha()

        self.rect = self.image.get_rect(center = player.rect.center)
        self.effect_radius = 300
        self.vibe_radius = 160

        self.duration = 20
        self.time_so_far = 0
        self.game.time_between_frames

        self.audio = pygame.mixer.Sound('sound/brightside-dis.mp3')
        self.base_level = 0.0038
        self.audio.set_volume(self.base_level)
        self.audio.play()

        if player.speaker_upgrade == True:
            self.effect_radius = 600
            self.duration = 30
            
    
    def update(self):
        if self.player.covid == True:
            self.audio.stop()

        distance_to_player = pygame.math.Vector2(self.player.rect.x  - self.rect.x, self.player.rect.y - self.rect.y).magnitude()
        if distance_to_player != 0:
            if 0 < distance_to_player <= 10:
                distance_to_player = 11
            elif distance_to_player > self.effect_radius + 400:
                distance_to_player = self.effect_radius

            sound_diminisher = (self.effect_radius + 400) / distance_to_player
            self.audio.set_volume(self.base_level * sound_diminisher)
        
        elif distance_to_player >= 256:
            self.audio.set_volume(0)
        else:
            self.audio.set_volume(1)

        if self.time_so_far >= self.duration * 1000:
            self.audio.stop()
            self.effect_radius = 0
            self.vibe_radius = 0
        else:
            self.time_so_far += self.game.time_between_frames

