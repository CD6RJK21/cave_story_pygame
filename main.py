import pygame
from menus import *
from player import *
from level import *
from enemy import *

TILESIZE = 32
FPS = 60
resolution = WIDTH, HEIGHT = 640, 480

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
screen = pygame.display.set_mode(resolution)  # , pygame.FULLSCREEN
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player((8 * TILESIZE, 11 * TILESIZE))
player.rect.x, player.rect.y = 8 * TILESIZE, 11 * TILESIZE
main_menu_res = main_menu(screen)

loading_screen(screen)

test_map = load_first_cave()
maap = Map(test_map[0])
maap.FixedBackdrop(load_image('bkBlue.png'))
maap.background(test_map[1])

enemies = pygame.sprite.Group()
bat = FirstCaveBat(enemies, 13*TILESIZE, 7*TILESIZE)

all_sprites.add(*maap.backdrop_group.sprites(), *maap.foreground_group.sprites(), *maap.background_group.sprites(),
                *player.damage_group.sprites(), *player.player_group.sprites(), *enemies.sprites(),
                *player.health_background_group.sprites(), *player.health_foreground.sprites(),
                *player.health_number_group.sprites())

running = True
if SOUND_ON:
    pygame.mixer.music.load('data/music/gestation.mp3')  # TODO: down the music volume
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_F4] and pressed[pygame.K_LALT]:
                exit()
            if event.key == pygame.K_ESCAPE:
                quit_menu(screen, resolution, all_sprites)
                continue
            # if pressed[pygame.K_RIGHT] and pressed[pygame.K_LEFT]:
            #     player.stop_running()
            if pressed[pygame.K_UP] and pressed[pygame.K_DOWN]:
                player.look = 'fwd'
            elif pressed[pygame.K_UP]:
                player.look = 'up'
            elif pressed[pygame.K_DOWN]:
                player.look = 'down'
                player.interacting = True
            if event.key == pygame.K_LEFT:
                player.start_running_left()
            elif event.key == pygame.K_RIGHT:
                player.start_running_right()
            elif event.key == pygame.K_z:
                player.start_jump()
            elif event.key == pygame.K_x:
                player.start_fire()
        if event.type == pygame.KEYUP:
            pressed = pygame.key.get_pressed()
            if event.key == pygame.K_LEFT and not pressed[pygame.K_RIGHT]:
                player.stop_running()
            elif event.key == pygame.K_RIGHT and not pressed[pygame.K_LEFT]:
                player.stop_running()
            elif event.key == pygame.K_UP:
                player.look = 'fwd'
            elif event.key == pygame.K_DOWN:
                player.look = 'fwd'
                player.interacting = False
            elif event.key == pygame.K_z:
                player.stop_jump()
            elif event.key == pygame.K_x:
                player.stop_fire()
    maap.draw_background(screen)
    enemies.update(player)
    enemies.draw(screen)
    player.update(maap, enemies)
    player.draw(screen)

    for enemy in enemies.sprites():
        if player.damage_rectangle().collide_width(enemy.damage_rectangle()):
            player.take_damage(enemy.damage)

    maap.update()
    maap.draw(screen)
    player.drawHUD(screen)
    clock.tick(FPS)
    pygame.display.flip()
