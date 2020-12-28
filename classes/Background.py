import pygame, json

from classes.Tile import Tile
from entities.Coin import Coin

FPS = 60

tile_size = 16
scale = 2
window_size = (25 * tile_size * scale, 14 * tile_size * scale)

tiles = Tile().tiles
pygame.display.set_caption('MARIO')


class Background:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.map, self.map_size = self.add_map([
            "./levels/map1_2.json",
        ])
        self.index = 1  # defaul map = 1
        self.wall = self.load_wall()
        self.coin = self.load_coin() # [[pos1],[pos2],..]

    def update(self, screen, player):
        self.check_camera(player)
        self.update_wall(screen)
        self.update_coin(tiles,screen)

    def add_map(self, urlListMap):
        dic = {}
        map_size = [(0, 0)]  # map 0 deo co
        for url in urlListMap:
            with open(url) as jsonData:
                map = json.load(jsonData)
                map_size.append((map['lengthx']*tile_size*scale, map['lengthy']*tile_size*scale))
                list_object = map['object']
                for object in list_object:
                    if object == "wall":
                        dic[object] = {}
                        for wall_name in list_object[object]:
                            dic[object][wall_name] = list_object[object][wall_name]  # {"wall":{"wall_name":[pos]}}
                    elif object == "animation":
                        dic[object] = list_object[object]  # {"animation:[[pos1][pos2]...]}
        return dic, map_size  # dic{"name_tiles" : [position in map]}

    def load_wall(self):
        print(tiles)
        print(self.map)
        load_wall = {}
        # img = pygame.image.load("./img/Tileset.png")
        for i in self.map["wall"]:
            img = pygame.image.load(tiles[i][0])
            img = img.subsurface(tiles[i][1], tiles[i][2], tiles[i][3][0], tiles[i][3][1])
            load_wall[i] = pygame.transform.scale(img, (tiles[i][3][0] * scale, tiles[i][3][1] * scale))
        return load_wall  # dictionary{"name_tiles" : img}

    def check_camera(self, player):
        x_camera = player.x - (window_size[0] - tile_size * scale) / 2
        if x_camera < 0:
            x_camera = 0
        if x_camera + window_size[0] >= self.map_size[self.index][0]:
            x_camera = self.map_size[self.index][0] - window_size[0]
        self.x = -x_camera

    def load_coin(self):
        coin = []
        for pos in self.map["animation"]:
            coin.append(Coin(pos[0]*tile_size, pos[1]*tile_size))
        return coin
    def update_coin(self,tiles,screen):
        for coin in self.coin:
            coin.update(self.x,self.y,tiles,screen)
    def update_wall(self,screen):
        for tiles_name in self.map["wall"]:
            for i in self.map["wall"][tiles_name]:
                screen.blit(self.wall[tiles_name], (i[0] * tile_size * scale + self.x, i[1] * tile_size * scale + self.y))
