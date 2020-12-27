import pygame
from classes.Tile import Tile
FPS = 60

scale = 2


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.index = 0
        self.type = "Item"
        self.size = [8,14]

    def update(self,x,y, tiles, screen):  # index 1-3
        coin = tiles["coin"]  # [url,pos]
        self.size = coin[1]
        pos = coin[2][int(self.index)]
        self.index += 1 / (FPS/6) if self.index < (4 - (1/(FPS/6))) else -self.index
        img = pygame.image.load(coin[0])
        img = img.subsurface(pos["x"], pos["y"], self.size[0], self.size[1])
        img = pygame.transform.scale(img, (self.size[0] * scale, self.size[1] * scale))
        screen.blit(img, (self.x + x, self.y + y))
