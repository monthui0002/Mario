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

screen = pygame.display.set_mode(window_size)
bg = pygame.transform.scale(screen, background.map_size[1])
pygame.display.set_caption('MARIO')

mario = Mario(50, 100, Mario.DIRECTION_RIGHT, 1, Mario.IDLE, screen)

i = 0
index = 0
time = 0
while True:
    screen.fill((0, 0, 0))
    mario.update()
    pygame.display.update()
    fpsClock.tick(13)
