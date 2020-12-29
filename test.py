import pygame
from entities.Mario import Mario
from classes.Background import Background
from classes.Dashboard import Dashboard
FPS = 60
tile_size = 16
scale = 2
fpsClock = pygame.time.Clock()
pygame.font.init()
window_size = (25 * tile_size * scale, 14 * tile_size * scale)  # 25*14

display_surface = pygame.display.set_mode(window_size)
background = Background(0, 0, display_surface)
bg = pygame.transform.scale(display_surface, background.map_size[1])
pygame.display.set_caption('MARIO')

mario = Mario(0, 0, Mario.DIRECTION_RIGHT, 0, Mario.IN_AIR, display_surface)

while not mario.pause:
    display_surface = pygame.display.set_mode(window_size)  # (0,191,255)
    display_surface.fill(background.color[background.index])
    background.update(mario)
    mario.update(background)
    pygame.display.update()
    fpsClock.tick(60)
