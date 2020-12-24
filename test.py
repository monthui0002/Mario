import pygame, sys
from classes.Mario import Mario
from classes.Background import Background

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()


# mario = pygame.image.load('./mario.png')
# mario = mario.subsurface((80, 34, 16, 16))
# mario = pygame.transform.scale(mario, (32, 32))
# DISPLAYSURF.blit(self.img, (int(self.x), int(self.y)))

tile_size = 16
window_size = (25*tile_size, 14*tile_size) #25*14

x = 0
y = 0
background = Background(x,y)

display_surface = pygame.display.set_mode(window_size)
bg = pygame.transform.scale(display_surface, background.map_size[1])
pygame.display.set_caption('MARIO')

mario = Mario(0,0,"sound",display_surface,2)

i = 0
while True:
    display_surface = pygame.display.set_mode(window_size)
    background.update(display_surface,mario)
    # mario.updateImage(display_surface,2)
    mario.update(display_surface)
    # img = pygame.image.load("./img/Tileset.png")
    # img = img.subsurface(80,144,16,16)
    # img = pygame.transform.scale(img, (16,16))
    # display_surface.blit(img,(16, 112))
    pygame.display.update()
    # background.x -= 1
    fpsClock.tick(FPS)