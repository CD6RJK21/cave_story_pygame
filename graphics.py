import pygame
import os


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_group, sheet, columns, rows, x, y, update_time, chosen_sprites=False):
        super().__init__(sprite_group)
        self.chosen_sprites = chosen_sprites
        self.update_time = update_time
        self.time = 0
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        if self.chosen_sprites is not False:
            self.frames_chosen = []
            for i in self.chosen_sprites:
                self.frames_chosen.append(self.frames[i[0] * columns + i[1]])
            self.frames = self.frames_chosen[:]

    def update(self):
        if len(self.frames) != 1:
            self.time += 1
            if self.time >= self.update_time:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.time = 0


class ChosenAnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_group, frames, update_time):
        super().__init__(sprite_group)
        self.update_time = update_time
        self.time = 0
        self.frames = frames
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def update(self):
        self.time += 1
        if self.time >= self.update_time:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.time = 0


# class ChosenAnimatedSprite(AnimatedSprite):
#     def __init__(self, sprite_group, sheet, columns, rows, x, y, update_time, chosen_sprites):  # e.g. chosen_sprites:
#         super().__init__(sprite_group, sheet, columns, rows, x, y, update_time)  # [(row, column), ...]
#         self.chosen_sprites = chosen_sprites
#         self.frames_chosen = []
#
#         self.frames
#
#     def update(self):
#         self.cur_frame = (self.cur_frame + 1) % len(self.frames)
#         self.image = self.frames[self.cur_frame]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def cut_sheet(sheet, columns, rows, chosen_sprites=list()):
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


def get_number_image(num, colour='w'):
    numbers = cut_sheet(load_image('numbers.png'), 10, 2)
    numbers_red = numbers[10:]
    if colour == 'w':
        return numbers[num]
    else:
        return numbers_red[num]


def cut_image_one(image, pos1, pos2):
    image = image.subsurface(pygame.Rect(pos1, (pos2[0] - pos1[0], pos2[1] - pos1[1])))
    return image


def cut_level(image, rows, columns, chosen=False):
    frames = []
    rect = pygame.Rect(0, 0, image.get_width() // columns,
                       image.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(image.subsurface(pygame.Rect(
                frame_location, rect.size)))
    if chosen is not False:
        frames_chosen = []
        for i in chosen:
            frames_chosen.append(frames[i[0] * columns + i[1]])
        frames = frames_chosen[:]
    return frames


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = x
        self.right = x + width
        self.top = y
        self.bottom = y + height

    def collide_width(self, rect):
        return self.right >= rect.left and self.left <= rect.right and\
               self.top <= rect.bottom and self.bottom >= rect.top
