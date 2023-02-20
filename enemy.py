import pygame
from config import *
import math
from Bullets import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, groups, obstacles, incoming_attack_group, spawn_pos):
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
        self.move_state = 'idle'
        self.distance = 0

        self.obstacle_sprites = obstacles
        self.incoming_attacks = incoming_attack_group

        #attack stuff
        self.trigger_radius = 400
        self.attack_state = False 
        self. attack_cooldown = 200
        self.attack_time = None

    def movement(self):
        self.enemy_vector = pygame.math.Vector2(self.rect.center)
        # if self.move_state == 'moving':
        player_vector = pygame.math.Vector2(self.game.player.rect.center)
        difference_vector = (player_vector - self.enemy_vector)
        self.distance = difference_vector.magnitude()
        if self.distance != 0:
            self.direction = difference_vector.normalize()

        self.dx, self.dy = 0, 0

        # angle_to_player = math.atan2(self.game.player.rect.y - self.rect.y, self.game.player.rect.x - self.rect.x)
        # angle_to_player = math.degrees(angle_to_player)

        self.move_state = 'moving'

        self.rect.x = self.rect.x + self.direction.x * self.speed
        self.collisions('horizontal')
        self.rect.y = self.rect.y + self.direction.y * self.speed
        self.collisions('vertical')

        # elif self.move_state == 'knocked':
        #     self.apply_knockback()

        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y

        self.x = self.rect.x / TILE_SIZE
        self.y = self.rect.y / TILE_SIZE
        

        
    def get_state(self, knocked = False):
        #temporary aggro solution
        distance = math.hypot(self.game.player.rect.x - self.rect.x, self.game.player.rect.y - self.rect.y)
        if self.move_state != 'knocked':
            if distance <= self.trigger_radius :
                self.move_state = 'moving'
            else: 
                self.move_state = 'idle'
    
    # def apply_knockback(self):
    #     # self.knockback_vector = self.enemy_vector - self.bullet_vector
    #     self.distance = self.knockback_vector.magnitude()
    #     if self.distance != 0:
    #         self.direction = self.knockback_vector.normalize()

    #     if self.force < 20:
    #         self.rect.x = self.rect.x + self.direction.x / self.force
    #     else:
    #         self.rect.x = self.rect.x
    #         self.force = 0.5
    #         self.move_state = 'idle'

    #     self.force += 1


    def collisions(self, direction):
        # vertical collisions
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if self.rect.colliderect(sprite.rect):
                    if self.dy < 0: # up
                        self.rect.top = sprite.rect.bottom
                    elif self.dy > 0: # down
                        self.rect.bottom = sprite.rect.top
        # horizontal collisions               
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if self.rect.colliderect(sprite.rect):
                    if self.dx < 0: # left
                        self.rect.left = sprite.rect.right
                    elif self.dx > 0: # right
                        self.rect.right = sprite.rect.left

        # for sprite in self.incoming_attacks:
        #         if self.hitbox.colliderect(sprite.rect):
        #             self.move_state = 'knocked'
        #             self.knockback_vector = self.enemy_vector - sprite.bullet_vector

    # def masking(self):         #for optimisation, so masks arent always generated DOEsnt work lomao
    #     if self.distance >= VISION_RANGE:
    #         self.mask = 0 #this doesnt work
    #     elif self.distance < VISION_RANGE:
    #         self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        #self.masking()
        self.movement()
    

    @property
    def position(self):
        return self.x, self.y
    
    @property
    def tile_position(self):
        return int(self.x), int(self.y)