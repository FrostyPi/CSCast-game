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
        self.tmx_data = self.game.tmx_data
        self.matrix = [[]]

    def get_map(self):
        #make dependent on which zone and potentially optimise for pathfinding
        self.matrix = self.matrix_gen(88, 88)

        for layer in self.game.tmx_data.layers:
            if hasattr(layer, 'data'):
                if layer.name == 'Walls':
                    for x, y, surface in layer.tiles():
                        Tile((x * TILE_SIZE + TILE_SIZE/2, y * TILE_SIZE + TILE_SIZE/2), [self.game.visible_sprites, self.game.obstacle_sprites], surface = surface.convert_alpha(), flag = 1)
                        self.world_map[(x, y)] = 1
                        self.matrix[y][x] = 1
                        #print(x, y)
                        #self.matrix[0][66] = 1
        #print(self.matrix)



    def matrix_gen(self, rows, columns):
        matrix = [[0 for _ in range(columns)] for _ in range(rows)]
        return matrix
        
        #print(self.world_map)
                # elif layer.name == 'Floor':
                #     for x, y, surface in layer.tiles():
                #         Tile((x * TILE_SIZE + TILE_SIZE/2, y * TILE_SIZE + TILE_SIZE/2), [self.game.visible_sprites], surface = surface.convert_alpha(), flag = 1)

                


        # for j, row in enumerate(mini_map):
        #     for i, element in enumerate(row):
        #         if element != 0:
        #             Tile((i * TILE_SIZE + TILE_SIZE/2, j * TILE_SIZE + TILE_SIZE/2), [self.game.visible_sprites, self.game.obstacle_sprites], surface = pygame.image.load('graphics/rock.png').convert_alpha(), flag = element)
        #             self.world_map[(i, j)] = element
                # else: 
                #     Tile((i * TILE_SIZE + TILE_SIZE/2, j * TILE_SIZE + TILE_SIZE/2), [self.game.visible_sprites], surface = pygame.image.load((TILE_SIZE, TILE_SIZE)), flag = element)





    # def draw(self):
    #     [pygame.draw.rect(self.game.screen, 'darkgray', (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
    #      for pos in self.world_map]     
    