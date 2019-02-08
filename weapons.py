from graphics import *

GUNWIDTH = 3 * TILESIZE / 2
GUNHEIGHT = TILESIZE


class PolarStar:
    def __init__(self):
        self.offsets = {'up': 2, 'down': 4, 'fwd': 0, 'left': 0, 'right': 1}
        self.sprite_group = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite(self.sprite_group)
        self.images = cut_sheet(load_image('polar_star.png'), 1, 6, [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0]])
        self.images = {'left_fwd': cut_image_one(load_image('Arms.png'),
                                                 (GUNWIDTH * 2, 0), (GUNWIDTH * 3, GUNHEIGHT)),
                       'right_fwd': cut_image_one(load_image('Arms.png'),
                                                  (GUNWIDTH * 2, GUNHEIGHT), (GUNWIDTH * 3, GUNHEIGHT * 2)),
                       'left_up': cut_image_one(load_image('Arms.png'),
                                                (GUNWIDTH * 2, GUNHEIGHT * 2), (GUNWIDTH * 3, GUNHEIGHT * 3)),
                       'right_up': cut_image_one(load_image('Arms.png'),
                                                 (GUNWIDTH * 2, GUNHEIGHT * 3), (GUNWIDTH * 3, GUNHEIGHT * 4)),
                       'left_down': cut_image_one(load_image('Arms.png'),
                                                  (GUNWIDTH * 2, GUNHEIGHT * 4), (GUNWIDTH * 3, GUNHEIGHT * 5)),
                       'right_down': cut_image_one(load_image('Arms.png'),
                                                   (GUNWIDTH * 2, GUNHEIGHT * 5), (GUNWIDTH * 3, GUNHEIGHT * 6))}
        self.state = 'right_fwd'
        self.direction = self.state.split('_')[0]
        self.look = self.state.split('_')[1]
        self.sprite.image = self.images[self.state]
        self.sprite.rect = self.sprite.image.get_rect()
        self.time = 0

    def update(self, state):
        if state == self.state:
            return
        self.state = state
        self.direction = self.state.split('_')[0]
        self.look = self.state.split('_')[1]
        self.sprite.image = self.images[state]

    def draw(self, screen, x, y, motion, time, update_time):
        if self.direction == 'left':
            x -= TILESIZE / 2
        if self.look == 'up':
            y -= TILESIZE / 4
        elif self.look == 'down':
            y += TILESIZE / 4
        if motion == 'running':  # delete this, if game lags
            if update_time - 1 <= time:
                self.time = (self.time + 1) % 2
        else:
            self.time = 0
        y += self.time

        self.sprite.rect.x, self.sprite.rect.y = x, y
        self.sprite_group.draw(screen)
