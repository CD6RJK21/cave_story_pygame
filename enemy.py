import math
from graphics import *


class FirstCaveBat:
    def __init__(self, group, x, y):
        self.x = x
        self.y = y
        self.update_time = 3
        self.cur_frame = 0
        self.time = 0

        self.image = load_image('bat.png')
        self.sprite_group = group
        self.sprite = pygame.sprite.Sprite(self.sprite_group)

        self.direction = 'right'
        self.set_sprite('left')
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = self.x
        self.sprite.rect.y = self.y

        self.angular_speed = 5
        self.flight_angle = 0.0

    def damage_rectangle(self):
        return Rectangle(self.sprite.rect.center[0], self.sprite.rect.center[1], 1, 1)

    def set_sprite(self, state):
        if self.direction != state:
            sprites = {'left': cut_sheet(self.image, 6, 2, [[0, 2], [0, 4], [0, 3], [0, 4]]),
                       'right': cut_sheet(self.image, 6, 2, [[1, 2], [1, 4], [1, 3], [1, 4]])
                       }
            self.direction = state
            self.frames = sprites[state]
            self.state = state
            self.sprite.image = self.frames[0]

    def draw(self, screen):
        self.sprite_group.draw(screen)

    def update(self, player):
        if self.sprite.rect.center[0] < player.rect.center[0]:
            self.set_sprite('right')
        else:
            self.set_sprite('left')
        self.flight_angle += self.angular_speed

        self.time += 1
        if self.time >= self.update_time:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.sprite.image = self.frames[self.cur_frame]
            self.time = 0
        self.sprite.rect.y = self.y + 5 * TILESIZE / 2 * math.sin(self.flight_angle / 180)
