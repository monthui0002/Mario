import random

import pygame

from boxes.Box import Box
from classes.Constants import *


class RandomBox(Box):

    def __init__(self, img, x, y, t):
        self.img = img
        self.x, self.y = x, y
        self.cur_frame = 0
        self.state = Box.NOT_OPENED
        self.has_coin = random.choice([True, False])
        self.coin_img = []
        if self.has_coin:
            t = t["coin-in-box"]
            img = pygame.image.load(t[0])
            for i in t[2]:
                self.coin_img.append(pygame.transform.scale(img.subsurface(i['x'], i['y'], t[1][0], t[1][1]),
                                                            (t[1][0] * scale, t[1][1] * scale)))
        self.coin_img_idx = 0
        self.w, self.h = tile_size * scale, tile_size * scale
        self.triggered = False
