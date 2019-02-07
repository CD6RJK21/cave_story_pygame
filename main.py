import pygame
from menus import *
from player import *
from level import *
from enemy import *

TILESIZE = 32
FPS = 60
resolution = WIDTH, HEIGHT = 640, 480

pygame.init()
screen = pygame.display.set_mode(resolution)  # , pygame.FULLSCREEN
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = Player(player_group, (50, 50))
main_menu_res = main_menu(screen)

support_group = pygame.sprite.Group()
screen.fill((0, 0, 0))
loading = pygame.sprite.Sprite(support_group)
loading.image = load_image('Loading.png')
loading.rect = loading.image.get_rect()
loading.rect.x, loading.rect.y = WIDTH / 2 - loading.rect.width / 2, HEIGHT / 2 - loading.rect.height / 2
support_group.draw(screen)
pygame.display.flip()

test_map = create_test_map()
maap = Map(test_map[0])
maap.FixedBackdrop(load_image('bkBlue.png'))
maap.background(test_map[1])

bat = FirstCaveBat(50, 150)

running = True
pygame.mixer.music.load('data/music/gestation.mp3')
pygame.mixer.music.play(-1)
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_F4] and pressed[pygame.K_LALT]:
                exit()  # TODO: make exit dialog window
            if event.key == pygame.K_ESCAPE:
                quit_menu(screen, resolution)
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
    all_sprites.update()
    all_sprites.draw(screen)
    maap.draw_background(screen)
    player_group.update(maap)
    player_group.draw(screen)
    bat.update()
    bat.sprite_group.draw(screen)
    maap.update()
    maap.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
