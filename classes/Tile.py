import pygame, json


class Tile:
    def __init__(self):
        self.tiles = self.loadTiles(
            [
                "./sprites/tiled.json"
            ]
        )

    def loadTiles(self, urlListTile):
        dic = {}
        for url in urlListTile:
            with open(url) as url:
                data = json.load(url)
                img = data['ImageURL']
                sprites = data['sprites']
                for sprite in sprites:
                    dic[sprite['name']] = [img, sprite['x'], sprite['y'], sprite['size']]
        return dic
