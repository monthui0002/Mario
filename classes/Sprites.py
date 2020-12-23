import pygame, json

from classes.Animation import Animation

# from classes.Sprite import Sprite
# from classes.Spritesheet import Spritesheet

WIDTH = 16
HEIGHT = 16


class Sprites:
    def __init__(self):
        self.spriteCollection = self.loadSprites(
            [
                "./sprites/Mario.json",
            ]
        )

    def loadSprites(self, urlList):
        resDict = {}
        for url in urlList:
            with open(url) as jsonData:
                jsonData = json.load(jsonData)
                imgURL = jsonData['url']
                for data in jsonData['sprites']:
                    # img = pygame.image.load(url)
                    dic = {}  # img và name của ảnh
                    size = jsonData['size']
                    sprites = jsonData['sprites']
                    for sprite in sprites:
                        # image = img.subsurface(sprites['x'],sprites['y'],size[0],size[1]*sprites['scale']) #vì con to chỉ x2 chiều cao
                        subSurface = (sprite['x'], sprite['y'], size[0], size[1] * sprite['scale'])
                        scale = (WIDTH, HEIGHT * sprite['scale'])
                        # image = pygame.transform.scale(image, (WIDTH, HEIGHT*sprites['scale']))
                        dic[sprite['name']] = [imgURL, subSurface, scale]
                    resDict.update(dic)

        return resDict
