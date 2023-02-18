import sys
import pygame
from player import *
from config import *
from level import *
from raycast import *
from camera import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        self.time_between_frames = 0
        pygame.mouse.set_cursor(pygame.cursors.broken_x)

        self.new_game()


    def new_game(self):
        self.visible_sprites = YCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.map = Map(self)
        self.player = Player(self, [self.visible_sprites], self.obstacle_sprites) #Player(self)
        self.raycast = RayCast(self)
    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        while True:
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