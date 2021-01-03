import json

import pygame

from classes.Dashboard import Dashboard
from classes.Tile import Tile
from entities.Mario import Mario

FPS = 60
tile_size = 16
scale = 2
w, h = (16 * tile_size * scale, 14 * tile_size * scale)

tiles = Tile().tiles


def load_map_data(url_list):
    map_data_list = [None]
    map_sizes = [(0, 0)]
    bg_colors = [[0, 0, 0]]
    for url in url_list:
        with open(url) as jsonData:
            map_data = json.load(jsonData)
            map_sizes.append((map_data['length-x'] * tile_size * scale, map_data['length-y'] * tile_size * scale))
            bg_colors.append(map_data['color'])
            map_data_list.append(map_data['object'])
    return map_data_list, map_sizes, bg_colors


class Background:
    DIRECTION_LEFT = 0
    DIRECTION_RIGHT = 1
    DIRECTION_UP = 2
    DIRECTION_DOWN = 3

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.map, self.map_size, self.color = load_map_data([
            "./levels/map1_1.json",
            "./levels/bonus_area_1_1.json"
        ])
        self.index = 1  # default map = 1
        self.ground = self.load_ground()
        self.background_and_stones = self.load_background_and_stones()
        self.reactables = self.load_reactables()
        self.items = self.load_items()  # [[pos1],[pos2],..]
        self.screen = screen
        self.dashboard = Dashboard(screen)
        self.character = None

    def set_character(self, c):
        self.character = c

    def update(self):
        self.update_camera()
        self.update_background_and_stones()
        self.update_ground()
        self.update_reactables()
        self.update_coins(tiles)
        self.dashboard.update()
        self.check_on_ground()

    def load_reactables(self):
        reactables = {}
        if "reactable" in self.map[self.index]:
            for reactable_type in self.map[self.index]["reactable"]:
                img = pygame.image.load(tiles[reactable_type][0])
                img = img.subsurface(tiles[reactable_type][1], tiles[reactable_type][2],
                                     tiles[reactable_type][3][0], tiles[reactable_type][3][1])
                reactables[reactable_type] = pygame.transform.scale(img, (
                    tiles[reactable_type][3][0] * scale, tiles[reactable_type][3][1] * scale))
        return reactables  # dictionary{"name_tiles" : img}

    def load_ground(self):
        load_ground = {}
        if "ground" in self.map[self.index]:
            for ground_type in self.map[self.index]["ground"]:
                img = pygame.image.load(tiles[ground_type][0])
                img = img.subsurface(tiles[ground_type][1], tiles[ground_type][2], tiles[ground_type][3][0],
                                     tiles[ground_type][3][1])
                load_ground[ground_type] = pygame.transform.scale(img, (
                    tiles[ground_type][3][0] * scale, tiles[ground_type][3][1] * scale))
        return load_ground  # dictionary{"name_tiles" : img}

    def load_background_and_stones(self):
        load_background_and_stone = {}
        if "background" in self.map[self.index]:
            for background_type in self.map[self.index]["background"]:
                img = pygame.image.load(tiles[background_type][0])
                img = img.subsurface(tiles[background_type][1], tiles[background_type][2],
                                     tiles[background_type][3][0], tiles[background_type][3][1])
                load_background_and_stone[background_type] = pygame.transform.scale(img, (
                    tiles[background_type][3][0] * scale, tiles[background_type][3][1] * scale))
        if "stone" in self.map[self.index]:
            for stone_type in self.map[self.index]["stone"]:
                img = pygame.image.load(tiles[stone_type][0])
                img = img.subsurface(tiles[stone_type][1], tiles[stone_type][2], tiles[stone_type][3][0],
                                     tiles[stone_type][3][1])
                load_background_and_stone[stone_type] = pygame.transform.scale(img, (
                    tiles[stone_type][3][0] * scale, tiles[stone_type][3][1] * scale))
        return load_background_and_stone  # dictionary{"name_tiles" : img}

    def load_items(self):
        items = {}
        return items

    def update_coins(self, tiles_list):
        for coin in self.items:
            coin.update(self.x, self.y, tiles_list, self.screen)

    def update_reactables(self):
        if "reactable" in self.map[self.index]:
            for tiles_name in self.map[self.index]["reactable"]:
                for i in self.map[self.index]["reactable"][tiles_name]:
                    self.screen.blit(self.reactables[tiles_name],
                                     (i[0] * tile_size * scale + self.x, i[1] * tile_size * scale + self.y))

    def update_ground(self):
        if "ground" in self.map[self.index]:
            for tiles_name in self.map[self.index]["ground"]:
                for i in self.map[self.index]["ground"][tiles_name]:
                    for y in range(i[1], i[1] + i[3]):
                        for x in range(i[0], i[0] + i[2]):
                            self.screen.blit(self.ground[tiles_name],
                                             (x * tile_size * scale + self.x, y * tile_size * scale + self.y))

    def update_background_and_stones(self):
        if "background" in self.map[self.index]:
            for tiles_name in self.map[self.index]["background"]:
                for i in self.map[self.index]["background"][tiles_name]:
                    self.screen.blit(self.background_and_stones[tiles_name],
                                     (i[0] * tile_size * scale + self.x, i[1] * tile_size * scale + self.y))
        if "stone" in self.map[self.index]:
            for tiles_name in self.map[self.index]["stone"]:
                for i in self.map[self.index]["stone"][tiles_name]:
                    self.screen.blit(self.background_and_stones[tiles_name],
                                     (i[0] * tile_size * scale + self.x, i[1] * tile_size * scale + self.y))

    def update_camera(self):
        x_camera = self.character.x - (w - tile_size * scale) / 2
        if x_camera < 0:
            x_camera = 0
        if x_camera + w >= self.map_size[self.index][0]:
            x_camera = self.map_size[self.index][0] - w
        self.x = -x_camera

    def check_on_ground(self):
        if "ground" in self.map[self.index]:
            for ground_name in self.map[self.index]["ground"]:
                on_ground, rect, direction = self.rect_collision(self.map[self.index]["ground"][ground_name])
                if on_ground:
                    self.character.y = rect[1] * tile_size * scale - tile_size * scale * (
                        2 if self.character.level == 1 else 1)
                    if self.character.state == Mario.IN_AIR:
                        self.character.state = Mario.IDLE
                else:
                    if self.character.state != Mario.IN_AIR:
                        self.character.state = Mario.IN_AIR

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
