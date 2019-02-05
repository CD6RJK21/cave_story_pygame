import pygame
from graphics import load_image, cut_image_one, AnimatedSprite


class Player(pygame.sprite.Sprite):
    def __init__(self, player_group, pos):
        super().__init__(player_group)

        self.walking_acceleration = 0.3
        self.acceleration = 0
        self.slowdown = 0.91
        self.max_speed_x = 4
        self.speed_x = 0

        self.max_speed_y = 4
        self.gravity = 0.23
        self.speed_y = 0
        self.jump_time = 120
        self.jump_speed = 4
        self.on_ground = False
        self.remaining_time = 0
        self.elapsed_time = 0
        self.jump_active = False

        self.update_time = 8
        self.time = 0
        self.cur_frame = 0
        self.player_image = load_image('MyChar.png')
        self.player_group = player_group
        self.motion = 'staying'
        self.direction = 'left'
        self.look = 'fwd'
        self.last_state = 'staying_left_fwd'
        self.set_sprite('staying_left_fwd')
        self.rect = self.image.get_rect()
        self.rect.move(pos[0], pos[1])

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
        sprites = {'staying_left_fwd': self.cut_sheet(self.player_image, 11, 4, [[0, 0]]),
                   'staying_left_up': self.cut_sheet(self.player_image, 11, 4, [[0, 3]]),
                   'running_left_fwd': self.cut_sheet(self.player_image, 11, 4, [[0, 2], [0, 0], [0, 1], [0, 0]]),
                   'running_left_up': self.cut_sheet(self.player_image, 11, 4, [[0, 5], [0, 3], [0, 4], [0, 3]]),
                   'jumping_left_fwd': self.cut_sheet(self.player_image, 11, 4, [[0, 2]]),
                   'jumping_left_up': self.cut_sheet(self.player_image, 11, 4, [[0, 5]]),
                   'jumping_left_down': self.cut_sheet(self.player_image, 11, 4, [[0, 6]]),
                   'falling_left_fwd': self.cut_sheet(self.player_image, 11, 4, [[0, 1]]),
                   'falling_left_up': self.cut_sheet(self.player_image, 11, 4, [[0, 4]]),
                   'falling_left_down': self.cut_sheet(self.player_image, 11, 4, [[0, 6]]),
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
        self.look = state.split('_')[2]
        self.direction = state.split('_')[1]
        self.motion = state.split('_')[0]
        self.frames = sprites[state]
        self.state = state
        self.image = self.frames[0]

    def get_sprite_state(self):
        if self.on_ground:
            motion = 'staying' if self.acceleration == 0 else 'running'
        else:
            motion = 'jumping' if self.speed_y <= 0 else 'falling'
        return motion

    def set_current_sprite_state(self):
        if self.last_state == '_'.join([self.get_sprite_state(), self.direction, self.look]):
            return
        if self.look == 'down' and self.on_ground:
            self.set_sprite('_'.join([self.get_sprite_state(), self.direction, 'fwd']))
        else:
            self.set_sprite('_'.join([self.get_sprite_state(), self.direction, self.look]))

    def start_running_left(self):
        self.motion = 'running'
        self.direction = 'left'
        self.acceleration = -self.walking_acceleration

    def start_running_right(self):
        self.motion = 'running'
        self.direction = 'right'
        self.acceleration = self.walking_acceleration

    def reset_jump(self):
        self.remaining_time = self.jump_time
        self.jump_active = self.remaining_time > 0
        self.elapsed_time = 0

    def update_jump(self):
        if self.jump_active:
            self.remaining_time -= self.elapsed_time
            if self.remaining_time <= 0:
                self.motion = 'falling'
                self.jump_active = False

    def start_jump(self):
        if self.on_ground:
            self.reset_jump()
            self.speed_y = -self.jump_speed
            self.motion = 'jumping'
        elif self.speed_y < 0:
            self.jump_active = self.remaining_time > 0

    def stop_jump(self):
        self.jump_active = False

    def stop_running(self):
        # while self.speed_x > 0:
        #     self.speed_x -= self.slowdown
        self.acceleration = 0
        self.motion = 'staying'
        # if self.direction == 'left':
        #     self.set_sprite('staying_left')
        # elif self.direction == 'right':
        #     self.set_sprite('staying_right')

    def update(self):
        self.set_current_sprite_state()
        self.rect.x += self.speed_x
        self.speed_x += self.acceleration  # TODO: fix player walking stops when both arrows are pressed
        # if (self.speed_x < self.max_speed_x and (self.speed_x > 0)) or\
        #         (self.speed_x > -self.max_speed_x and (self.speed_x < 0)) or self.speed_x * self.acceleration <= 0:
        #     self.speed_x += self.acceleration
        if self.acceleration > 0:
            self.speed_x = min(self.speed_x, self.max_speed_x)
        elif self.acceleration < 0:
            self.speed_x = max(self.speed_x, -self.max_speed_x)
        else:
            if self.speed_x < 0:
                self.speed_x *= self.slowdown
                if self.speed_x > -0.5:
                    self.speed_x = 0
            # if self.speed_x < 0:
            #     self.speed_x *= self.slowdown * 0.13
            self.speed_x *= self.slowdown

        self.update_jump()
        self.elapsed_time += 1
        self.rect.y += self.speed_y
        if not self.jump_active:
            self.speed_y = min(self.speed_y + self.gravity, self.max_speed_y)
        if self.rect.y >= 200:  # TODO: remove this temporary solution
            self.rect.y = 200
            self.speed_y = 0
        self.on_ground = self.rect.y == 200

        if len(self.frames) > 1:
            self.time += 1
            if self.time >= self.update_time:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.time = 0

