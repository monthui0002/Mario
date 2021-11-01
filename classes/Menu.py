import json

import pygame

from classes.Constants import *
from classes.Dashboard import Dashboard
from classes.Input import get
from classes.Tile import Tile

tiles = Tile().tiles


def load_json():
    with open('./settings/menu.json') as jsonData:
        map_data = json.load(jsonData)
        bg_colors = map_data['color']
        ground = map_data['object']["ground"]
        background = map_data['object']["background"]
        return background, ground, bg_colors


def load_setting():
    with open('./settings/setting.json') as jsonData:
        data = json.load(jsonData)
        music = data['music']
        return music


def load_level_name():
    files = []
    for file in os.listdir("./levels"):
        files.append(file.split(".")[0])
    return files


levels = load_level_name()


class Menu:
    image = pygame.image.load('./img/items.png')
    image1 = image.subsurface(311, 160, 9, 8)
    image2 = image.subsurface(23, 160, 9, 8)
    img = [pygame.transform.scale(image1, (18, 16)), pygame.transform.scale(image2, (18, 16))]

    MENU = 0
    IN_CHOOSING_LEVEL = 1
    INSETTING = 2
    EXIT = 3

    def __init__(self, screen, sound_player):
        self.screen = screen
        self.sound_player = sound_player
        self.dashboard = Dashboard(screen)
        self.dashboard.state = "menu"
        self.key_input = {"Enter": False, "Up": False, "Right": False, "Down": False, "Left": False, "Escape": False}
        self.pause = False
        self.cur_img = 1
        self.state = self.MENU
        self.music = load_setting()
        self.sound_player.allow_sound = self.music
        self.level = 1
        self.level_name = ""

    def update(self):
        self.dashboard.update()
        self.update_menu()
        self.update_setting()

    def get_input(self):
        self.key_input = get(
            {"Enter": False, "Up": False, "Right": False, "Down": False, "Left": False, "Escape": False})

    def draw_background(self):
        background, ground, bg_colors = load_json()

        # load background menu
        self.screen.fill(bg_colors)
        ground_tile = tiles['1-1']
        img = pygame.image.load(ground_tile[0])
        img = img.subsurface(0, 0, 16, 16)
        img = pygame.transform.scale(img, (tile_size * scale, tile_size * scale))
        for y in range(ground[1], ground[1] + ground[3]):
            for x in range(ground[0], ground[0] + ground[2]):
                self.screen.blit(img, (x * tile_size * scale, y * tile_size * scale))
        for background_type in background:
            img = pygame.image.load(tiles[background_type][0])
            img = img.subsurface(tiles[background_type][1], tiles[background_type][2],
                                 tiles[background_type][3][0], tiles[background_type][3][1])
            img = pygame.transform.scale(img,
                                         (tiles[background_type][3][0] * scale, tiles[background_type][3][1] * scale))
            for i in background[background_type]:
                self.screen.blit(img, (i[0] * scale * tile_size, i[1] * scale * tile_size))

        # load character images
        mario = pygame.image.load('./img/mario.png')
        mario = mario.subsurface(80, 34, 16, 16)
        mario = pygame.transform.scale(mario, (16 * scale, 16 * scale))
        self.screen.blit(mario, (2.5 * scale * tile_size, 11 * scale * tile_size))

    def draw_menu_background(self):
        image = pygame.image.load('./img/title_screen.png')
        image = image.subsurface(1, 60, 175, 87)
        image = pygame.transform.scale(image, (262, 130))
        self.screen.blit(image, ((w - 262) / 2, 100))

    def update_menu(self):
        self.draw_background()
        if self.state != self.IN_CHOOSING_LEVEL:
            self.draw_menu_background()
            self.dashboard.update()

        if self.state == self.MENU:
            self.draw_menu()
        elif self.state == self.IN_CHOOSING_LEVEL:
            self.draw_choose_level()
        elif self.state == self.INSETTING:
            self.draw_setting()
        else:
            exit(0)

    def update_setting(self):
        self.get_input()
        if self.key_input["Up"]:
            self.cur_img = self.cur_img - 1 if self.cur_img > 1 else 3
        if self.key_input["Down"]:
            self.cur_img = self.cur_img + 1 if self.cur_img < 3 else 1
        if self.state == self.IN_CHOOSING_LEVEL:
            if self.key_input["Right"]:
                self.level = self.level + 1 if self.level < len(levels) else 1
            elif self.key_input["Left"]:
                self.level = self.level - 1 if self.level > 1 else len(levels)
        if self.key_input["Enter"]:
            if self.state == self.MENU:
                if self.cur_img == 1:
                    self.state = self.IN_CHOOSING_LEVEL
                elif self.cur_img == 2:
                    self.state = self.INSETTING
                else:
                    self.state = self.EXIT
            elif self.state == self.INSETTING:
                if self.cur_img == 1:
                    self.music = not self.music
                    self.sound_player.allow_sound = self.music
                else:
                    self.state = self.MENU
                    self.save_setting()
            elif self.state == self.IN_CHOOSING_LEVEL:
                self.level_name = list_map[self.level - 1]
                self.pause = True

    def drawText(self, text, x, y, size):
        my_font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = my_font.render(text, False, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def draw_menu(self):
        self.screen.blit(self.img[0], ((w - 262) / 2, 240))
        self.screen.blit(self.img[0], ((w - 262) / 2, 270))
        self.screen.blit(self.img[0], ((w - 262) / 2, 300))
        self.drawText("CHOOSE LEVEL", (w - 262) / 2 + 24, 240, 25)
        self.drawText("SETTINGS", (w - 262) / 2 + 24, 270, 25)
        self.drawText("EXIT", (w - 262) / 2 + 24, 300, 25)
        self.screen.blit(self.img[1], ((w - 262) / 2, 240 if self.cur_img == 1 else 270 if self.cur_img == 2 else 300))

    def draw_setting(self):
        self.screen.blit(self.img[0], ((w - 262) / 2, 240))
        self.screen.blit(self.img[0], ((w - 262) / 2, 270))
        self.drawText("MUSIC", (w - 262) / 2 + 24, 240, 25)
        self.drawText("ON" if self.music else "OFF", (w - 262) / 2 + 150, 240, 25)
        self.drawText("BACK", (w - 262) / 2 + 24, 270, 25)
        self.screen.blit(self.img[1], ((w - 262) / 2, 240 if self.cur_img == 1 else 270))

    def draw_choose_level(self):
        x = 30
        y = 30
        width = 120
        for i in range(0, len(levels)):
            if i + 1 != self.level:
                pygame.draw.rect(self.screen, [150, 150, 150], pygame.Rect(x + width * i, y, 100, 100), 2)
            else:
                pygame.draw.rect(self.screen, [255, 255, 255], pygame.Rect(x + width * i, y, 100, 100), 2)
            self.drawText(levels[i], 60 + width * i, 60, 30)

    def save_setting(self):
        data = {"music": self.music}
        with open('./settings/setting.json', "w") as outfile:
            json.dump(data, outfile)
