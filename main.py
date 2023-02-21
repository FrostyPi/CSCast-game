import sys
import pygame
from pytmx.util_pygame import load_pygame
from player import *
from config import *
from level import *
from raycast import *
from camera import *
from enemy import *
from loot import *

# class GameState():
#     def __init__(self):
#         self.state = 'main_game'
    
#     def main_game()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.time_between_frames = 0
        pygame.mouse.set_cursor(pygame.cursors.broken_x)
        #need a thing here for both zones with tmx_data
        #self.zone = 'upper'
        self.game_state = 'new game'
        self.stage = "floor-one"
        #self.tmx_data = load_pygame(f'graphics/tiled_map/{self.stage}.tmx')
        

        self.new_game()



    def new_game(self):
        self.display_surf = pygame.display.get_surface()
        self.camera_set = pygame.math.Vector2(100, 200)
        self.floor_surf = pygame.image.load('graphics/tiled_map/floor-one.png')

        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0)) 

        self.visible_sprites = YCameraGroup(self)
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        self.upgrade_sprites = pygame.sprite.Group() # neeed to put into rewsrt_levle?

        self.door_sprites = pygame.sprite.Group()

        self.speaker_sprite = pygame.sprite.GroupSingle()
        self.tmx_data = load_pygame('graphics/tiled_map/floor-one.tmx')
        self.map = Map(self)
        
        self.inventory = []
        self.keys = []

        self.generate_level_one((11.5, 17))
        

    def reset_level(self): 
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        self.enemy_sprites.empty()
        self.attack_sprites.empty()
        self.door_sprites.empty()
        self.speaker_sprite.empty()
        


    def generate_level_one(self, spawn_position):
        self.floor_surf = pygame.image.load('graphics/tiled_map/floor-one.png')

        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0)) 
        self.visible_sprites.floor_surf = self.floor_surf
        self.visible_sprites.floor_rect = self.floor_rect
        self.tmx_data = load_pygame('graphics/tiled_map/floor-one.tmx')

        self.map = Map(self)
        self.player = Player(self, [self.visible_sprites], self.obstacle_sprites, self.enemy_sprites, spawn_position, self.inventory, self.keys)
        self.raycast = RayCast(self)
        print(self.inventory)

    def generate_level_two(self):
        self.floor_surf = pygame.image.load('graphics/tiled_map/floor-two.png')

        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0)) 
        self.visible_sprites.floor_surf = self.floor_surf
        self.visible_sprites.floor_rect = self.floor_rect
        self.tmx_data = load_pygame('graphics/tiled_map/floor-two.tmx')
        self.map = Map(self)

        # self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (0, 0))
        # self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (0, 0))
        if "speaker" not in self.inventory:
            self.speaker_item = Item([self.visible_sprites, self.upgrade_sprites], "speaker", (2, 50))
        if "flashlight upgrade" not in self.inventory:
            self.flashlight_upgrade_item = Item([self.visible_sprites, self.upgrade_sprites], "flashlight-upgrade", (29, 25))
        if "speaker upgrade" not in self.inventory:
            self.speaker_upgrade_item = Item([self.visible_sprites, self.upgrade_sprites], "speaker-upgrade", (5, 37))
        if "gun upgrade" not in self.inventory:
            self.gun_upgrade_item = Item([self.visible_sprites, self.upgrade_sprites], "gun-upgrade", (28, 7))
        
        #key check
        if "lecture room" not in self.keys:
            self.lecture_room_key = Item([self.visible_sprites, self.upgrade_sprites], "keycard", (28, 32))
        if "right corridor" not in self.keys:
            self.right_corridor_key = Item([self.visible_sprites, self.upgrade_sprites], "keycard", (27, 4))
        if "MCS0001" not in self.keys:
            self.final_key = Item([self.visible_sprites, self.upgrade_sprites], "keycard", (1.8, 25))
#
        self.player = Player(self, [self.visible_sprites], self.obstacle_sprites, self.enemy_sprites, (19, 40), self.inventory, self.keys)
        self.raycast = RayCast(self)
        #print(self.inventory)

    
    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # or self.game_state == 'game over':
                pygame.quit()
                sys.exit()


    def update(self):
       #self.map.update()
        self.raycast.update()
        self.visible_sprites.update()
        #self.raycast.update()
        pygame.display.update()
        self.time_between_frames = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() : .1f}')

    def draw(self):
        self.screen.fill('black')
        self.visible_sprites.new_draw(self.player)

    def run(self):
        while True and self.game_state != 'game over':
            if self.stage == "floor-one" and self.player.rect.x > 760 and self.player.rect.y < 70:
                self.reset_level()
                self.stage = "floor-two"
                self.generate_level_two()

            elif self.stage == "floor-two" and 1120 <= self.player.rect.x <= 1248 and 2816 >= self.player.rect.y >= 2600 :
                self.reset_level()
                self.stage = "floor-one"
                self.generate_level_one((14, 2))

            #print(self.player.x, self.player.y)
            self.event_loop()
            self.draw()
            self.update()

if __name__ == '__main__':
    game = Game()
    game.run()



# class YCameraGroup(pygame.sprite.Group):
#     def __init__(self, game):
#         super().__init__()

#         self.display_surf = pygame.display.get_surface()
#         self.camera_set = pygame.math.Vector2(100, 200)

#         self.floor_surf = pygame.Surface((5120, 2880)) #self.floor_surf = pygame.image.load('graphics/ground.png').convert()
#         self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))
    
#     def new_draw(self, player):

#         self.camera_set.y = player.rect.centery - HALF_HEIGHT
#         self.camera_set.x = player.rect.centerx - HALF_WIDTH

#         self.floor_rect_offset = self.floor_rect.topleft - self.camera_set
#         self.display_surf.blit(self.floor_surf, self.floor_rect_offset)
        
#         for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
#             camera_set_pos = sprite.rect.topleft - self.camera_set
#             self.display_surf.blit(sprite.image, camera_set_pos)