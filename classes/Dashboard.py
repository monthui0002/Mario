import time

import pygame

from classes.Constants import *


class Dashboard:

    def __init__(self, screen, lvl_name):
        self.state = "mario"
        self.screen = screen
        self.level_name = lvl_name
        self.point = 0
        self.coins = 0
        self.time = time.time()
        coin = pygame.image.load('./img/items.png')
        self.coin = [pygame.transform.scale(coin.subsurface(0, 160, 7, 8), (14, 16)),
                     pygame.transform.scale(coin.subsurface(8, 160, 7, 8), (14, 16)),
                     pygame.transform.scale(coin.subsurface(16, 160, 7, 8), (14, 16))]
        self.coin_img = self.coin[0]
        self.index = 0

    def update(self):
        self.draw_text("MARIO", 25, 20, 15)
        self.draw_text(self.point_string(), 25, 37, 15)

        self.screen.blit(self.coin_img, (int(w / 4), 37))
        self.draw_text("x {}".format(self.coin_string()), int(w / 4) + 25, 37, 16)

        self.draw_text("WORLD", int(w / 2) + 25, 20, 15)
        self.draw_text(str(self.level_name), int(w / 2) + 40, 37, 15)

        self.draw_text("TIME", int(3 * w / 4) + 25, 20, 15)
        if self.state != "menu":
            self.update_time()
            self.draw_text(self.time_string(), int(3 * w / 4) + 17, 37, 15)

    def draw_text(self, text, x, y, size):
        my_font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = my_font.render(text, False, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def coin_string(self):
        return "{:02d}".format(self.coins)

    def point_string(self):
        return "{:06d}".format(self.point)

    def time_string(self):
        delta_time = int(time.time() - self.time)
        return "{:02d}:{:02d}:{:02d}".format(delta_time // 3600, (delta_time - delta_time // 3600) // 60,
                                             delta_time % 60)

    def update_time(self):
        self.index += 5 / FPS if self.index < 2 else -self.index
        self.coin_img = self.coin[int(self.index)]
