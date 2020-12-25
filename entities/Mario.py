import pygame
from classes.Input import Input

window_size = (800, 448)
mario_size = 32

IDLE = 0
RUN = 1
JUMP = 2
SIT = 3
SWIM = 4
GRASP = 5
CLIMB = 6
GRAVITY = .5

RIGHT = 0
LEFT = 1

JUMP_HEIGHT = 48


class Mario:
    def __init__(self, x, y, sound, screen, inAir=False, level=1, direction=RIGHT):
        self.x = x
        self.y = y
        self.input = Input(self)
        self.level = level
        self.state = IDLE
        self.sound = sound  # sound chưa có
        self.direction = direction
        self.screen = screen
        self.inAir = inAir
        self.small, self.big = self.load_images()
        self.speed = 2
        self.pos = x

    def load_images(self):
        small_images = []
        big_images = []
        pos_x = 80
        pos_y = 1
        for i in range(0, 22):
            big_images.append([(pos_x, pos_y, 16, 32), (32, 64)])
            if i < 14: small_images.append([(pos_x, pos_y + 33, 16, 16), (32, 32)])
            pos_x += 17
        return small_images, big_images

    def update(self, screen, run_index, img=pygame.image.load("./img/mario.png")):
        self.state, self.direction = self.input.check(self.state, self.direction)
        image = self.small if self.level == 1 else self.big
        if self.state == IDLE:
            img = img.subsurface(image[IDLE][0])
            img = pygame.transform.scale(img, image[IDLE][1])
            global GRAVITY
            GRAVITY = .75
        elif self.state == RUN:
            img = img.subsurface(image[RUN + int(run_index)][0])
            img = pygame.transform.scale(img, image[RUN + int(run_index)][1])
            if self.direction:
                self.turn_left()
            else:
                self.turn_right()
        elif self.state == JUMP:
            img = img.subsurface(image[JUMP + 3][0])
            img = pygame.transform.scale(img, image[JUMP + 3][1])
            self.jump()
        else:
            if self.level == 2:
                img = img.subsurface(image[SIT + 3][0])
                img = pygame.transform.scale(img, image[SIT + 3][1])
            else:
                img = img.subsurface(image[IDLE][0])
                img = pygame.transform.scale(img, image[IDLE][1])
        if self.direction: img = pygame.transform.flip(img, True, False)
        self.check()
        screen.blit(img, (self.pos, self.y))

    def turn_right(self):
        global GRAVITY
        self.x += self.speed * GRAVITY
        self.pos = self.x if self.x < (window_size[0] - 32) / 2 else (window_size[0] - 32) / 2
        if self.state == RUN:
            if GRAVITY < 1:
                GRAVITY += 0.005
        else:
            GRAVITY = 0.5

    def turn_left(self):
        global GRAVITY
        self.x -= self.speed * GRAVITY
        self.pos = self.x if self.x < (window_size[0] - 32) / 2 else (window_size[0] - 32) / 2
        if self.state == RUN:
            if GRAVITY < 1:
                GRAVITY += 0.005
        else:
            GRAVITY = 0.5

    def jump(self):
        self.y -= JUMP_HEIGHT
        self.inAir = True
        self.state = IDLE

    def check(self):
        if self.x < 0:
            self.x = 0
        # if self.x + 16 > window_size[0]:
        #     self.x = window_size[0] - 16
        if self.y > window_size[1]:
            print("game over")
            return
