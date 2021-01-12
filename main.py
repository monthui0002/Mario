import pygame

from classes.Menu import Menu
from classes.Background import Background
from classes.Level import Level
from entities.Mario import Mario
from classes.Constants import *

fpsClock = pygame.time.Clock()
pygame.font.init()
window_size = (16 * tile_size * scale, 14 * tile_size * scale)  # 25*14
pygame.display.set_caption('MARIO')
screen = pygame.display.set_mode(window_size)
bg = pygame.transform.scale(screen, (w, h))


while True:
    menu = Menu(screen)

    while not menu.pause:
        menu.update()
        pygame.display.update()
        fpsClock.tick(FPS/6)
    level = Level("levels/" + menu.level_name, screen)
    background = Background(0, 0, screen, level)
    mario = Mario(0, 0, Mario.DIRECTION_RIGHT, 0, Mario.IN_AIR, screen, background, level)
    background.set_character(mario)

    while not mario.restart:
        if mario.pause:
            mario.pauseObject.update()
        else:
            background.update()
            mario.update()
        pygame.display.update()
        fpsClock.tick(FPS)
