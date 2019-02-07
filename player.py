import pygame
from graphics import *
from level import *

TILESIZE = 32

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        self.group = pygame.sprite.Group()
        super().__init__(self.group)
        self.sound = {'running': pygame.mixer.Sound('data/sound/quote_walk.wav'),
                      'head_bump': pygame.mixer.Sound('data/sound/quote_bonkhead.wav'),
                      'jumping': pygame.mixer.Sound('data/sound/quote_jump.wav')
                      }
        self.rectangle_x = Rectangle(6, 10, 20, 12)
        self.rectangle_y = Rectangle(10, 2, 12, 30)

        self.air_acceleration = 0.08680555555555554  # or it eq to jump gravity
        self.walking_acceleration = 0.25
        self.acceleration = 0
        self.friction = 0.13834635277777776
        self.max_speed_x = 3
        self.speed_x = 0

        self.jump_gravity = 0.1
        self.max_speed_y = 5
        self.gravity = 0.23
        self.speed_y = 0
        self.jump_speed = 4
        self.shortjump_speed = self.jump_speed / 1.5
        self.on_ground = False
        self.jump_active = False

        self.invincible = False
        self.invincible_time = 0
        self.invincible_time_max = 180
        self.invincible_flash_time = 4

        self.update_time = 8
        self.time = 0
        self.cur_frame = 0
        self.player_image = load_image('MyChar.png')
        self.motion = 'staying'
        self.direction = 'left'
        self.look = 'fwd'
        self.interacting = False
        self.last_state = 'staying_left_fwd'
        self.set_sprite('staying_left_fwd')
        self.rect = self.image.get_rect()
        self.rect.move(pos[0], pos[1])

    def collision_info(self, maap, rectangle):
        tiles = maap.get_colliding_tiles(rectangle)
        info = {'collided': False, 'row': 0, 'col': 0}
        for i in range(len(tiles)):
            if tiles[i].type == 'wall':
                info['row'] = tiles[i].row
                info['col'] = tiles[i].col
                info['collided'] = True
                break
        return info

    def bottom_collision(self, delta):
        assert delta >= 0
        return Rectangle(self.rect.x + self.rectangle_y.left,
                         self.rect.y + self.rectangle_y.top + self.rectangle_y.width / 2,
                         self.rectangle_y.width,  self.rectangle_y.height / 1.2 + delta)  # TODO: test bottom_collision

    def top_collision(self, delta):
        assert delta <= 0
        return Rectangle(self.rect.x + self.rectangle_y.left, self.rect.y + self.rectangle_y.top + delta,
                         self.rectangle_y.width, self.rectangle_y.height / 2 - delta)

    def left_collision(self, delta):
        assert delta <= 0
        return Rectangle(self.rect.x + self.rectangle_x.left + delta, self.rect.y + self.rectangle_x.top,
                         self.rectangle_x.width / 2 - delta, self.rectangle_x.height)

    def right_collision(self, delta):
        assert delta >= 0
        return Rectangle(self.rect.x + self.rectangle_x.left + self.rectangle_x.width / 2,
                         self.rect.y + self.rectangle_x.top, self.rectangle_x.width / 2 + delta,
                         self.rectangle_x.height)

    def updatex(self, maap):
        # Speed update
        acceleration = 0
        if self.acceleration < 0:
            acceleration = -self.walking_acceleration if self.on_ground else -self.air_acceleration
        elif self.acceleration > 0:
            acceleration = self.walking_acceleration if self.on_ground else self.air_acceleration
        self.speed_x += acceleration
        if self.acceleration > 0:
            self.speed_x = min(self.speed_x, self.max_speed_x)
        elif self.acceleration < 0:
            self.speed_x = max(self.speed_x, -self.max_speed_x + 0.1)

        else:
            # if self.speed_x < 0:
            #     self.speed_x *= self.slowdown * 1
            #     if self.speed_x > -0.4:
            #         self.speed_x = 0
            # if self.speed_x < 0:
            #     self.speed_x *= self.slowdown * 0.13
            self.speed_x = max(0.0, self.speed_x - self.friction) \
                if self.speed_x > 0 else min(0.0, self.speed_x + self.friction + 0.08)

        delta = self.speed_x
        # Running to right
        if delta > 0:
            info = self.collision_info(maap, self.right_collision(delta))
            if info['collided']:
                self.rect.x = info['col'] * TILESIZE - self.rectangle_x.right
                self.speed_x = 0
            else:
                self.rect.x += delta

            info = self.collision_info(maap, self.left_collision(0))
            if info['collided']:
                self.rect.x = info['col'] * TILESIZE + TILESIZE / 1.52 + self.rectangle_x.left
        # Running to left
        elif delta < 0:
            info = self.collision_info(maap, self.left_collision(delta))
            if info['collided']:  # TODO: fix a little space between player and tile
                self.rect.x = info['col'] * TILESIZE + TILESIZE / 1.55 + self.rectangle_x.left
                self.speed_x = 0
            else:
                self.rect.x += delta

            info = self.collision_info(maap, self.right_collision(0))
            if info['collided']:
                self.rect.x = info['col'] * TILESIZE - self.rectangle_x.right

    def updatey(self, maap):
        # Speed update
        gravity = self.jump_gravity if self.jump_active and self.speed_y < 0 else self.gravity
        self.speed_y = min(self.speed_y + gravity, self.max_speed_y)

        delta = self.speed_y
        if delta > 0:
            info = self.collision_info(maap, self.bottom_collision(delta))
            if info['collided']:
                self.rect.y = info['row'] * TILESIZE - self.rectangle_y.bottom
                self.speed_y = 0
                self.on_ground = True
            else:
                self.on_ground = False
                self.rect.y += delta

            info = self.collision_info(maap, self.top_collision(0))
            if info['collided']:
                self.sound['head_bump'].play()
                self.rect.y = info['row'] * TILESIZE + self.rectangle_y.height
        elif delta < 0:
            info = self.collision_info(maap, self.top_collision(delta))
            if info['collided']:
                self.sound['head_bump'].play()
                self.rect.y = info['row'] * TILESIZE + TILESIZE + self.rectangle_y.top
                self.speed_y = 0
            else:
                self.on_ground = False
                self.rect.y += delta

            info = self.collision_info(maap, self.bottom_collision(0))
            if info['collided']:
                self.on_ground = True
                self.rect.y = info['row'] * TILESIZE - self.rectangle_y.bottom

        # if self.rect.y >= 192 - self.rect.height:  # TODO: remove this temporary solution
        #     self.rect.y = 192 - self.rect.height
        #     self.speed_y = 0
        # self.on_ground = self.rect.y == 192 - self.rect.height

    def cut_sheet(self, sheet, columns, rows, chosen_sprites=list()):
        frames = []
        rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                           sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)))
        if chosen_sprites:
            frames_chosen = []
            for i in chosen_sprites:
                frames_chosen.append(frames[i[0] * columns + i[1]])
            frames = frames_chosen[:]
        return frames

    def set_sprite(self, state):
        self.last_state = '_'.join([self.get_sprite_state(), self.direction, self.look])
        sprites = {'staying_left_down': self.cut_sheet(self.player_image, 11, 4, [[0, 7]]),
                   'staying_left_fwd': self.cut_sheet(self.player_image, 11, 4, [[0, 0]]),
                   'staying_left_up': self.cut_sheet(self.player_image, 11, 4, [[0, 3]]),
                   'running_left_fwd': self.cut_sheet(self.player_image, 11, 4, [[0, 2], [0, 0], [0, 1], [0, 0]]),
                   'running_left_up': self.cut_sheet(self.player_image, 11, 4, [[0, 5], [0, 3], [0, 4], [0, 3]]),
                   'jumping_left_fwd': self.cut_sheet(self.player_image, 11, 4, [[0, 2]]),
                   'jumping_left_up': self.cut_sheet(self.player_image, 11, 4, [[0, 5]]),
                   'jumping_left_down': self.cut_sheet(self.player_image, 11, 4, [[0, 6]]),
                   'falling_left_fwd': self.cut_sheet(self.player_image, 11, 4, [[0, 1]]),
                   'falling_left_up': self.cut_sheet(self.player_image, 11, 4, [[0, 4]]),
                   'falling_left_down': self.cut_sheet(self.player_image, 11, 4, [[0, 6]]),
                   'staying_right_down': self.cut_sheet(self.player_image, 11, 4, [[1, 7]]),
                   'staying_right_fwd': self.cut_sheet(self.player_image, 11, 4, [[1, 0]]),
                   'staying_right_up': self.cut_sheet(self.player_image, 11, 4, [[1, 3]]),
                   'running_right_fwd': self.cut_sheet(self.player_image, 11, 4, [[1, 2], [1, 0], [1, 1], [1, 0]]),
                   'running_right_up': self.cut_sheet(self.player_image, 11, 4, [[1, 5], [1, 3], [1, 4], [1, 3]]),
                   'jumping_right_fwd': self.cut_sheet(self.player_image, 11, 4, [[1, 2]]),
                   'jumping_right_up': self.cut_sheet(self.player_image, 11, 4, [[1, 5]]),
                   'jumping_right_down': self.cut_sheet(self.player_image, 11, 4, [[1, 6]]),
                   'falling_right_fwd': self.cut_sheet(self.player_image, 11, 4, [[1, 1]]),
                   'falling_right_up': self.cut_sheet(self.player_image, 11, 4, [[1, 4]]),
                   'falling_right_down': self.cut_sheet(self.player_image, 11, 4, [[1, 6]])
                   }
        state1 = state.split('_')
        self.look = state1[2]
        self.direction = state1[1]
        self.motion = state1[0]
        self.frames = sprites[state]
        self.state = state
        self.image = self.frames[0]

    def damage_rectangle(self):
        return Rectangle(self.rect.x + self.rectangle_x.left, self.rect.y + self.rectangle_y.top,
                                          self.rectangle_x.width, self.rectangle_y.height)

    def get_sprite_state(self):
        if self.on_ground:
            motion = 'staying' if self.acceleration == 0 else 'running'
        else:
            motion = 'jumping' if self.speed_y <= 0 else 'falling'
        return motion

    def set_current_sprite_state(self):
        self.motion = self.get_sprite_state()
        if self.last_state == '_'.join([self.motion, self.direction, self.look]):
            return
        self.motion = self.get_sprite_state()
        if self.look == 'down' and self.motion == 'staying':
            self.set_sprite('_'.join([self.motion, self.direction, self.look]))
        elif self.look == 'down' and self.on_ground:
            self.set_sprite('_'.join([self.motion, self.direction, 'fwd']))
        else:
            self.set_sprite('_'.join([self.motion, self.direction, self.look]))

    def start_running_left(self):
        self.interacting = False
        self.motion = 'running'
        self.direction = 'left'
        self.acceleration = -1

    def start_running_right(self):
        self.interacting = False
        self.motion = 'running'
        self.direction = 'right'
        self.acceleration = 1

    def start_jump(self):
        self.interacting = False
        self.jump_active = True
        if self.on_ground:
            self.sound['jumping'].play()

            self.speed_y = -self.jump_speed
            self.motion = 'jumping'

    def stop_jump(self):
        self.jump_active = False

    def take_damage(self):
        if self.invincible:
            return
        self.speed_y = min(-self.shortjump_speed, self.speed_y)
        print('I need healing!!')
        self.invincible = True
        self.invincible_time = 0

    def stop_running(self):
        # while self.speed_x > 0:
        #     self.speed_x -= self.slowdown
        self.acceleration = 0
        self.motion = 'staying'
        # if self.direction == 'left':
        #     self.set_sprite('staying_left')
        # elif self.direction == 'right':
        #     self.set_sprite('staying_right')

    def draw(self, screen):
        if self.invincible and self.invincible_time % self.invincible_flash_time == 0:
            return
        self.group.draw(screen)

    def update(self, maap):
        self.set_current_sprite_state()
        self.updatex(maap)
        self.updatey(maap)

        self.interacting = True if self.motion == 'staying' and self.look == 'down' else False  # TODO: test interacting

        if self.invincible:
            self.invincible_time += 1
            self.invincible = self.invincible_time < self.invincible_time_max

        if len(self.frames) > 1:
            self.time += 1
            if self.time >= self.update_time:
                if self.motion == 'running':
                    self.sound['running'].play()
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.time = 0

