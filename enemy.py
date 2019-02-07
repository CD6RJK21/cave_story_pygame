from graphics import *


class FirstCaveBat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.update_time = 3
        self.cur_frame = 0
        self.time = 0

        self.image = load_image('NpcCemet.png')
        self.sprite_group = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite()
        self.direction = 'left'
        self.motion = 'flying'

        self.set_sprite('flying_left')
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = x
        self.sprite.rect.y = y


    def set_sprite(self, state):
        # self.last_state = '_'.join([self.get_sprite_state(), self.direction])
        sprites = {'flying_left': cut_sheet(self.image, 19, 7, [[2, 2], [4, 2], [3, 2], [4, 2]])
                   }
        state1 = state.split('_')
        self.direction = state1[1]
        self.motion = state1[0]
        self.frames = sprites[state]
        self.state = state
        self.sprite.image = self.frames[0]

    def update(self):
        if len(self.frames) > 1:
            self.time += 1
            if self.time >= self.update_time:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.sprite.image = self.frames[self.cur_frame]
                self.time = 0
