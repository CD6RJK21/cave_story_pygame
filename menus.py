import pygame
from graphics import *


def main_menu(screen):
    songs = ['data/music/curly.mp3']
    title_image = load_image('title.png')
    move_sound = pygame.mixer.Sound('data/sound/menu_move.wav')
    running = True
    menu_sprites = pygame.sprite.Group()
    title = pygame.sprite.Sprite(menu_sprites)
    title.image = title_image
    title.rect = title.image.get_rect()
    clock = pygame.time.Clock()
    title.rect.x = (screen.get_size()[0] // 2) - (title.rect.width // 2)
    title.rect.y = screen.get_size()[1] // 2 - title.rect.height * 1.5
    new_game = pygame.sprite.Sprite(menu_sprites)
    new_game.image = cut_image_one(load_image('Title1.png'), (292, 8), (339, 25))
    new_game.rect = new_game.image.get_rect()
    new_game.rect.x = (screen.get_size()[0] // 2) - (new_game.rect.width // 2)
    new_game.rect.y = screen.get_size()[1] // 2 - new_game.rect.height
    load_game = pygame.sprite.Sprite(menu_sprites)
    load_game.image = cut_image_one(load_image('Title1.png'), (292, 38), (343, 55))
    load_game.rect = load_game.image.get_rect()
    load_game.rect.x = (screen.get_size()[0] // 2) - (load_game.rect.width // 2)
    load_game.rect.y = screen.get_size()[1] // 2 - load_game.rect.height + new_game.rect.height * 2
    player_right = AnimatedSprite(menu_sprites, load_image('MyChar.png'), 11, 4, 16, 16, 8,
                                  [[1, 1], [1, 0], [1, 2], [1, 0]])
    player_right.rect.x = new_game.rect.x - player_right.rect.width
    player_right.rect.y = new_game.rect.y - 0.25 * player_right.rect.height
    active_button = 'new'
    pygame.mixer.music.load(songs[0])
    pygame.mixer.music.play(-1)
    while running:
        screen.fill((50, 51, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    running = False  # TODO: fix game start
                elif event.key == pygame.K_DOWN:
                    if active_button == 'new':
                        move_sound.play()
                        active_button = 'load'
                        player_right.rect.y = load_game.rect.y - 0.25 * player_right.rect.height
                    else:
                        move_sound.play()
                        active_button = 'new'
                        player_right.rect.y = new_game.rect.y - 0.25 * player_right.rect.height
                elif event.key == pygame.K_UP:
                    if active_button == 'load':
                        move_sound.play()
                        active_button = 'new'
                        player_right.rect.y = new_game.rect.y - 0.25 * player_right.rect.height
                    else:
                        move_sound.play()
                        active_button = 'load'
                        player_right.rect.y = load_game.rect.y - 0.25 * player_right.rect.height
        menu_sprites.update()
        menu_sprites.draw(screen)
        clock.tick(60)
        pygame.display.flip()
    pygame.mixer.music.stop()
    if active_button == 'new':
        return 'new'
    elif active_button == 'load':
        return 'load'


def quit_menu(screen, resolution, groups):
    clock = pygame.time.Clock()
    move_sound = pygame.mixer.Sound('data/sound/menu_move.wav')
    dialog_window_group = pygame.sprite.Group()
    dialog_window = pygame.sprite.Sprite(dialog_window_group)
    dialog_window.image = cut_image_one(load_image('TextBox.png'), (310, 102), (463, 153))
    dialog_window.rect = dialog_window.image.get_rect()
    dialog_window.rect.x = resolution[0]
    dialog_window.rect.y = resolution[1] / 2
    arrow_group = pygame.sprite.Group()
    arrow = ChosenAnimatedSprite(arrow_group, [cut_image_one(load_image('TextBox.png'), (227, 180), (251, 199)),
                                               cut_image_one(load_image('TextBox.png'), (258, 180), (283, 199))], 120)
    arrow.rect = arrow.image.get_rect()
    arrow.rect.x = dialog_window.rect.x + 80
    arrow.rect.y = dialog_window.rect.y + 20
    active_button = 'no'
    slide = False
    runn = True
    while runn:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if active_button == 'yes':
                        exit()
                    else:
                        runn = False
                elif event.key == pygame.K_LEFT:
                    if active_button == 'no':
                        move_sound.play()
                        active_button = 'yes'
                    else:
                        move_sound.play()
                        active_button = 'no'
                elif event.key == pygame.K_RIGHT:
                    if active_button == 'yes':
                        move_sound.play()
                        active_button = 'no'
                    else:
                        move_sound.play()
                        active_button = 'yes'
        if not slide:
            dialog_window.rect.x -= 5
            arrow.rect.x = dialog_window.rect.x + 80
            arrow.rect.y = dialog_window.rect.y + 20
            if dialog_window.rect.x <= resolution[0] - dialog_window.rect.width:
                slide = True
        if active_button == 'yes':
            arrow.rect.x = dialog_window.rect.x + 2
        else:
            arrow.rect.x = dialog_window.rect.x + 80
        groups.draw(screen)
        dialog_window_group.draw(screen)
        arrow_group.update()
        arrow_group.draw(screen)
        clock.tick(120)
        pygame.display.flip()







