import pygame

from classes.Input import get

tile_size = 16
scale = 2
w, h = (25 * tile_size * scale, 14 * tile_size * scale)
FPS = 60


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
    FALL_SPEED = 3
    IMAGE = pygame.image.load("./img/mario.png")

    def __init__(self, x, y, direction, level, state, screen):
        self.x, self.y = x, y
        self.small_img, self.big_img = load_img()
        self.direction = direction
        self.level = level
        self.state = state
        self.key_input = {"Enter": False, "Up": False, "Right": False, "Down": False, "Left": False, "Escape": False}
        self.screen = screen
        self.cur_frame = 0
        self.cur_fall_speed = Mario.FALL_SPEED
        self.cur_img = self.small_img if self.level == 0 else self.big_img
        self.grow_lvl = 0
        self.pause = False

    def get_input(self):
        self.key_input = get(self.key_input)

    def update(self, background):
        self.get_input()
        self.move()
        self.check_out_range(background)
        self.render(background)
        # for coin in background.coin:
        #     if self.rect_collision(coin):
        #         background.coin.remove(coin)
        #         print("coin + 1")  # dashboard.coin + 1

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
            if self.state == Mario.IDLE:
                self.state = Mario.WALK

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
            land_condition = self.y > h - tile_size * scale * (2 if self.level == 1 else 1)
            if land_condition:
                if self.level == 0:
                    print("game over! ngu lon chua")
                else:
                    self.state = Mario.SHRINK
                    self.x = 0
                    self.y = 0
                self.state = Mario.IDLE
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

    def render(self, background):
        img = Mario.IMAGE.subsurface(self.cur_img[int(self.cur_frame)][0])
        if self.direction == Mario.DIRECTION_LEFT:
            img = pygame.transform.flip(img, True, False)
        if self.x <= (w - tile_size * scale) / 2:
            pos_x = self.x
        elif self.x + (w + tile_size * scale) / 2 >= background.map_size[background.index][0]:
            pos_x = w - (background.map_size[background.index][0] - self.x)
        else:
            pos_x = (w - tile_size * scale) / 2
        self.screen.blit(
            pygame.transform.scale(img, (tile_size * scale, tile_size * scale * (2 if self.level == 1 else 1))),
            (pos_x, self.y))

    def check_out_range(self, background):
        if self.x < 0:
            self.x = 0
        if self.x + tile_size * scale >= background.map_size[background.index][0]:
            self.x = background.map_size[background.index][0] - tile_size * scale

    def rect_collision(self, entities, size_entities=None):
        if size_entities is None:
            size_entities = [8 * scale, 14 * scale]
        rect1 = [self.x, self.y, tile_size * scale, tile_size * scale]
        rect2 = [entities.x, entities.y, size_entities[0], size_entities[1]]
        return rect1[0] <= rect2[0] + rect2[2] and rect2[0] <= rect1[0] + rect1[2] and rect1[1] <= rect2[1] + rect2[
            3] and rect2[1] <= rect1[1] + rect1[3]
