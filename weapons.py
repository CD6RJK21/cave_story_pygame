from graphics import *

GUNWIDTH = 3 * TILESIZE / 2
GUNHEIGHT = TILESIZE


class PolarStar:
    def __init__(self):
        self.sound = {'polar_star_l1_2': pygame.mixer.Sound('data/sound/polar_star_l1_2.wav'),
                      'polar_star_l3': pygame.mixer.Sound('data/sound/polar_star_l3.wav')
                      }
        self.offsets = {'up': 2, 'down': 4, 'fwd': 0, 'left': 0, 'right': 1}
        self.sprite_group = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite(self.sprite_group)
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
        self.nozzle = {'left_fwd': (10, 23), 'right_fwd': (38, 23), 'left_up': (27, 4), 'right_up': (21, 4),
                       'left_down': (29, 28), 'right_down': (19, 28)}
        self.state = 'right_fwd'
        self.direction = self.state.split('_')[0]
        self.look = self.state.split('_')[1]
        self.sprite.image = self.images[self.state]
        self.sprite.rect = self.sprite.image.get_rect()
        self.time = 0

        self.bullets_group = pygame.sprite.Group()

    def gun_x(self, direction, player_x):
        return player_x - TILESIZE / 2 if direction == 'left' else player_x

    def gun_y(self, look, player_y):
        y = player_y
        if look == 'up':
            y -= TILESIZE / 4
        elif look == 'down':
            y += TILESIZE / 4
        return y

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, group, x, y, direction, look):
            super().__init__(group)
            self.offset = 0
            self.max_offset = 3.5 * TILESIZE
            self.speed = 10
            self.direction = direction
            self.look = look
            self.x = x
            self.y = y
            if look == 'fwd':
                self.image = cut_image_one(load_image('Bullet.png'),
                                           (TILESIZE * 8, GUNHEIGHT * 2), (TILESIZE * 9, TILESIZE * 3))
            else:
                self.image = cut_image_one(load_image('Bullet.png'),
                                           (TILESIZE * 9, GUNHEIGHT * 2), (TILESIZE * 10, TILESIZE * 3))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y
            self.mask = pygame.mask.from_surface(self.image)

        def collision_rectangle(self):
            width = TILESIZE if self.look == 'fwd' else 4
            height = TILESIZE if self.look != 'fwd' else 4
            return Rectangle(self.rect.x + TILESIZE / 2 - width / 2, self.rect.y + TILESIZE / 2 - height / 2,
                             width, height)

        def update(self, maap, enemies):
            for enemy in enemies.sprites():
                if pygame.sprite.collide_mask(self, enemy):
                    self.kill()
                    enemy.take_damage(1)

            tiles = maap.get_colliding_tiles(self.collision_rectangle())
            for i in range(len(tiles)):
                if tiles[i].type == 'wall':
                    self.kill()
                    return False

            self.offset += self.speed
            if self.look == 'fwd':
                if self.direction == 'left':
                    self.rect.x -= self.speed
                else:
                    self.rect.x += self.speed
            elif self.look == 'up':
                self.rect.y -= self.speed
            elif self.look == 'down':
                self.rect.y += self.speed
            if self.offset >= self.max_offset:
                self.kill()

    def start_fire(self, x, y, direction, look, motion):
        self.sound['polar_star_l1_2'].play()
        bullet_y = self.gun_y(look, y) - TILESIZE / 2
        bullet_x = self.gun_x(direction, x) - TILESIZE / 2
        if look == 'fwd':
            bullet_y += self.nozzle['left_fwd'][1]
            if self.direction == 'left':
                bullet_x += self.nozzle['left_fwd'][0]
            else:
                bullet_x += self.nozzle['right_fwd'][0]
        elif look == 'up':
            bullet_y += self.nozzle['left_up'][1]
            if self.direction == 'left':
                bullet_x += self.nozzle['left_up'][0]
            else:
                bullet_x += self.nozzle['right_up'][0]
        elif look == 'down':
            if motion == 'staying' or motion == 'running':
                look = 'fwd'
                bullet_y += self.nozzle['left_fwd'][1] * 0.65
                if self.direction == 'left':
                    bullet_x += self.nozzle['left_fwd'][0]
                else:
                    bullet_x += self.nozzle['right_fwd'][0]
            else:
                bullet_y += self.nozzle['left_down'][1]
                if self.direction == 'left':
                    bullet_x += self.nozzle['left_down'][0]
                else:
                    bullet_x += self.nozzle['right_down'][0]
        bullet = self.Bullet(self.bullets_group, bullet_x, bullet_y, direction, look)
        # if self.look == 'fwd':
        #     self.fwd_bullet.rect.x, self.fwd_bullet.rect.y = bullet_x, bullet_y
        #     self.bullets_group_fwd.draw(screen)
        # else:
        #     self.up_bullet.rect.x, self.up_bullet.rect.y = bullet_x, bullet_y
        #     self.bullets_group_up.draw(screen)

    def stop_fire(self, direction, look):
        pass

    def update(self, state):
        if state == self.state:
            return
        self.state = state
        self.direction = self.state.split('_')[0]
        self.look = self.state.split('_')[1]
        self.sprite.image = self.images[state]

    def update_bullets(self, maap, enemies):
        self.bullets_group.update(maap, enemies)

    def draw(self, screen, x, y, motion, time, update_time):
        x = self.gun_x(self.direction, x)
        y = self.gun_y(self.look, y)

        if motion == 'running':  # delete this, if game lags
            if update_time - 1 <= time:
                self.time = (self.time + 1) % 2
        else:
            self.time = 0
        y += self.time

        self.sprite.rect.x, self.sprite.rect.y = x, y
        self.sprite_group.draw(screen)
