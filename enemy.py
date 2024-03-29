import pygame
from config import *
import math
from weapons import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, groups, obstacles, spawn_pos):
        super().__init__(groups)
        self.game = game

        self.spawn_x = spawn_pos[0]
        self.spawn_y = spawn_pos[1]

        self.x = spawn_pos[0]
        self.y = spawn_pos[1]

        self.image = pygame.image.load('graphics/humanities-student-standard-frame.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE))
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = self.rect.inflate(-10,-10)     
        self.speed = 3

        self.force = 0.5
        #movement
        self.direction = None
        self.move_state = 'idle'
        self.distance = 0

        self.obstacle_sprites = obstacles

        #aggro
        self.trigger_radius = 400
        self.linger_radius = 800

    def movement(self):
        self.enemy_vector = pygame.math.Vector2(self.rect.center)
       
        player_vector = pygame.math.Vector2(self.game.player.rect.center)
        difference_vector = (player_vector - self.enemy_vector)
        self.distance = difference_vector.magnitude()
        if self.distance != 0:
            self.direction = difference_vector.normalize()

        self.aggro_check()
        self.bullet_collision()

        if self.move_state == 'knocked':
            self.knockback_vector = self.enemy_vector - self.bullet_vector
            self.distance = self.knockback_vector.magnitude()
            if self.distance != 0:
                self.direction = self.knockback_vector.normalize()
        elif self.move_state == 'seeking vibes' or self.move_state == 'vibing':
            difference_vector = self.speaker_difference
            if self.speaker_distance != 0:
                self.direction = difference_vector.normalize()


        if self.move_state == 'aggro' or self.move_state == 'seeking vibes':
            self.rect.x = self.rect.x + self.direction.x * self.speed
            self.collisions('horizontal')
            self.rect.y = self.rect.y + self.direction.y * self.speed
            self.collisions('vertical')

        elif self.move_state == 'knocked':
            self.rect.x = self.rect.x + self.direction.x * self.force
            self.collisions('horizontal')
            self.rect.y = self.rect.y + self.direction.y * self.force
            self.collisions('vertical')

        #bullet mechanics
        if self.force > 0:
            self.force -= 1
        else:
            self.move_state = 'idle'
            self.aggro_check()

        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y

        self.x = self.rect.x / TILE_SIZE
        self.y = self.rect.y / TILE_SIZE

        angle = math.degrees(math.atan2(-self.direction[1], self.direction[0])) - 90
        self.rot_image = pygame.transform.rotate(self.image, angle)

        
    def aggro_check(self):
        if self.move_state != 'knocked':
            if self.game.speaker_sprite:
                for sprite in self.game.speaker_sprite:
                    self.speaker_difference = pygame.math.Vector2(sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y)
                    self.speaker_distance = self.speaker_difference.magnitude()

                    if self.speaker_distance > sprite.effect_radius:
                        if self.distance > self.linger_radius:
                            # if self.x != self.spawn_x and self.y != self.spawn_y:
                            #     self.move_state = 'return'
                            if self.x == self.spawn_x and self.y == self.spawn_y:
                                self.move_state = 'idle'
                        #elif self.trigger_radius < self.distance <= self.linger_radius:
                        elif self.distance <= self.trigger_radius:
                            self.move_state = 'aggro'
                    elif (self.speaker_distance <= sprite.effect_radius) and (self.speaker_distance > sprite.vibe_radius):
                        self.move_state = 'seeking vibes'

                    elif self.speaker_distance <= sprite.vibe_radius:
                        self.move_state = 'vibing'

            else:
                if self.distance > self.linger_radius:
                            # if self.x != self.spawn_x and self.y != self.spawn_y:
                            #     self.move_state = 'return'
                            if self.x == self.spawn_x and self.y == self.spawn_y:
                                self.move_state = 'idle'
                        #elif self.trigger_radius < self.distance <= self.linger_radius and self.move_state:
                elif self.distance <= self.trigger_radius:
                    self.move_state = 'aggro'


    def bullet_collision(self):
        if self.game.attack_sprites:
            for attack_sprite in self.game.attack_sprites:
                collided_enemy_sprites = pygame.sprite.spritecollide(attack_sprite, self.game.enemy_sprites, False)
                if collided_enemy_sprites:
                    attack_sprite.kill()
                    for target_sprite in collided_enemy_sprites:
                        target_sprite.move_state = 'knocked'
                        target_sprite.bullet_vector = attack_sprite.bullet_vector
                        target_sprite.force = 8


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

    def update(self):
        #self.masking()
        self.movement()
        #self.speaker_check()
        
    @property
    def position(self):
        return self.x, self.y
    
    @property
    def tile_position(self):
        return int(self.x), int(self.y)