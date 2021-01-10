import pygame
import json
from classes.Dashboard import Dashboard
from classes.Tile import Tile
from classes.Input import get
from classes.Constants import *

tiles = Tile().tiles

def load_json():
    with open('./levels/menu.json') as jsonData:
        map_data = json.load(jsonData)
        bg_colors = map_data['color']
        ground = map_data['object']["ground"]
        background = map_data['object']["background"]
        return background,ground,bg_colors

class Menu:
    image = pygame.image.load('./img/items.png')
    image1 = image.subsurface(311, 160, 9, 8)
    image2 = image.subsurface(23, 160, 9, 8)
    img = [pygame.transform.scale(image1, (18, 16)),pygame.transform.scale(image2, (18, 16))]
    def __init__(self, screen):
        self.screen = screen
        self.dashboard = Dashboard(screen)
        self.dashboard.state = "menu"
        self.dashboard.levelName = ""
        self.key_input = self.key_input = {"Enter": False, "Up": False, "Right": False, "Down": False, "Left": False, "Escape": False}
        self.pause = False
        self.cur_img = 1

    def update(self):
        self.load_background()
        self.dashboard.update()
        self.draw_setting()
        self.update_setting()
        self.get_input()
    def load_background(self):
        background, ground, bg_colors = load_json()

        # load background menu
        self.screen.fill(bg_colors)
        ground_tile = tiles['1-1']
        img = pygame.image.load(ground_tile[0])
        img = img.subsurface(0,0,16,16)
        img = pygame.transform.scale(img,(tile_size*scale,tile_size*scale))
        for y in range(ground[1], ground[1] + ground[3]):
            for x in range(ground[0], ground[0] + ground[2]):
                self.screen.blit(img,(x * tile_size * scale, y * tile_size * scale))
        for background_type in background:
            img = pygame.image.load(tiles[background_type][0])
            img = img.subsurface(tiles[background_type][1], tiles[background_type][2],
                                 tiles[background_type][3][0], tiles[background_type][3][1])
            img = pygame.transform.scale(img, (tiles[background_type][3][0] * scale, tiles[background_type][3][1] * scale))
            for i in background[background_type]:
                self.screen.blit(img,(i[0]*scale*tile_size,i[1]*scale*tile_size))

        # load bảng tên
        image = pygame.image.load('./img/title_screen.png')
        image = image.subsurface(1,60,175,87)
        image = pygame.transform.scale(image,(262,130))
        self.screen.blit(image,((w - 262)/2,100))

        # load ảnh nhân vật
        mario = pygame.image.load('./img/mario.png')
        mario = mario.subsurface(80, 34, 16, 16)
        mario = pygame.transform.scale(mario, (16*scale, 16*scale))
        self.screen.blit(mario,(2.5*scale*tile_size,11*scale*tile_size))

    def get_input(self):
        self.key_input = get(self.key_input)
    def drawText(self, text, x, y, size):
        myfont = pygame.font.Font('freesansbold.ttf', size)
        textsurface = myfont.render(text, False, (255, 255, 255))
        self.screen.blit(textsurface, (x, y))

    def draw_setting(self):
        self.screen.blit(self.img[0],((w - 262)/2,240))
        self.screen.blit(self.img[0],((w - 262)/2,270))
        self.screen.blit(self.img[0],((w - 262)/2,300))
        self.drawText("CHOOSE LEVEL", (w - 262)/2 + 24, 240, 25)
        self.drawText("SETTINGS", (w - 262)/2 + 24, 270, 25)
        self.drawText("EXIT", (w - 262)/2 + 24, 300, 25)
        self.screen.blit(self.img[1],((w - 262)/2,240 if self.cur_img == 1 else 270 if self.cur_img == 2 else 300))

    def update_setting(self):
        if self.key_input["Up"]:
            self.cur_img = self.cur_img - 1 if self.cur_img > 1 else 3
        if self.key_input["Down"]:
            self.cur_img = self.cur_img + 1 if self.cur_img < 3 else 1
        if self.key_input["Enter"]:
            if self.cur_img == 1:
                print("choose level")
            elif self.cur_img == 2:
                print("setting")
            else:
                pygame.quit()