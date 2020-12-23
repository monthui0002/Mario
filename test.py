import pygame, sys
import time
from classes.Mario import Mario

pygame.init()
FPS = 1
fpsClock = pygame.time.Clock()

windowSize = (640, 480)

# mario = pygame.image.load('./mario.png')
# mario = mario.subsurface((80, 34, 16, 16))
# mario = pygame.transform.scale(mario, (32, 32))
# DISPLAYSURF.blit(self.img, (int(self.x), int(self.y)))

displaySurface = pygame.display.set_mode(windowSize)
mario = Mario(0,0,"sound",displaySurface)
pygame.display.set_caption('MARIO')
pygame.init()
i = 0
while True:
    left = False
    right = False
    up = False
    down = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_UP:
                up = True
                down = True
            if event.key == pygame.K_DOWN:
                down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False
            if event.key == pygame.K_UP:
                up = False
            if event.key == pygame.K_DOWN:
                down = True
    mario.updateImage(up,down,right,left,displaySurface,2)
    pygame.display.update()
    fpsClock.tick(FPS)