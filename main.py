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

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.time_between_frames = 0
        pygame.mouse.set_cursor(pygame.cursors.broken_x)

        self.game_state = 'new game'
        self.stage = "floor-one"
        
        self.pause = False
        self.spawn_position = (11.5, 17)
        self.main_font = pygame.font.SysFont('Arial', 50)
        self.title_surf = self.main_font.render('Cool Man', False, (111, 196, 169))
        self.title_rect = self.title_surf.get_rect(center = (400, 400))
        pygame.mixer.music.load('sound/rain.mp3')
        pygame.mixer.music.set_volume(0.07)
        pygame.mixer.music.play(-1)


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

        self.generate_level_one(self.spawn_position)
        

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

    def generate_level_two(self):
        self.floor_surf = pygame.image.load('graphics/tiled_map/floor-two.png')

        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0)) 
        self.visible_sprites.floor_surf = self.floor_surf
        self.visible_sprites.floor_rect = self.floor_rect
        self.tmx_data = load_pygame('graphics/tiled_map/floor-two.tmx')
        self.map = Map(self)

        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (0, 0))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (21, 2))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (25, 2))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (2, 26))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (5.8, 24.5))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (2.5, 32))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (8, 37))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (5, 40))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (5, 46))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (4, 52))

        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (19, 51.5))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (26, 50))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (3, 5))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (3, 42))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (7, 5))

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
            self.lecture_room_key = Item([self.visible_sprites, self.upgrade_sprites], "keycard-lecture", (28, 32))
        if "right corridor" not in self.keys:
            self.right_corridor_key = Item([self.visible_sprites, self.upgrade_sprites], "keycard-corridor", (27, 4))
        if "MCS0001" not in self.keys:
            self.final_key = Item([self.visible_sprites, self.upgrade_sprites], "keycard-final", (1.8, 25))
#
        self.player = Player(self, [self.visible_sprites], self.obstacle_sprites, self.enemy_sprites, (19, 40), self.inventory, self.keys)
        self.raycast = RayCast(self)

    
    
    def game_event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause = True

    def pause_screen(self):
        while self.pause == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = False


    def game_over_screen(self):
        
        while self.game_state == 'game over':
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # or self.game_state == 'game over':
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_e or event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                        self.game_state = 'new game'
                        self.reset_game()
                        #self.reset_game()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            self.display_surf.blit(self.title_surf, self.title_rect)
            #self.screen.fill((94, 129, 162))

    def reset_game(self):
        self.reset_level()
        self.upgrade_sprites.empty()
        #self.new_game()
        self.inventory = []
        self.keys = []
        
        self.stage = 'floor-one'
        self.generate_level_one(self.spawn_position)

    def update(self):
        self.raycast.update()
        self.visible_sprites.update()
        pygame.display.update()
        self.time_between_frames = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() : .1f}')

    def draw(self):
        self.screen.fill('black')
        self.visible_sprites.new_draw()


    def run(self):
        while True:
            self.game_event_loop()
            if self.pause == True or self.game_state == 'victory':
                self.draw()
                self.update()
                self.pause_screen()
            if self.player.covid == True:
                # if self.player.speaker.audio:
                #     self.player.speaker.audio.stop()
                self.player.kill()
                self.game_state = 'game over'
                self.game_over_screen()

            if self.stage == "floor-one" and self.player.rect.x > 760 and self.player.rect.y < 70:
                self.reset_level()
                self.stage = "floor-two"
                self.generate_level_two()

            elif self.stage == "floor-two" and 1120 <= self.player.rect.x <= 1248 and 2816 >= self.player.rect.y >= 2600 :
                self.reset_level()
                self.stage = "floor-one"
                self.generate_level_one((14, 2))

            self.draw()
            self.update()

if __name__ == '__main__':
    game = Game()
    game.run()

