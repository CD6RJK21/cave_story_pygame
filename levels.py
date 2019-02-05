import pygame
from graphics import load_image, cut_image_one, AnimatedSprite
import player


class start_point(screen):
    def __init__(self, screen, all_sprites):
        running = True
        pygame.mixer.music.load('data/music/gestation.mp3')
        pygame.mixer.music.play(-1)

        pygame.mixer.music.stop()
