import random
import pygame
from os import listdir
import time

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()
FPS = pygame.time.Clock()

screen = width, height = 1000, 800

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0
CHANGING = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

font = pygame.font.SysFont('Verdana', 20)
font_gameOver = pygame.font.SysFont('Verdana', 40)

main_surface = pygame.display.set_mode(screen) #creating display

IMGS_PATH = 'Goose'

#player = pygame.Surface((20, 20))
#player.fill(WHITE)
player_imgs = [pygame.transform.scale_by(pygame.image.load(IMGS_PATH+'/'+file).convert_alpha(), 0.8) for file in listdir(IMGS_PATH)]
player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 5


def create_enemy():
    #enemy = pygame.Surface((20,20))
    #enemy.fill(RED)
    enemy = pygame.transform.scale_by(pygame.image.load('enemy.png').convert_alpha(), 0.8)
    enemy_rect = pygame.Rect(width, random.randint(0 + enemy.get_height(), height - enemy.get_height()), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]


def create_bonus():
    #bonus = pygame.Surface((20,20))
    #bonus.fill(GREEN)
    bonus = pygame.transform.scale_by(pygame.image.load('bonus.png').convert_alpha(), 0.8)
    bonus_rect = pygame.Rect(random.randint(0 + bonus.get_width(), width - bonus.get_width()), -bonus.get_height(), *bonus.get_size())
    bonus_speed = random.randint(2, 5)
    return [bonus, bonus_rect, bonus_speed]


bg = pygame.transform.scale(
    pygame.image.load('background.png').convert(), screen)

bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 2500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

# GAME_OVER = pygame.USEREVENT + 4
# pygame.time.set_timer(GAME_OVER, 125, 0)

img_index = 0

scores = 0

enemies = []
bonuses = []

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            is_working = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]


    pressed_keys = pygame.key.get_pressed()

    #main_surface.fill(BLACK)

    #main_surface.blit(bg, (0,0))

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(player, player_rect) #draw player on the display

    main_surface.blit(font.render(str(scores), True, BLACK), (width - 30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0 - enemy[0].get_width():
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            # main_surface.fill(BLACK)
            # event.type = GAME_OVER
            # Якщо зіткнення сталось, то виводимо на екран "GAME OVER" та чекаємо 5 секунд
            # font = pygame.font.Font(None, 100)
            text = font_gameOver.render("GAME OVER", True, WHITE)
            main_surface.fill(BLACK)
            main_surface.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.flip()
            time.sleep(3)
            # pygame.time.set_timer(False, 125)
            pygame.quit()
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom > height + bonus[0].get_height():
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)
    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)
    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)
    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)

    #main_surface.fill((155, 30, 155))
    pygame.display.flip()
