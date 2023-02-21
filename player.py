import pygame
from config import *
import math
from weapons import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, groups, obstacles, enemy_group, spawn_pos, inventory, keys):
        super().__init__(groups)
        self.game = game
        self.inventory = inventory
        self.keys = keys

        self.x = spawn_pos[0]
        self.y = spawn_pos[1]
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(center = (self.x * TILE_SIZE, self.y * TILE_SIZE))  
        self.hitbox = self.rect.inflate(-5, -5) 

        self.rect = self.hitbox.inflate(5,5)
        self.angle = 0

        self.obstacle_sprites = obstacles
        self.enemy_sprites = enemy_group

        #attack stuff
        self.attack_state = False 
        self.attack_cooldown = 200
        self.attack_time = None

        #upgrade possession
        self.speaker_possession = False
        self.flashlight_upgrade = False
        self.speaker_upgrade = False
        self.gun_upgrade = False
        for item in self.game.inventory:
            print(item)
            if item == "speaker":
                self.speaker_possession = True
                print('yes')
            elif item == "flashlight upgrade":
                self.flashlight_upgrade = True
            elif item == "speaker upgrade":
                self.speaker_upgrade = True
            elif item == "gun upgrade":
                self.gun_upgrade = True

        #key possession
        self.right_corridor_key = False
        self.lecture_room_key = False
        self.final_key = False
        for key in keys:
            if key == "lecture room":
                self.right_corridor_key = True
            elif key == "right corridor":
                self.lecture_room_key = True
            elif key == "MCS0001":
                self.final_key = True

        #speaker possession

    def movement(self):
        
        speed = 5
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

        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y

        #for raycasting
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_pos_y - HALF_HEIGHT, mouse_pos_x - HALF_WIDTH) 
        self.angle %= math.tau

    def mouse_inputs(self):
        #attack
        mouse = pygame.mouse.get_pressed(num_buttons=3)

        if mouse[0] and not self.attack_state:
            self.attack_state = True
            self.attack_time = pygame.time.get_ticks()
            self.spawn_attack()

        if mouse[2] and self.speaker_possession:
            self.spawn_speaker()
            self.speaker_possession = False


    def spawn_attack(self):
        Bullet(self, [self.game.visible_sprites, self.game.attack_sprites], self.game.obstacle_sprites)

    def spawn_speaker(self):
        self.speaker = PortableSpeaker(self.game, self, [self.game.visible_sprites, self.game.speaker_sprite])

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

        # collisions with COVID-positive folk
        for sprite in self.enemy_sprites:
            if self.hitbox.colliderect(sprite.hitbox):
                    self.game.game_state = 'game over'

    def item_pickup_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            if self.speaker_possession == False:
                for sprite in self.game.speaker_sprite:
                    if self.rect.colliderect(sprite.rect):
                        sprite.audio.stop()
                        sprite.kill()
                        self.speaker_possession = True
            if self.game.upgrade_sprites:
                for sprite in self.game.upgrade_sprites:
                    if self.rect.colliderect(sprite.rect):
                        sprite.kill()
                        self.inventory_maker()
                        
                        #print(self.game.keys)

    def inventory_maker(self):
        #item upgrades
        if 1 <= self.x <= 3 and 49 <= self.y <= 51:
            self.speaker_possession = True
            self.game.inventory.append("speaker")
        elif 27 <= self.x <= 30 and 24 <= self.y <= 27:
            self.flashlight_upgrade = True
            self.game.inventory.append("flashlight upgrade")
        elif 4 <= self.x <= 6 and 36 <= self.y <= 38:
            self.speaker_upgrade = True
            self.game.inventory.append("speaker upgrade")
        elif 27 <= self.x <= 30 and 5 <= self.y <= 8:
            self.gun_upgrade = True
            self.game.inventory.append("gun upgrade")

        #keys
        elif 27 <= self.x <= 29 and 30 <= self.y <= 33:
            self.lecture_room_key = True
            self.game.keys.append("lecture room")
        elif 26 <= self.x <= 28 and 3 <= self.y <= 5:
            self.right_corridor_key = True
            self.game.keys.append("right corridor")
        elif 1 <= self.x <= 3 and 24 <= self.y <= 26:
            self.final_key = True
            self.game.keys.append("MCS0001")


    def update(self):
        self.movement()
        self.mouse_inputs()
        self.cooldowns()
        self.item_pickup_events()

    @property
    def position(self):
        return self.x, self.y
    
    @property
    def tile_position(self):
        return int(self.x), int(self.y)