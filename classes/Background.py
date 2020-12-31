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


def add_map(urlListMap):
    res = [0]
    map_size = [(0, 0)]  # map 0 deo co
    color = [[0, 0, 0]]
    for url in urlListMap:
        with open(url) as jsonData:
            dic = {}
            map = json.load(jsonData)
            map_size.append((map['lengthx'] * tile_size * scale, map['lengthy'] * tile_size * scale))
            color.append(map["color"])
            list_object = map['object']
            for object in list_object:
                if object == "animation":
                    dic[object] = {}
                    for items_name in list_object[object]:
                        dic[object][items_name] = list_object[object][items_name]  # {"animation":{"items_name":[pos]}}
                elif object == "background" or object == "ground" or object == "stone":
                    dic[object] = {}
                    for background_name in list_object[object]:
                        dic[object][background_name] = list_object[object][
                            background_name]  # {"background":{"background_name":[pos]}}
                elif object == "reactable":
                    dic[object] = {}
                    for reactable_name in list_object[object]:
                        dic[object][reactable_name] = list_object[object][reactable_name]
                res.append(dic)

    return res, map_size, color  # dic{"name_tiles" : [position in map]}


class Background:
    DIRECTION_LEFT = 0
    DIRECTION_RIGHT = 1
    DIRECTION_UP = 2
    DIRECTION_DOWN = 3
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.map, self.map_size, self.color = add_map([
            "./levels/map1_2.json",
            # "./levels/map1_1.json",
            # "./levels/bonus_area_1_1.json"
        ])
        self.index = 1  # defaul map = 1
        # self.wall = self.load_wall()
        self.ground = self.load_ground()
        self.background_and_stone = self.load_background_and_stone()
        self.reactable = self.load_reactable()
        self.items = self.load_items()  # [[pos1],[pos2],..]
        self.screen = screen
        self.dashboard = Dashboard(screen)

    def update(self, player):
        self.check_camera(player)
        self.update_background_and_stone()
        self.update_ground()
        self.update_reactable()
        self.update_coin(tiles)
        self.dashboard.update()
        self.check_on_ground(player)

    def load_reactable(self):
        load_reactable = {}
        if "reactable" in self.map[self.index]:
            for type in self.map[self.index]["reactable"]:
                for i in self.map[self.index]["reactable"][type]:
                    img = pygame.image.load(tiles[type][0])
                    img = img.subsurface(tiles[type][1], tiles[type][2], tiles[type][3][0], tiles[type][3][1])
                    load_reactable[type] = pygame.transform.scale(img, (
                        tiles[type][3][0] * scale, tiles[type][3][1] * scale))
        return load_reactable  # dictionary{"name_tiles" : img}

    def load_ground(self):
        load_ground = {}
        if "ground" in self.map[self.index]:
            for i in self.map[self.index]["ground"]:
                img = pygame.image.load(tiles[i][0])
                img = img.subsurface(tiles[i][1], tiles[i][2], tiles[i][3][0], tiles[i][3][1])
                load_ground[i] = pygame.transform.scale(img, (tiles[i][3][0] * scale, tiles[i][3][1] * scale))
        return load_ground  # dictionary{"name_tiles" : img}

    def load_background_and_stone(self):
        load_background_and_stone = {}
        if "background" in self.map[self.index]:
            for type in self.map[self.index]["background"]:
                for i in self.map[self.index]["background"][type]:
                    img = pygame.image.load(tiles[type][0])
                    img = img.subsurface(tiles[type][1], tiles[type][2], tiles[type][3][0], tiles[type][3][1])
                    load_background_and_stone[type] = pygame.transform.scale(img, (
                        tiles[type][3][0] * scale, tiles[type][3][1] * scale))
        if "stone" in self.map[self.index]:
            for type in self.map[self.index]["stone"]:
                for i in self.map[self.index]["stone"][type]:
                    img = pygame.image.load(tiles[type][0])
                    img = img.subsurface(tiles[type][1], tiles[type][2], tiles[type][3][0], tiles[type][3][1])
                    load_background_and_stone[type] = pygame.transform.scale(img, (
                        tiles[type][3][0] * scale, tiles[type][3][1] * scale))
        return load_background_and_stone  # dictionary{"name_tiles" : img}

    def load_items(self):
        items = {}
        if "animation" in self.map[self.index]:
            img = pygame.image.load('./img/items.png')
            """
            for item in self.map[self.index]["animation"]:
                print("tiles[item]", tiles[item])
                coin.append(Coin(pos[0]*tile_size, pos[1]*tile_size))
            """
        return items

    def update_coin(self, tiles):
        for coin in self.items:
            coin.update(self.x, self.y, tiles, self.screen)

    def update_reactable(self):
        if "reactable" in self.map[self.index]:
            for tiles_name in self.map[self.index]["reactable"]:
                for i in self.map[self.index]["reactable"][tiles_name]:
                    self.screen.blit(self.reactable[tiles_name],
                                     (i[0] * tile_size * scale + self.x, i[1] * tile_size * scale + self.y))

    def update_ground(self):
        if "ground" in self.map[self.index]:
            for tiles_name in self.map[self.index]["ground"]:
                for i in self.map[self.index]["ground"][tiles_name]:
                    for y in range(i[1], i[1] + i[3]):
                        for x in range(i[0], i[0] + i[2]):
                            self.screen.blit(self.ground[tiles_name],
                                             (x * tile_size * scale + self.x, y * tile_size * scale + self.y))

    def update_background_and_stone(self):
        if "background" in self.map[self.index]:
            for tiles_name in self.map[self.index]["background"]:
                for i in self.map[self.index]["background"][tiles_name]:
                    self.screen.blit(self.background_and_stone[tiles_name],
                                     (i[0] * tile_size * scale + self.x, i[1] * tile_size * scale + self.y))
        if "stone" in self.map[self.index]:
            for tiles_name in self.map[self.index]["stone"]:
                for i in self.map[self.index]["stone"][tiles_name]:
                    self.screen.blit(self.background_and_stone[tiles_name],
                                     (i[0] * tile_size * scale + self.x, i[1] * tile_size * scale + self.y))

    def check_camera(self, player):
        x_camera = player.x - (w - tile_size * scale) / 2
        if x_camera < 0:
            x_camera = 0
        if x_camera + w >= self.map_size[self.index][0]:
            x_camera = self.map_size[self.index][0] - w
        self.x = -x_camera

    def check_on_ground(self, player):
        if "ground" in self.map[self.index]:
            for ground_name in self.map[self.index]["ground"]:
                on_ground, rect, direction = rect_collision(player, self.map[self.index]["ground"][ground_name])
                if on_ground:
                    player.y = rect[1] * tile_size * scale - tile_size * scale * (2 if player.level == 1 else 1)
                    # if direction == Background.DIRECTION_UP:
                    #     player.y = rect[1] * tile_size * scale - tile_size * scale * (2 if player.level == 1 else 1)
                    # elif direction == Background.DIRECTION_DOWN:
                    #     player.y = rect[1] + rect[3]
                    # elif direction == Background.DIRECTION_RIGHT:
                    #     player.x = rect[0] + rect[2]
                    # else:
                    #     player.x = rect[0]
                    if player.state == Mario.IN_AIR:
                        player.state = Mario.IDLE
                else:
                    if player.state != Mario.IN_AIR:
                        player.state = Mario.IN_AIR
                        print("roi")

def rect_collision(player, list_rect):
    size = tile_size * scale
    rect1 = [player.x, player.y, size, size * (2 if player.level == 1 else 1)]
    for rect2 in list_rect:
        if rect1[0] <= rect2[0] * size + rect2[2] * size and rect2[0] * size <= rect1[0] + rect1[2] and rect1[1] <= \
                rect2[1] * size + rect2[3] * size and \
                rect2[1] * size <= rect1[1] + rect1[3]:
            if player.cur_fall_speed > 0:
                player.cur_fall_speed = 0
                direction = Background.DIRECTION_UP
            elif player.cur_fall_speed < 0:
                direction = Background.DIRECTION_DOWN
            elif player.direction == Mario.DIRECTION_LEFT:
                direction = Background.DIRECTION_LEFT
            else:
                direction = Background.DIRECTION_RIGHT
            return True, rect2, direction
    return False, [], 0
