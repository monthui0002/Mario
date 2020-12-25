import pygame, json

from classes.Tile import Tile
tile_size = 16
scale = 2
window_size = (25*tile_size*scale, 14*tile_size*scale)

tiles = Tile().tiles
pygame.display.set_caption('MARIO')


class Background:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.map, self.map_size = self.addMaps([
            "./levels/map1.json",
        ])
        self.index = 1  # defaul map = 1
        self.images = self.loadMaps()

    def addMaps(self, urlListMap):
        dic = {}
        map_size = [(0, 0)]  # map 0 deo co
        for url in urlListMap:
            with open(url) as jsonData:
                map = json.load(jsonData)
                map_size.append((map['length-x'], map['length-y']))
                listObject = map['object']
                for objects in listObject:
                    for object in listObject[objects]:
                        dic[object] = listObject[objects][object]
        return dic, map_size  # dic{"name_tiles" : [position in map]}

    def loadMaps(self):
        print(tiles)
        print(self.map)
        load_images = {}
        # img = pygame.image.load("./img/Tileset.png")
        for i in self.map:
            img = pygame.image.load(tiles[i][0])
            img = img.subsurface(tiles[i][1], tiles[i][2], tiles[i][3][0], tiles[i][3][1])
            load_images[i] = pygame.transform.scale(img, (tiles[i][3][0]*scale, tiles[i][3][1]*scale))
        return load_images  # dictionary{"name_tiles" : img}

    def update(self, screen, player):
        x_camera = player.x - (window_size[0] - tile_size*scale) / 2
        if x_camera < 0:
            x_camera = 0
        if x_camera + window_size[0] >= self.map_size[self.index][0] * scale:
            x_camera = self.map_size[self.index][0]*scale - window_size[0]
        self.x = -x_camera
        for tiles_name in self.map:
            for i in self.map[tiles_name]:
                screen.blit(self.images[tiles_name], (i[0]*scale + self.x, i[1]*scale + self.y))
    # def update(self, screen):
