import pygame
from config import *
import math
from Bullets import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, groups, obstacles, spawn_pos):
        super().__init__(groups)
        self.game = game

        self.x = spawn_pos[0]
        self.y = spawn_pos[1]
        self.image = pygame.image.load('graphics/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE))
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = self.rect.inflate(-10,-10)     
        self.speed = 3

        self.force = 0.5
        #movement
        self.direction = None
        self.move_state = 'moving'
        self.distance = 0

        self.obstacle_sprites = obstacles

        #attack stuff
        self.trigger_radius = 400
        self.attack_state = False 
        self. attack_cooldown = 200
        self.attack_time = None

    def movement(self):
        self.enemy_vector = pygame.math.Vector2(self.rect.center)
        #if self.move_state == 'moving':
        player_vector = pygame.math.Vector2(self.game.player.rect.center)
        difference_vector = (player_vector - self.enemy_vector)
        self.distance = difference_vector.magnitude()
        if self.distance != 0:
            self.direction = difference_vector.normalize()
        

        if self.move_state == 'knocked':
            self.knockback_vector = self.enemy_vector - self.bullet_vector
            self.distance = self.knockback_vector.magnitude()
            if self.distance != 0:
                self.direction = self.knockback_vector.normalize()
        elif self.move_state == 'seeking vibes':
            difference_vector = self.speaker_difference
            if self.speaker_distance != 0:
                self.direction = difference_vector.normalize()


        if self.move_state == 'moving' or self.move_state == 'seeking vibes':
            self.rect.x = self.rect.x + self.direction.x * self.speed
            self.collisions('horizontal')
            self.rect.y = self.rect.y + self.direction.y * self.speed
            self.collisions('vertical')

        elif self.move_state == 'knocked':
            self.rect.x = self.rect.x + self.direction.x * self.force
            self.collisions('horizontal')
            self.rect.y = self.rect.y + self.direction.y * self.force
            self.collisions('vertical')

        self.collisions('bullet')
        #bullet mechanics
        if self.force > 0:
            self.force -= 1
        else:
            self.move_state = 'moving'

        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y

        self.x = self.rect.x / TILE_SIZE
        self.y = self.rect.y / TILE_SIZE
        
    def speaker_check(self):
        if self.game.speaker_sprite:
            for sprite in self.game.speaker_sprite:
                self.speaker_difference = pygame.math.Vector2(sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y)
                self.speaker_distance = self.speaker_difference.magnitude()

                if (self.speaker_distance < sprite.effect_radius) and (self.speaker_distance > sprite.vibe_radius) and self.move_state != 'knocked':
                    self.move_state = 'seeking vibes'

                elif self.speaker_distance <= sprite.vibe_radius and self.move_state != 'knocked':
                    self.move_state = 'vibing'
                elif self.move_state != 'knocked':
                    self.move_state = 'moving'


    # def get_state(self, knocked = False):
    #     #temporary aggro solution
    #     distance = math.hypot(self.game.player.rect.x - self.rect.x, self.game.player.rect.y - self.rect.y)
    #     if self.move_state != 'knocked':
    #         if distance <= self.trigger_radius :
    #             self.move_state = 'moving'
    #         else: 
    #             self.move_state = 'idle'
    
    def apply_knockback(self, bullet_vector):
        self.move_state = 'knocked'
        self.bullet_vector = bullet_vector
        self.force = 10


    def collisions(self, direction):
        # vertical collisions
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if self.rect.colliderect(sprite.rect):
                    if self.direction.y < 0: # up
                        self.rect.top = sprite.rect.bottom
                    elif self.direction.y > 0: # down
                        self.rect.bottom = sprite.rect.top

            for sprite in self.game.enemy_sprites:
                if sprite != self:
                    if self.rect.colliderect(sprite.rect):
                        if self.direction.y < 0: # up
                            self.rect.top = sprite.rect.bottom
                        elif self.direction.y > 0: # down
                            self.rect.bottom = sprite.rect.top
                elif sprite == self:
                    pass
            
        # horizontal collisions               
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if self.rect.colliderect(sprite.rect):
                    if self.direction.x < 0: # left
                        self.rect.left = sprite.rect.right
                    elif self.direction.x > 0: # right
                        self.rect.right = sprite.rect.left

            for sprite in self.game.enemy_sprites:
                if sprite != self:
                    if self.rect.colliderect(sprite.rect):
                        if self.direction.x < 0: # up
                            self.rect.left = sprite.rect.right
                        elif self.direction.x > 0: # down
                            self.rect.right = sprite.rect.left
                elif sprite == self:
                    pass

        #bullet collision
        if direction == 'bullet':
            if self.game.attack_sprites:
                for attack_sprite in self.game.attack_sprites:
                    collided_enemy_sprites = pygame.sprite.spritecollide(attack_sprite, self.game.enemy_sprites, False)
                    if collided_enemy_sprites:
                        attack_sprite.kill()
                        for target_sprite in collided_enemy_sprites:
                            target_sprite.apply_knockback(attack_sprite.bullet_vector)


    # def masking(self):         #for optimisation, so masks arent always generated DOEsnt work lomao
    #     if self.distance >= VISION_RANGE:
    #         self.mask = 0 #this doesnt work
    #     elif self.distance < VISION_RANGE:
    #         self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        #self.masking()
        self.movement()
        self.speaker_check()
        

    

    @property
    def position(self):
        return self.x, self.y
    
    @property
    def tile_position(self):
        return int(self.x), int(self.y)