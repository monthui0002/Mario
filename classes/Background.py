import pygame, json

from classes.Tile import Tile

window_size = (400, 224)

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
            load_images[i] = pygame.transform.scale(img, (tiles[i][3][0], tiles[i][3][1]))
        return load_images  # dictionary{"name_tiles" : img}

    def update(self, screen, player):
        x_camera = player.x - (window_size[0] - 16) / 2
        if x_camera < 0:
            x_camera = 0
        if x_camera + window_size[0] > self.map_size[self.index][0]:
            x_camera = player.x
            player.x = (window_size[0] - 16) / 2
        self.x = -x_camera
        print("player:", player.x, "x_camera:", x_camera)
        for tiles_name in self.map:
            for i in self.map[tiles_name]:
                screen.blit(self.images[tiles_name], (i[0] + self.x, i[1] + self.y))
    # def update(self, screen):
