import pygame
from classes.Constants import *

class Dashboard():
    coin = pygame.image.load('./img/items.png')
    coin1 = coin.subsurface(0, 160, 7, 8)
    coin2 = coin.subsurface(8, 160, 7, 8)
    coin3 = coin.subsurface(16, 160, 7, 8)
    coin = [pygame.transform.scale(coin1, (14, 16)), pygame.transform.scale(coin2, (14, 16)),
            pygame.transform.scale(coin3, (14, 16))]

    def __init__(self, screen):
        self.state = "mario"
        self.screen = screen
        self.levelName = "1-1"
        self.points = 0
        self.coins = 0
        self.ticks = 0
        self.time = 0
        self.coin_img = Dashboard.coin[0]
        self.index = 0

    # myfont = pygame.font.Font('freesansbold.ttf', 32)
    def update(self):

        self.drawText("MARIO", 17, 20, 15)
        self.drawText(self.pointString(), 17, 37, 15)

        self.screen.blit(self.coin_img, (int(w / 4), 37))
        self.drawText("x {}".format(self.coinString()), int(w / 4) + 17, 37, 16)

        self.drawText("WORLD", int(w / 2) + 17, 20, 15)
        self.drawText(str(self.levelName), int(w / 2) + 34, 37, 15)

        self.drawText("TIME", int(3 * w / 4) + 17, 20, 15)
        if self.state != "menu":
            self.update_time()
            self.drawText(self.timeString(), int(3 * w / 4) + 7, 37, 15)

    def drawText(self, text, x, y, size):
        myfont = pygame.font.Font('freesansbold.ttf', size)
        textsurface = myfont.render(text, False, (255, 255, 255))
        self.screen.blit(textsurface, (x, y))

    def coinString(self):
        return "{:02d}".format(self.coins)

    def pointString(self):
        return "{:06d}".format(self.points)

    def timeString(self):
        return "{:02d}:{:02d}:{:02d}".format(self.time // 3600, (self.time % 3600) // 60, (self.time % 3600) % 60)

    def update_time(self):
        self.ticks += 1
        if self.ticks == 60:
            self.ticks = 0
            self.time += 1

        if self.ticks % 10 == 0:
            self.index += 1 if self.index < 2 else -self.index
            self.coin_img = Dashboard.coin[self.index]
