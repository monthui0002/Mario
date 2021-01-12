from classes.Constants import *
from entities.Mario import Mario


class Background:
    DIRECTION_LEFT = 0
    DIRECTION_RIGHT = 1
    DIRECTION_UP = 2
    DIRECTION_DOWN = 3

    def __init__(self, x, y, screen, level):
        self.x = x
        self.y = y
        self.level = level
        self.w, self.h = level.map_size[0], level.map_size[1]
        self.screen = screen
        self.character = None

    def set_character(self, c):
        self.character = c

    def update(self):
        self.update_camera()
        self.level.update(self.x, self.y)

    def update_camera(self):
        x_camera = self.character.x - (w - tile_size * scale) / 2
        if x_camera < 0:
            x_camera = 0
        if x_camera + w >= self.w:
            x_camera = self.w - w
        self.x = -x_camera

    def rect_collision(self, list_rect):
        size = tile_size * scale
        rect1 = [self.character.x, self.character.y, size, size * (2 if self.character.level == 1 else 1)]
        direction = Background.DIRECTION_UP
        for rect2 in list_rect:
            if rect1[0] <= rect2[0] * size + rect2[2] * size and rect2[0] * size <= rect1[0] + rect1[2] and rect1[1] <= \
                    rect2[1] * size + rect2[3] * size and \
                    rect2[1] * size <= rect1[1] + rect1[3]:
                if self.character.cur_fall_speed > 0:
                    self.character.cur_fall_speed = 0
                    direction = Background.DIRECTION_UP
                elif self.character.cur_fall_speed < 0:
                    direction = Background.DIRECTION_DOWN
                elif self.character.direction == Mario.DIRECTION_LEFT:
                    direction = Background.DIRECTION_LEFT
                else:
                    direction = Background.DIRECTION_RIGHT
                return True, rect2, direction
        return False, [], direction

    def check_out_range(self):
        if self.character.x < 0:
            self.character.x = 0
        if self.character.x + tile_size * scale >= self.w:
            print("Win")
            self.character.x = self.w - tile_size * scale
