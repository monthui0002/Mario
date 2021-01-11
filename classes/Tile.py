import json


def load(list_url):
    res = {}
    for url in list_url:
        dic = {}
        with open(url) as loaded_data:
            data = json.load(loaded_data)
            if data["type"] == "tile":
                img = data["image_url"]
                sprites = data["sprites"]
                for sprite_type in sprites:
                    for data in sprites[sprite_type]:
                        dic[data["name"]] = [img, data["x"], data["y"], data["size"]]
            elif data["type"] == "animation" or data["type"] == "items":
                img = data["image_url"]
                sprites = data["sprites"]
                size = data["size"]
                for sprite in sprites:
                    dic[sprite["name"]] = [img, size, sprite["images"]]
            elif data["type"] == "static_items":
                img = data["image_url"]
                sprites = data["sprites"]
                for sprite in sprites:
                    dic[sprite["name"]] = [img, sprite["x"], sprite["y"], sprite["size"]]
                print(dic)
        res.update(dic)
    return res


class Tile:
    def __init__(self):
        self.tiles = load(
            [
                "./sprites/tiled.json",
                "./sprites/animation.json",
                "./sprites/items.json",
                "./sprites/static_items.json",
            ]
        )
