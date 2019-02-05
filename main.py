import pygame
from menus import main_menu
from player import Player

FPS = 60
resolution = width, height = 640, 480

pygame.init()
screen = pygame.display.set_mode(resolution)  # , pygame.FULLSCREEN
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = Player(player_group, (50, 50))
main_menu_res = main_menu(screen)


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
            if pressed[pygame.K_RIGHT] and pressed[pygame.K_LEFT]:
                player.stop_running()
            if pressed[pygame.K_UP] and pressed[pygame.K_DOWN]:
                player.look = 'fwd'
            elif pressed[pygame.K_UP]:
                player.look = 'up'
            elif pressed[pygame.K_DOWN]:
                player.look = 'down'
            if event.key == pygame.K_LEFT:
                player.start_running_left()
            elif event.key == pygame.K_RIGHT:
                player.start_running_right()
            elif event.key == pygame.K_z:
                player.start_jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.stop_running()
            elif event.key == pygame.K_RIGHT:
                player.stop_running()
            elif event.key == pygame.K_z:
                player.stop_jump()
    all_sprites.draw(screen)
    all_sprites.update()
    player_group.draw(screen)
    player_group.update()
    # player.update()
    clock.tick(FPS)
    pygame.display.flip()
