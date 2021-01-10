import pygame

from classes.Background import Background
from classes.Level import Level
from entities.Mario import Mario
from classes.Constants import *

fpsClock = pygame.time.Clock()
pygame.font.init()
window_size = (16 * tile_size * scale, 14 * tile_size * scale)  # 25*14
pygame.display.set_caption('MARIO')
screen = pygame.display.set_mode(window_size)
level = Level("levels/map1_1.json", screen)
background = Background(0, 0, screen, level)
bg = pygame.transform.scale(screen, (w, h))

mario = Mario(0, 0, Mario.DIRECTION_RIGHT, 0, Mario.IN_AIR, screen, background, level)
background.set_character(mario)

while not mario.pause:
    background.update()
    mario.update()
    pygame.display.update()
    fpsClock.tick(60)
