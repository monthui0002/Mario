import pygame

from classes.Constants import *


class Dashboard:

    def __init__(self, screen, lvl_name):
        self.state = "mario"
        self.screen = screen
        self.level_name = lvl_name
        self.point = 0
        self.coins = 0
        self.time = 0
        coin = pygame.image.load('./img/items.png')
        self.coin = [pygame.transform.scale(coin.subsurface(0, 160, 7, 8), (14, 16)),
                     pygame.transform.scale(coin.subsurface(8, 160, 7, 8), (14, 16)),
                     pygame.transform.scale(coin.subsurface(16, 160, 7, 8), (14, 16))]
        self.coin_img = self.coin[0]
        self.index = 0

    def update(self):
        self.drawText("MARIO", 25, 20, 15)
        self.drawText(self.pointString(), 25, 37, 15)

        self.screen.blit(self.coin_img, (int(w / 4), 37))
        self.drawText("x {}".format(self.coinString()), int(w / 4) + 25, 37, 16)

        self.drawText("WORLD", int(w / 2) + 25, 20, 15)
        self.drawText(str(self.level_name), int(w / 2) + 40, 37, 15)

        self.drawText("TIME", int(3 * w / 4) + 25, 20, 15)
        if self.state != "menu":
            self.update_time()
            self.drawText(self.timeString(), int(3 * w / 4) + 17, 37, 15)

    def drawText(self, text, x, y, size):
        my_font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = my_font.render(text, False, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def coinString(self):
        return "{:02d}".format(self.coins)

    def pointString(self):
        return "{:06d}".format(self.point)

    def timeString(self):
        return "{:02d}:{:02d}:{:02d}".format(self.time // 3600, (self.time % 3600) // 60, (self.time % 3600) % 60)

    def update_time(self):
        self.index += 5 / FPS if self.index < 2 else -self.index
        self.coin_img = self.coin[int(self.index)]
