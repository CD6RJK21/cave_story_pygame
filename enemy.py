import math
from graphics import *


class FirstCaveBat(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.x = x
        self.y = y
        self.update_time = 3
        self.cur_frame = 0
        self.time = 0

        self.image = load_image('bat.png')
        self.sprite_group = group

        self.direction = 'right'
        self.set_sprite('left')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.angular_speed = 5
        self.flight_angle = 0.0

        self.max_health = 1
        self.health_current = self.max_health
        self.damage = 1

        self.sound = {'enemy_hurt_cool': pygame.mixer.Sound('data/sound/enemy_hurt_cool.wav')}

    def take_damage(self, damage):
        self.sound['enemy_hurt_cool'].play()
        self.health_current -= damage

    def damage_rectangle(self):
        return Rectangle(self.rect.center[0], self.rect.center[1], 1, 1)

    def set_sprite(self, state):
        if self.direction != state:
            sprites = {'left': cut_sheet(self.image, 6, 2, [[0, 2], [0, 4], [0, 3], [0, 4]]),
                       'right': cut_sheet(self.image, 6, 2, [[1, 2], [1, 4], [1, 3], [1, 4]])
                       }
            self.direction = state
            self.frames = sprites[state]
            self.state = state
            self.image = self.frames[0]
            self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        self.sprite_group.draw(screen)

    def update(self, player):
        if self.health_current <= 0:
            self.kill()

        if self.rect.center[0] < player.rect.center[0]:
            self.set_sprite('right')
        else:
            self.set_sprite('left')
        self.flight_angle += self.angular_speed

        self.time += 1
        if self.time >= self.update_time:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.time = 0
        self.rect.y = self.y + 5 * TILESIZE / 2 * math.sin(self.flight_angle / 180)
