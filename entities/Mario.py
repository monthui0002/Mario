import pygame
from classes.Input import Input

tile_size = 16
scale = 2
window_size = (25 * tile_size * scale, 14 * tile_size * scale)

RUNWITHJUMP = -1
IDLE = 0
RUN = 1
PREPARE = 4
JUMP = 5
SIT = 6
CLIMB = 7
GRASP = 8  # win
SWIM = 9
GRAVITY = .5

RIGHT = 0
LEFT = 1

MAX_JUMP_HEIGHT = 6 * tile_size * scale
SPEED_RUN = 1
JUMP_HEIGHT = 16
MAX_SPEED = 5
V_X = 0.5
V_Y = 16 / 3
mario_image = pygame.image.load("./img/mario.png")


class Mario:
    def __init__(self, x, y, sound, screen, in_air=False, level=1, direction=RIGHT):
        self.x = x
        self.y = y
        self.input = Input()
        self.level = level
        self.state = IDLE
        self.sound = sound  # sound chưa có
        self.direction = direction
        self.screen = screen
        self.in_air = in_air
        self.small, self.big = self.load_images()
        self.speed_run = SPEED_RUN
        self.jump_height = JUMP_HEIGHT
        self.pause = False
        self.is_climbing = False
        self.is_swimming = False

    def load_images(self):
        small_images = []
        big_images = []
        pos_x = 80
        pos_y = 1
        for i in range(0, 22):
            big_images.append([(pos_x, pos_y, 16, 32), (tile_size * scale, tile_size * scale * 2)])
            if i < 14: small_images.append([(pos_x, pos_y + 33, 16, 16), (tile_size * scale, tile_size * scale)])
            pos_x += 17
        return small_images, big_images

    def update(self, screen, background, index):
        key_press = self.input.check(
            [0,
             self.state == RUN and self.direction == LEFT,
             self.state == RUN and self.direction == RIGHT,
             self.state == JUMP,
             self.state == SIT
             ]
        )
        self.check_state(key_press)
        self.check_direction(key_press)
        img = self.check_image(index)
        if self.direction: img = pygame.transform.flip(img, True, False)
        self.check(background)
        if self.x <= (window_size[0] - tile_size * scale) / 2:
            pos_x = self.x
        elif self.x + (window_size[0] - tile_size * scale) / 2 >= background.map_size[background.index][0] * scale:
            pos_x = (window_size[0] - tile_size * scale) - (background.map_size[background.index][0] * scale - self.x)
        else:
            pos_x = (window_size[0] - tile_size * scale) / 2
        screen.blit(img, (pos_x, self.y))

    def check_direction(self, key_press):
        if key_press[1]:
            self.direction = LEFT
        elif key_press[2]:
            self.direction = RIGHT

    def check_state(self, key_press):
        if key_press[3] and (key_press[1] or key_press[2]):
            self.state = RUNWITHJUMP
        elif key_press[3]:
            self.state = JUMP
        elif key_press[1] or key_press[2]:
            self.state = RUN
        elif not key_press[1] and not key_press[2]:
            if key_press[4]:
                self.state = SIT if self.level == 2 else IDLE
            else:
                self.state = IDLE
    def check_image(self,index):
        image = self.small if self.level == 1 else self.big
        if self.state == RUNWITHJUMP:
            print("run and jump")
            img = mario_image.subsurface(image[JUMP][0])
            res = pygame.transform.scale(img, image[JUMP][1])
            self.jump()
            if self.direction:
                self.turn_left()
            else:
                self.turn_right()
        elif self.state == IDLE:
            self.speed_jump = 0
            img = mario_image.subsurface(image[IDLE][0])
            res = pygame.transform.scale(img, image[IDLE][1])
            self.speed_run = SPEED_RUN
        elif self.state == RUN:
            img = mario_image.subsurface(image[RUN + int(index)][0])
            res = pygame.transform.scale(img, image[RUN + int(index)][1])
            if self.direction:
                self.turn_left()
            else:
                self.turn_right()
        elif self.state == JUMP:
            img = mario_image.subsurface(image[JUMP][0])
            res = pygame.transform.scale(img, image[JUMP][1])
            self.jump()
        else:  # them cac animation con lai sau
            if self.level == 2:
                img = mario_image.subsurface(image[SIT][0])
                res = pygame.transform.scale(img, image[SIT + 3][1])
            else:
                img = mario_image.subsurface(image[IDLE][0])
                res = pygame.transform.scale(img, image[IDLE][1])
        return res

    def turn_right(self):
        self.x += self.speed_run
        if self.speed_run <= MAX_SPEED: self.speed_run += V_X

    def turn_left(self):
        self.x -= self.speed_run
        if self.speed_run <= MAX_SPEED: self.speed_run += V_X

    def jump(self):
        self.in_air = False
        if self.jump_height + V_Y <= MAX_JUMP_HEIGHT:
            self.jump_height += V_Y
            self.y -= V_Y
            print(self.jump_height)
        else:
            print("???", self.jump_height)
            self.state = IDLE
            self.jump_height = JUMP_HEIGHT
            self.in_air = True

    def run_with_jump(self):
        self.in_air = False
        if self.jump_height < MAX_JUMP_HEIGHT:
            self.jump_height += V_Y
            self.y -= V_Y
        else:
            self.state = IDLE
            self.jump_height = JUMP_HEIGHT
            self.in_air = True
        if self.direction == RIGHT:
            self.x += self.speed_run
            if self.speed_run <= MAX_SPEED: self.speed_run += V_X
        else:
            self.x -= self.speed_run
            if self.speed_run <= MAX_SPEED: self.speed_run += V_X

    def check(self, backround):
        if self.x < 0:
            self.x = 0
        if self.x >= backround.map_size[backround.index][0] * scale:
            self.x = backround.map_size[backround.index][0] * scale
        if self.in_air:
            if self.y < window_size[1] - tile_size * scale:
                self.y += V_Y
        if self.y > window_size[1]:
            print("game over")
            return
