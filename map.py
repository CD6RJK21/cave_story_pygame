import pygame
from graphics import *
from player import *


def create_test_map():
    rows = 15
    cols = 20
    row = 6
    # empty_sprite = pygame.sprite.Sprite(group)
    # empty_sprite.image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    # empty_sprite.rect = empty_sprite.image.get_rect()
    foreground_sprites = [[0 for _ in range(cols)] for k in range(rows)]
    for col in range(cols):
        foreground_sprites[row][col] = pygame.sprite.Sprite()
        foreground_sprites[row][col].image = cut_level(load_image('PrtCave.png'), 5, 16, [[0, 1]])[0]
    return foreground_sprites


class Map:
    def __init__(self, foreground_sprites):
        self.foreground_group = pygame.sprite.Group()
        self.foreground_sprites = foreground_sprites
        self.rows = 15
        self.cols = 20
        for row in range(self.rows):
            for col in range(self.cols):
                if self.foreground_sprites[row][col] != 0:
                    self.foreground_sprites[row][col].rect = self.foreground_sprites[row][col].image.get_rect()
                    self.foreground_sprites[row][col].rect.x = col * 32
                    self.foreground_sprites[row][col].rect.y = row * 32
                    self.foreground_group.add(self.foreground_sprites[row][col])

    def update(self):
        self.foreground_group.update()

    def draw(self, screen):
        self.foreground_group.draw(screen)



# class start_point(screen):
#     def __init__(self, screen, all_sprites):
#         running = True
#         pygame.mixer.music.load('data/music/gestation.mp3')
#         pygame.mixer.music.play(-1)
#
#         pygame.mixer.music.stop()
