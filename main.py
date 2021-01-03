import pygame

from classes.Background import Background
from entities.Mario import Mario

FPS = 60
tile_size = 16
scale = 2
fpsClock = pygame.time.Clock()
pygame.font.init()
window_size = (16 * tile_size * scale, 14 * tile_size * scale)  # 25*14
pygame.display.set_caption('MARIO')
screen = pygame.display.set_mode(window_size)
background = Background(0, 0, screen)
bg = pygame.transform.scale(screen, background.map_size[1])

mario = Mario(0, 0, Mario.DIRECTION_RIGHT, 0, Mario.IN_AIR, screen, background)
background.set_character(mario)

while not mario.pause:
    screen.fill(background.color[background.index])
    background.update()
    mario.update()
    pygame.display.update()
    fpsClock.tick(60)
