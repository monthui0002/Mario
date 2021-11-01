import random

import pygame

from boxes.Box import Box
from classes.Constants import *


class HiddenBox(Box):

    def __init__(self, img, x, y, t):
        self.img = img
        self.x, self.y = x, y
        self.cur_frame = 0
        self.state = Box.NOT_OPENED
        self.has_item = random.choice([True, False, False])
        self.item_type = Box.ITEM_COIN
        self.item_img = []
        self.item_name = "coin-in-box"
        if self.has_item:
            t = t[self.item_name]
            img = pygame.image.load(t[0])
            for i in t[2]:
                self.item_img.append(pygame.transform.scale(img.subsurface(i['x'], i['y'], t[1][0], t[1][1]),
                                                            (t[1][0] * scale, t[1][1] * scale)))
        self.item_img_idx = 0
        self.w, self.h = tile_size * scale, tile_size * scale
        self.triggered = False
