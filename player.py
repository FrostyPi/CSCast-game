import pygame
from config import *
import math
from Bullets import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, groups, obstacles):
        super().__init__(groups)
        self.game = game

        self.x = 1.5
        self.y = 5
        self.image = pygame.image.load('graphics/tony.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE))        

        self.angle = 0

        self.obstacle_sprites = obstacles

        #attack stuff
        self.attack_state = False 
        self. attack_cooldown = 200
        self.attack_time = None

    def movement(self):
        
        speed = 0.3 * self.game.time_between_frames
        self.dx, self.dy = 0, 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.dy = self.dy - speed
        if keys[pygame.K_s]:
            self.dy = self.dy + speed
        if keys[pygame.K_a]:
            self.dx = self.dx - speed
        if keys[pygame.K_d]:
            self.dx = self.dx + speed

        self.rect.x = self.rect.x + self.dx
        self.collisions('horizontal')
        self.rect.y = self.rect.y + self.dy
        self.collisions('vertical')

        self.x = self.rect.x / TILE_SIZE
        self.y = self.rect.y / TILE_SIZE

        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_pos_y - HALF_HEIGHT, mouse_pos_x - HALF_WIDTH) #self.angle = math.atan2(mouse_pos_y/TILE_SIZE - self.y, mouse_pos_x/TILE_SIZE - self.x)
        #self.angle = math.degrees(math.atan2(mouse_pos_y - self.y, mouse_pos_x - self.x))
        self.angle %= math.tau
        #pygame.transform.rotate(self.image, 40)

    def mouse_inputs(self):
        #attack
        mouse = pygame.mouse.get_pressed(num_buttons=3)

        if mouse[0] and not self.attack_state:
            self.attack_state = True
            self.attack_time = pygame.time.get_ticks()
            self.spawn_attack()
            print('nice')


    def spawn_attack(self):
        Bullet(self, [self.game.visible_sprites])

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attack_state:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attack_state = False


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


    
    def update(self):
        #pygame.transform.rotate(self.image, 40)
        self.movement()
        self.mouse_inputs()
        self.cooldowns()
        #print('x')

    @property
    def position(self):
        return self.x, self.y
    
    @property
    def tile_position(self):
        return int(self.x), int(self.y)