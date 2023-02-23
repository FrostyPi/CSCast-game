import pygame
from player import *
from config import *


class YCameraGroup(pygame.sprite.Group):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.display_surf = self.game.display_surf
        self.camera_set = self.game.camera_set

        self.floor_surf = self.game.floor_surf
        self.floor_rect = self.game.floor_rect 

        self.speaker = pygame.image.load('graphics/speaker.png').convert_alpha()
        self.speaker_mask = pygame.mask.from_surface(self.speaker)
        self.new_speaker_surface = self.speaker_mask.to_surface()
        self.new_speaker_surface.set_colorkey((0, 0, 0))
        self.new_speaker_surface.fill((0, 0, 0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        self.victory = pygame.image.load('graphics/end-screen.png')


    def new_draw(self):
        if self.game.game_state =='victory':
            self.display_surf.blit(self.victory, (0, 0))
        else:
            self.camera_set.y = self.game.player.rect.centery - HALF_HEIGHT
            self.camera_set.x = self.game.player.rect.centerx - HALF_WIDTH

            self.floor_rect_offset = self.floor_rect.topleft - self.camera_set
            self.display_surf.blit(self.floor_surf, self.floor_rect_offset)
        
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): #centery
                camera_set_pos = sprite.rect.topleft - self.camera_set 

                if "Player" in str(sprite):
                    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                    x_theta, y_theta = mouse_pos_x - HALF_WIDTH, mouse_pos_y - HALF_HEIGHT 
                    angle = math.degrees(math.atan2(-y_theta, x_theta)) - 90
                    rot_player = pygame.transform.rotate(sprite.image, angle)
                    camera_set_pos = sprite.rect.center - self.camera_set 
                    self.display_surf.blit(rot_player, (camera_set_pos[0] - int(rot_player.get_width()/2), camera_set_pos[1] - int(rot_player.get_height()/2)))     
                elif "Enemy" in str(sprite):
                    
                    self.offset_x = camera_set_pos[0] - self.game.raycast.rect.left
                    self.offset_y = camera_set_pos[1] - self.game.raycast.rect.top

                    if self.game.raycast.mask.overlap_area(sprite.mask, (self.offset_x, self.offset_y)) > ENEMY_DRAW_OVERLAP:
                        self.display_surf.blit(sprite.rot_image, camera_set_pos)
                    else:
                        pass
                elif "Portable" in str(sprite):
                    self.display_surf.blit(sprite.image, camera_set_pos)
                else: 
                        #if you sprite.rect.topleft player is centered properly, but not tiles. if use sprite.rect.center, tile sprites are centered instead
                    self.display_surf.blit(sprite.image, camera_set_pos)

            if self.game.player.speaker_possession == True:
                self.display_surf.blit(self.speaker, (900, 490))
            else:
                self.display_surf.blit(self.new_speaker_surface, (900, 490))

   