import pygame
from tiles import *
from config import *
from camera import *

mini_map = [
    [1, 1 ,1 ,1 ,1 ,1 , 1 ,1 , 1 ,1 ,1 ,1 ,1 ,1 ,1, 1],
    [1, 0 ,0 ,0 ,0 ,0 , 0 ,0 , 0 ,0 ,0 ,0 ,0 ,0 ,0, 1],
    [1, 0 ,0 ,0 ,0 ,0 , 0 ,0 , 0 ,0 ,0 ,0 ,0 ,0 ,0, 1],
    [1, 0 ,0 ,0 ,0 ,0 , 0 ,0 , 0 ,0 ,0 ,0 ,0 ,0 ,0, 1],
    [1, 0 ,0 ,0 ,0 ,0 , 0 ,0 , 0 ,0 ,0 ,0 ,0 ,0 ,0, 1],
    [1, 0 ,0 ,0 ,0 ,0 , 0 ,1 , 0 ,0 ,0 ,0 ,0 ,0 ,0, 1],
    [1, 0 ,0 ,0 ,0 ,0 , 0 ,0 , 0 ,0 ,0 ,0 ,0 ,0 ,0, 1],
    [1, 0 ,0 ,0 ,0 ,0 , 0 ,0 , 0 ,0 ,0 ,0 ,0 ,0 ,0, 1],
    [1, 1 ,1 ,1 ,1 ,1 , 1 ,1 , 1 ,1 ,1 ,1 ,1 ,1 ,1, 1]
]

class Map(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()
    def get_map(self):
        for j, row in enumerate(mini_map):
            for i, element in enumerate(row):
                if element != 0:
                    Tile((i * TILE_SIZE + TILE_SIZE/2, j * TILE_SIZE + TILE_SIZE/2), [self.game.visible_sprites, self.game.obstacle_sprites], surface = pygame.image.load('graphics/rock.png').convert_alpha(), flag = element)
                    self.world_map[(i, j)] = element
                # else: 
                #     Tile((i * TILE_SIZE + TILE_SIZE/2, j * TILE_SIZE + TILE_SIZE/2), [self.game.visible_sprites], surface = pygame.image.load((TILE_SIZE, TILE_SIZE)), flag = element)





    # def draw(self):
    #     [pygame.draw.rect(self.game.screen, 'darkgray', (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
    #      for pos in self.world_map]     
    