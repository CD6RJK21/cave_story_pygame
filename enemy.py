import math
from graphics import *


TILESIZE = 32


class FirstCaveBat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.update_time = 3
        self.cur_frame = 0
        self.time = 0

        self.image = load_image('bat.png')
        self.sprite_group = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite(self.sprite_group)
        self.direction = 'left'
        self.motion = 'flying'

        self.set_sprite('flying_left')
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = self.x
        self.sprite.rect.y = self.y

        self.angular_speed = 5
        self.flight_angle = 0.0

    def set_sprite(self, state):
        # self.last_state = '_'.join([self.get_sprite_state(), self.direction])
        sprites = {'flying_left': cut_sheet(self.image, 6, 2, [[0, 2], [0, 4], [0, 3], [0, 4]])
                   }
        state1 = state.split('_')
        self.direction = state1[1]
        self.motion = state1[0]
        self.frames = sprites[state]
        self.state = state
        self.sprite.image = self.frames[0]

    def draw(self, screen):
        self.sprite.rect.y = self.y + 5 * TILESIZE / 2 * math.sin(self.flight_angle/180)
        self.sprite_group.draw(screen)

    def update(self):
        self.flight_angle += self.angular_speed

        self.time += 1
        if self.time >= self.update_time:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.sprite.image = self.frames[self.cur_frame]
            self.time = 0
