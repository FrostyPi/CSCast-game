import pygame
from tiles import *
from config import *
from camera import *

class Map(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.world_map = {}
        self.get_map()
        self.tmx_data = self.game.tmx_data


    def get_map(self):
        #make dependent on which zone and potentially optimise for pathfinding

        for layer in self.game.tmx_data.layers:
            if hasattr(layer, 'data'):
                if layer.name == 'Walls':
                    for x, y, surface in layer.tiles():
                        Tile((x * TILE_SIZE + TILE_SIZE/2, y * TILE_SIZE + TILE_SIZE/2), [self.game.visible_sprites, self.game.obstacle_sprites], surface = surface.convert_alpha())
                        self.world_map[(x, y)] = 1
                        # self.matrix[y][x] = 1
                if layer.name == 'Doors':
                    for x, y, surface in layer.tiles():
                        Tile((x * TILE_SIZE + TILE_SIZE/2, y * TILE_SIZE + TILE_SIZE/2), [self.game.visible_sprites, self.game.obstacle_sprites, self.game.door_sprites], type = 'door', surface = surface.convert_alpha())




