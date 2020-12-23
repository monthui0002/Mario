import pygame, json

from classes.Tile import Tile

url_list_map = [
    "./levels/map1.json",
]

windowSize = (640, 480)

tiles = Tile().tiles

def loadMaps(urlListMap):
    dic = {}
    map_size = [(0, 0)]  # map 0
    for url in urlListMap:
        with open(url) as jsonData:
            map = json.load(jsonData)
            map_size.append((map['length-x'], map['length-y']))
            listObject = map['object']
            for objects in listObject:
                for object in listObject[objects]:
                    dic[object] = listObject[objects][object]
    return dic, map_size

map,map_size = loadMaps(url_list_map)

class Background:
    def __init__(self):
        self.map = map
        self.map_size = map_size
        self.index = 1

    def draw(self):
        bg = pygame.display.set_mode(windowSize)
        bg = pygame.transform.scale(bg, self.map_size[self.index])  # map ban đầu
        pygame.display.set_caption('MARIO')
        pygame.display.update()
        for name_tile in self.map:
            for tile in self.map[name_tile]:
                img = pygame.image.load(tiles[name_tile][0])
                img = img.subsurface(tiles[name_tile][1],tiles[name_tile][2],tiles[name_tile][3][0],tiles[name_tile][3][1])
                img = pygame.transform.scale(img,tiles[name_tile][3])
                bg.blit(img, tile)
