import random
import os
import pygame
from pygame.locals import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()
FPS = pygame.time.Clock()

WIDTH, HEIGHT = 1400, 900
main_display = pygame.display.set_mode((WIDTH, HEIGHT))

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)

FONT = pygame.font.SysFont("Verdana", 20)

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_x1, bg_x2 = 0, WIDTH
bg_move = 3

IMAGE_PATH = 'Goose'
PLAYER_IMAGES = [pygame.image.load(os.path.join(IMAGE_PATH, img)).convert_alpha() for img in os.listdir(IMAGE_PATH)]
player_index = 0
player = PLAYER_IMAGES[player_index]
player_rect = pygame.Rect(0, HEIGHT // 2.5, *player.get_size())

player_speed = 4
player_moves = {K_DOWN: (0, player_speed), K_UP: (0, -player_speed),
                K_LEFT: (-player_speed, 0), K_RIGHT: (player_speed, 0)}

def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (100, 40))
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - 150), *enemy.get_size())
    enemy_speed = [random.randint(-12, -4), 0]
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (150, 150))
    bonus_rect = pygame.Rect(random.randint(100, WIDTH - 200), -60, *bonus.get_size())
    bonus_speed = [0, random.randint(4, 6)]
    return [bonus, bonus_rect, bonus_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 600)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies, bonuses = [], []
score = 0
playing = True

while playing:
    FPS.tick(120)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        elif event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        elif event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        elif event.type == CHANGE_IMAGE:
            player_index = (player_index + 1) % len(PLAYER_IMAGES)
            player = PLAYER_IMAGES[player_index]

    bg_x1 -= bg_move
    bg_x2 -= bg_move
    if bg_x1 <= -WIDTH:
        bg_x1 = WIDTH
    if bg_x2 <= -WIDTH:
        bg_x2 = WIDTH

    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))

    keys = pygame.key.get_pressed()
    for key, move in player_moves.items():
        if keys[key]:
            player_rect.move_ip(move)
            player_rect.clamp_ip(main_display.get_rect())

    for enemy in enemies[:]:
        enemy[1].move_ip(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        if enemy[1].right < 0:
            enemies.remove(enemy)
        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses[:]:
        bonus[1].move_ip(bonus[2])
        main_display.blit(bonus[0], bonus[1])
        if bonus[1].top > HEIGHT:
            bonuses.remove(bonus)
        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.remove(bonus)

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

game_over_text = FONT.render('GAME OVER', True, COLOR_RED)
main_display.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
pygame.display.flip()
pygame.time.wait(2000)
pygame.quit()
