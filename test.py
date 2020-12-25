import pygame
from entities.Mario import Mario
from classes.Background import Background

FPS = 60
fpsClock = pygame.time.Clock()

scale = 2
tile_size = 16
window_size = (25 * tile_size * scale, 14 * tile_size * scale)  # 25*14

x = 0
y = 0
background = Background(x, y)

display_surface = pygame.display.set_mode(window_size)
bg = pygame.transform.scale(display_surface, background.map_size[1])
pygame.display.set_caption('MARIO')

mario = Mario(0, 14 * tile_size * scale - 32, "sound", display_surface, 1)

i = 0
index = 0
time = 0
while not mario.pause:
    display_surface = pygame.display.set_mode(window_size)  # (0,191,255)
    background.update(display_surface, mario)
    mario.update(display_surface,background, index)
    if mario.state == 1 and index < 2.91:
        index += 0.15
    else:
        index = 0
    time += 1 / 60
    pygame.display.update()
    fpsClock.tick(60)
