import sys
import pygame
from pytmx.util_pygame import load_pygame
from player import *
from config import *
from level import *
from raycast import *
from camera import *
from enemy import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.time_between_frames = 0
        pygame.mouse.set_cursor(pygame.cursors.broken_x)
        #need a thing here for both zones with tmx_data
        #self.zone = 'upper'
        self.tmx_data = load_pygame('graphics/tiled_map/tiledmap.tmx')
        self.game_state = 'new game'
        self.new_game()


    def new_game(self):
        self.display_surf = pygame.display.get_surface()
        self.camera_set = pygame.math.Vector2(100, 200)
        self.floor_surf = pygame.image.load('graphics/tiled_map/tiledmap.png')#(#pygame.Surface((5632, 5632))
        #self.floor_surf.fill('black')  
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))    #image.load('graphics/map.png').convert() #self.floor_surf = pygame.image.load('graphics/ground.png').convert()
        #self.floor_mask = pygame.mask.from_surface(self.floor_surf)

        # self.darkness_surf = pygame.Surface((5632, 5632), pygame.SRCALPHA, 32)
        # self.darkness_surf.fill('black')
        # self.darkness_mask = pygame.mask.from_surface(self.darkness_surf)

        self.visible_sprites = YCameraGroup(self)
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        self.speaker_sprite = pygame.sprite.GroupSingle()

        self.map = Map(self)
        
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (25, 25))
        self.enemy = Enemy(self, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, (20, 20))
        self.player = Player(self, [self.visible_sprites], self.obstacle_sprites, self.enemy_sprites, (30, 30)) #Player(self)
        self.raycast = RayCast(self)
    
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
        # self.map.draw()
        self.visible_sprites.new_draw(self.player)
        #for i in 
    
        #self.player.draw()

    def run(self):
        while True and self.game_state != 'game over':
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