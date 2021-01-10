import pygame

from classes.Input import get
from classes.Constants import *


def load_img():
    small_images = []
    big_images = []
    pos_x = 80
    pos_y = 1
    for i in range(0, 22):
        big_images.append([(pos_x, pos_y, 16, 32), (tile_size * scale, tile_size * scale * 2)])
        if i < 14:
            small_images.append([(pos_x, pos_y + 33, 16, 16), (tile_size * scale, tile_size * scale)])
        pos_x += 17
    return small_images, big_images


class Mario:
    # States
    IDLE = 1
    WALK = 2
    BREAK = 3
    IN_AIR = 4
    SHRINK = 5
    CLIMB = 6
    SWIM = 7
    GROW = 8
    UNDEFINED = 9

    # Constants
    STEP = 5
    DIRECTION_RIGHT = 1
    DIRECTION_LEFT = -1
    GRAVITY = .5
    FALL_SPEED = 0
    IMAGE = pygame.image.load("./img/mario.png")

    def __init__(self, x, y, direction, level, state, screen, background, play_lvl):
        self.x, self.y = x, y
        self.small_img, self.big_img = load_img()
        self.direction = direction
        self.level = level
        self.play_lvl = play_lvl
        self.state = state
        self.key_input = {"Enter": False, "Up": False, "Right": False, "Down": False, "Left": False, "Escape": False}
        self.screen = screen
        self.cur_frame = 0
        self.cur_fall_speed = Mario.FALL_SPEED
        self.cur_img = self.small_img if self.level == 0 else self.big_img
        self.grow_lvl = 0
        self.pause = False
        self.background = background

    def get_input(self):
        self.key_input = get(self.key_input)

    def update(self):
        self.get_input()
        self.move()
        self.background.check_out_range()
        self.render()

    def move(self):
        if self.key_input["Enter"] and (self.grow_lvl == 0 or self.grow_lvl == 2):
            self.key_input["Enter"] = False
            if self.level == 0:
                self.state = Mario.GROW
                print("Grow")
            else:
                print("Shrink")
                self.state = Mario.SHRINK

        moving = self.key_input["Right"] or self.key_input["Left"]
        if moving:
            self.x += self.direction * Mario.STEP
            self.direction = Mario.DIRECTION_LEFT if self.key_input["Left"] else Mario.DIRECTION_RIGHT
            if self.direction == Mario.DIRECTION_LEFT:
                self.play_lvl.check_collision_left(self)
            else:
                self.play_lvl.check_collision_right(self)
            if self.state == Mario.IDLE:
                self.state = Mario.WALK
            lol, _ = self.play_lvl.check_collision(self)
            if not lol:
                self.state = Mario.IN_AIR
        if self.key_input["Up"] and self.state != Mario.IN_AIR:
            self.cur_fall_speed = -6 * scale
            self.state = Mario.IN_AIR

        if self.state == Mario.IDLE:
            self.cur_frame = 0
        elif self.state == Mario.WALK:
            if moving:
                if int(self.cur_frame) > 3 or int(self.cur_frame) < 1:
                    self.cur_frame = 1
                elif int(self.cur_frame + 7 / FPS) <= 3:
                    self.cur_frame += 7 / FPS
                else:
                    self.cur_frame = 1
            else:
                self.state = Mario.IDLE
        elif self.state == Mario.IN_AIR:
            self.cur_frame = 5
            self.y += self.cur_fall_speed
            self.cur_fall_speed += Mario.GRAVITY
            if self.cur_fall_speed > 0:
                self.play_lvl.check_collision_bottom(self)
            else:
                self.play_lvl.check_collision_top(self)
            if self.y > h:
                print("Ngu")
                self.x = 0
                self.y = 0
                self.state = Mario.IN_AIR
                self.cur_fall_speed = Mario.FALL_SPEED
        elif self.state == Mario.SWIM:
            pass
        elif self.state == Mario.GROW and self.grow_lvl < 2:
            if self.grow_lvl == 0:
                self.y -= tile_size * scale
            self.grow_lvl += 8 / FPS
            self.cur_img = self.big_img
            self.cur_frame = 15
            self.level = 1
            if int(self.grow_lvl) == 2:
                self.grow_lvl = 2
                self.state = Mario.IDLE
                self.cur_frame = 0
        elif self.state == Mario.SHRINK:
            if self.level == 1:
                self.grow_lvl -= 8 / FPS
                self.cur_frame = 15
                if int(self.grow_lvl) == 0:
                    self.level = 0
                    self.grow_lvl = 0
                    self.state = Mario.IDLE
                    self.y += tile_size * scale
                    self.cur_frame = 0
                    self.cur_img = self.small_img
            else:
                print("Game over here!")

    def render(self):
        img = Mario.IMAGE.subsurface(self.cur_img[int(self.cur_frame)][0])
        if self.direction == Mario.DIRECTION_LEFT:
            img = pygame.transform.flip(img, True, False)
        if self.x <= (w - tile_size * scale) / 2:
            pos_x = self.x
        elif self.x + (w + tile_size * scale) / 2 >= self.background.w:
            pos_x = w - (self.background.w - self.x)
        else:
            pos_x = (w - tile_size * scale) / 2
        self.screen.blit(
            pygame.transform.scale(img, (tile_size * scale, tile_size * scale * (2 if self.level == 1 else 1))),
            (pos_x, self.y))
