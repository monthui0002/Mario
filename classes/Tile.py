import pygame, json


class Tile:
    def __init__(self):
        self.tiles = self.loadTiles(
            [
                "./sprites/tiled.json",
                "./sprites/Animation.json",
                "./sprites/items.json",
            ]
        )

    def loadTiles(self, urlListTile):
        res = {}
        for url in urlListTile:
            dic = {}
            with open(url) as url:
                data = json.load(url)
                if data["type"] == "wall":
                    img = data["image_url"]
                    sprites = data["sprites"]
                    for sprite in sprites:
                        dic[sprite["name"]] = [img, sprite['x'], sprite['y'], sprite['size']]
                elif data["type"] == "animation" or data["type"] == "items":
                    img = data["image_url"]
                    sprites = data["sprites"]
                    size = data["size"]
                    for sprite in sprites:
                        dic[sprite["name"]] = [img, size,sprite["images"]]
            res.update(dic)
        return res
