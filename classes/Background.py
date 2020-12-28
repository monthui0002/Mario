import pygame, json

from classes.Tile import Tile
from entities.Coin import Coin

FPS = 60

tile_size = 16
scale = 2
window_size = (25 * tile_size * scale, 14 * tile_size * scale)

tiles = Tile().tiles
pygame.display.set_caption('MARIO')


def add_map(urlListMap):
    res = [0]
    map_size = [(0, 0)]  # map 0 deo co
    color = [[0,0,0]]
    for url in urlListMap:
        with open(url) as jsonData:
            dic = {}
            map = json.load(jsonData)
            map_size.append((map['lengthx'] * tile_size * scale, map['lengthy'] * tile_size * scale))
            color.append(map["color"])
            list_object = map['object']
            for object in list_object:
                if object == "wall":
                    dic[object] = {}
                    for wall_name in list_object[object]:
                        dic[object][wall_name] = list_object[object][wall_name]  # {"wall":{"wall_name":[pos]}}
                elif object == "items":
                    dic[object] = {}
                    for items_name in list_object[object]:
                        dic[object][items_name] = list_object[object][items_name]  # {"items":{"items_name":[pos]}}
                elif object == "background":
                    dic[object] = {}
                    for background_name in list_object[object]:
                        dic[object][background_name] = list_object[object][
                            background_name]  # {"background":{"background_name":[pos]}}
                res.append(dic)
    return res, map_size,color  # dic{"name_tiles" : [position in map]}


class Background:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.map, self.map_size,self.color = add_map([
            "./levels/map1_1.json",
        ])
        self.index = 1  # defaul map = 1
        self.wall = self.load_wall()
        self.background = self.load_background()
        self.items = self.load_items() # [[pos1],[pos2],..]

    def update(self, screen, player):
        self.check_camera(player)
        self.update_wall(screen)
        self.update_background(screen)
        self.update_coin(tiles,screen)

    def load_wall(self):
        load_wall = {}
        if "wall" in self.map[self.index]:
            # img = pygame.image.load("./img/Tileset.png")
            for i in self.map[self.index]["wall"]:
                img = pygame.image.load(tiles[i][0])
                img = img.subsurface(tiles[i][1], tiles[i][2], tiles[i][3][0], tiles[i][3][1])
                load_wall[i] = pygame.transform.scale(img, (tiles[i][3][0] * scale, tiles[i][3][1] * scale))
        return load_wall  # dictionary{"name_tiles" : img}

    def load_background(self,):
        load_background = {}
        if "background" in self.map[self.index]:
            for i in self.map[self.index]["background"]:
                img = pygame.image.load(tiles[i][0])
                img = img.subsurface(tiles[i][1], tiles[i][2], tiles[i][3][0], tiles[i][3][1])
                load_background[i] = pygame.transform.scale(img, (tiles[i][3][0] * scale, tiles[i][3][1] * scale))
        return load_background  # dictionary{"name_tiles" : img}

    def load_items(self):
        items = {}
        if "items" in self.map[self.index]:
            img = pygame.image.load('./img/items.png')
            for item in self.map[self.index]["items"]:
                print(tiles[item])
                # coin.append(Coin(pos[0]*tile_size, pos[1]*tile_size))
        return items

    def update_coin(self,tiles,screen):
        for coin in self.items:
            coin.update(self.x,self.y,tiles,screen)

    def update_wall(self,screen):
        for tiles_name in self.map[self.index]["wall"]:
            for i in self.map[self.index]["wall"][tiles_name]:
                screen.blit(self.wall[tiles_name], (i[0] * tile_size * scale + self.x, i[1] * tile_size * scale + self.y))

    def update_background(self,screen):
        for tiles_name in self.map[self.index]["background"]:
            for i in self.map[self.index]["background"][tiles_name]:
                screen.blit(self.background[tiles_name], (i[0] * tile_size * scale + self.x, i[1] * tile_size * scale + self.y))

    def check_camera(self, player):
        x_camera = player.x - (window_size[0] - tile_size * scale) / 2
        if x_camera < 0:
            x_camera = 0
        if x_camera + window_size[0] >= self.map_size[self.index][0]:
            x_camera = self.map_size[self.index][0] - window_size[0]
        self.x = -x_camera

