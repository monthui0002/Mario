import json

import pygame

from boxes.Box import Box
from boxes.HiddenBox import HiddenBox
from boxes.RandomBox import RandomBox
from classes.Constants import *
from classes.Tile import Tile
from entities.Mario import Mario

tiles = Tile().tiles


def load_map_data(url):
    with open(url) as jsonData:
        map_data = json.load(jsonData)
        map_size = (map_data['length-x'] * tile_size * scale, map_data['length-y'] * tile_size * scale)
        bg_color = map_data['color']
        map_data_list = map_data['object']
        return map_data_list, map_size, bg_color


class Level:
    def __init__(self, path, screen):
        self.map, self.map_size, self.color = load_map_data(path)
        self.ground = self.load_ground()
        self.background_and_stones = self.load_background_and_stones()
        self.reactables = self.load_reactables()
        self.screen = screen
        self.name = path[path.rfind("/") + 1:path.rfind(".json")]

    def load_reactables(self):
        reactables = []
        if "reactable" in self.map:
            for reactable_type in self.map["reactable"]:
                images = []
                img = pygame.image.load(tiles[reactable_type][0])
                if reactable_type == "hidden-box":
                    img1 = img.subsurface(tiles[reactable_type][1], tiles[reactable_type][2],
                                          tiles[reactable_type][3][0], tiles[reactable_type][3][1])
                    images.append(pygame.transform.scale(img1, (
                        tiles[reactable_type][3][0] * scale, tiles[reactable_type][3][1] * scale)))
                elif reactable_type == "random-box":
                    for i in range(0, 3):
                        name = reactable_type + ("" if i == 0 else str(i))
                        img1 = img.subsurface(tiles[name][1], tiles[name][2],
                                              tiles[name][3][0], tiles[name][3][1])
                        images.append(pygame.transform.scale(img1, (
                            tiles[name][3][0] * scale, tiles[name][3][1] * scale)))
                img1 = img.subsurface(tiles["opened-box"][1], tiles["opened-box"][2], tiles["opened-box"][3][0],
                                      tiles["opened-box"][3][1])
                images.append(pygame.transform.scale(img1, (
                    tiles["opened-box"][3][0] * scale, tiles["opened-box"][3][1] * scale)))
                for obj in self.map["reactable"][reactable_type]:
                    if reactable_type == "hidden-box":
                        reactables.append(
                            HiddenBox(images, obj[0] * tile_size * scale, obj[1] * tile_size * scale, tiles))
                    elif reactable_type == "random-box":
                        reactables.append(
                            RandomBox(images, obj[0] * tile_size * scale, obj[1] * tile_size * scale, tiles))
        return reactables  # dictionary{"name_tiles" : img}

    def load_ground(self):
        load_ground = {}
        if "ground" in self.map:
            for ground_type in self.map["ground"]:
                img = pygame.image.load(tiles[ground_type][0])
                img = img.subsurface(tiles[ground_type][1], tiles[ground_type][2], tiles[ground_type][3][0],
                                     tiles[ground_type][3][1])
                load_ground[ground_type] = pygame.transform.scale(img, (
                    tiles[ground_type][3][0] * scale, tiles[ground_type][3][1] * scale))
        return load_ground  # dictionary{"name_tiles" : img}

    def load_background_and_stones(self):
        load_background_and_stone = {}
        if "background" in self.map:
            for background_type in self.map["background"]:
                img = pygame.image.load(tiles[background_type][0])
                img = img.subsurface(tiles[background_type][1], tiles[background_type][2],
                                     tiles[background_type][3][0], tiles[background_type][3][1])
                load_background_and_stone[background_type] = pygame.transform.scale(img, (
                    tiles[background_type][3][0] * scale, tiles[background_type][3][1] * scale))
        if "stone" in self.map:
            for stone_type in self.map["stone"]:
                img = pygame.image.load(tiles[stone_type][0])
                img = img.subsurface(tiles[stone_type][1], tiles[stone_type][2], tiles[stone_type][3][0],
                                     tiles[stone_type][3][1])
                load_background_and_stone[stone_type] = pygame.transform.scale(img, (
                    tiles[stone_type][3][0] * scale, tiles[stone_type][3][1] * scale))
        return load_background_and_stone  # dictionary{"name_tiles" : img}

    def update(self, bg_x, bg_y):
        self.screen.fill(self.color)
        self.update_background_and_stones(bg_x, bg_y)
        self.update_ground(bg_x, bg_y)
        self.update_reactables(bg_x, bg_y)

    def update_reactables(self, bg_x, bg_y):
        for item in self.reactables:
            if type(item).__name__ == "RandomBox":
                if item.cur_frame != len(item.img) - 1:
                    item.cur_frame += 5 / FPS
                    if int(item.cur_frame) > len(item.img) - 2:
                        item.cur_frame = 0
            elif type(item).__name__ == "HiddenBox":
                pass
            self.screen.blit(item.img[int(item.cur_frame)],
                             (item.x + bg_x, item.y + bg_y))
            if item.triggered:
                self.screen.blit(item.item_img[int(item.item_img_idx)], (item.x + bg_x,
                                                                         item.y + bg_y - tile_size * scale))
                item.item_img_idx += 10 / FPS
                if int(item.item_img_idx) > len(item.item_img) - 1:
                    item.item_img_idx = 0
                    item.triggered = False
                    item.has_item = False

    def update_ground(self, bg_x, bg_y):
        if "ground" in self.map:
            for tiles_name in self.map["ground"]:
                for i in self.map["ground"][tiles_name]:
                    for y in range(i[1], i[1] + i[3]):
                        for x in range(i[0], i[0] + i[2]):
                            self.screen.blit(self.ground[tiles_name],
                                             (x * tile_size * scale + bg_x, y * tile_size * scale + bg_y))

    def update_background_and_stones(self, bg_x, bg_y):
        if "background" in self.map:
            for tiles_name in self.map["background"]:
                for i in self.map["background"][tiles_name]:
                    self.screen.blit(self.background_and_stones[tiles_name],
                                     (i[0] * tile_size * scale + bg_x, i[1] * tile_size * scale + bg_y))
        if "stone" in self.map:
            for tiles_name in self.map["stone"]:
                for i in self.map["stone"][tiles_name]:
                    self.screen.blit(self.background_and_stones[tiles_name],
                                     (i[0] * tile_size * scale + bg_x, i[1] * tile_size * scale + bg_y))

    def check_collision(self, character):
        for collided_obj in self.map:
            if collided_obj == "background":
                continue
            for ground_name in self.map[collided_obj]:
                for obj_item in self.map[collided_obj][ground_name]:
                    if len(obj_item) != 4:
                        obj_item += [1, 1]
                    on_ground = (character.y + tile_size * scale * (character.level + 1) >= obj_item[
                        1] * tile_size * scale and character.y + tile_size * scale * (
                                         character.level + 1) <= (
                                         obj_item[1] + obj_item[3]) * tile_size * scale and
                                 (obj_item[0] * tile_size * scale <= character.x <= (
                                         obj_item[0] + obj_item[2]) * tile_size * scale - delta or obj_item[
                                      0] * tile_size * scale + delta <= character.x + tile_size * scale <= (
                                          obj_item[0] + obj_item[2]) * tile_size * scale))
                    if on_ground:
                        return on_ground, obj_item
        return False, None

    def check_collision_bottom(self, character):
        on_ground, obj = self.check_collision(character)
        if on_ground:
            character.y = obj[1] * tile_size * scale - tile_size * scale * (
                    character.level + 1)
            if character.state == Mario.IN_AIR:
                character.cur_fall_speed = Mario.FALL_SPEED
                character.state = Mario.IDLE
        elif character.state != Mario.IN_AIR:
            character.state = Mario.IN_AIR

    def check_collision_top(self, character):
        for collided_obj in self.map:
            if collided_obj == "background":
                continue
            for ground_name in self.map[collided_obj]:
                for obj_item in self.map[collided_obj][ground_name]:
                    if ground_name == "hidden-box" or ground_name == "random-box":
                        continue
                    if len(obj_item) != 4:
                        obj_item += [1, 1]
                    touch_up = (obj_item[
                                    1] * tile_size * scale <= character.y <= (
                                        obj_item[1] + obj_item[3]) * tile_size * scale and
                                (obj_item[0] * tile_size * scale <= character.x <= (
                                        obj_item[0] + obj_item[2]) * tile_size * scale - delta or obj_item[
                                     0] * tile_size * scale + delta <= character.x + tile_size * scale <= (
                                         obj_item[0] + obj_item[2]) * tile_size * scale))
                    if touch_up:
                        character.y = (obj_item[1] + obj_item[3]) * tile_size * scale
                        character.cur_fall_speed *= -0.7
                        return
        for item in self.reactables:
            touch_up = (item.y <= character.y <=
                        item.y + item.h and (
                                item.x <= character.x <= item.x + item.w - delta or item.x + delta <= character.x + tile_size * scale <= item.x + item.w))
            if touch_up:
                character.y = item.y + item.h
                character.cur_fall_speed *= -0.7
                if item.state == Box.NOT_OPENED and item.has_item or type(item).__name__ == "RandomBox":
                    item.state = Box.OPENED
                    if item.has_item:
                        item.has_item = False
                        if item.item_type == Box.ITEM_COIN:
                            character.dashboard.coins += 1
                            if character.sound_player.allow_sound:
                                character.sound_player.coin_sound.play_sound()
                        elif item.item_type == Box.ITEM_MUSHROOM:
                            character.key_input["Up"] = False
                            if character.level < 1:
                                if character.sound_player.allow_sound:
                                    character.sound_player.grow_up_sound.play_sound()
                                character.state = Mario.GROW
                        elif item.item_type == Box.ITEM_MINE:
                            character.key_input["Up"] = False
                            if character.sound_player.allow_sound:
                                character.sound_player.mine_sound.play_sound()
                            character.state = Mario.SHRINK
                        item.triggered = True
                    item.cur_frame = len(item.img) - 1
                return

    def check_collision_right(self, character):
        for collided_obj in self.map:
            if collided_obj == "background":
                continue
            for ground_name in self.map[collided_obj]:
                for obj_item in self.map[collided_obj][ground_name]:
                    if len(obj_item) != 4:
                        obj_item += [1, 1]
                    coll = (obj_item[0] * tile_size * scale - delta <= character.x + tile_size * scale <= (
                            obj_item[0] + obj_item[2]) * tile_size * scale) and (
                                   character.y + tile_size * scale * (character.level + 1) - delta >= obj_item[
                               1] * tile_size * scale and character.y + tile_size * scale * (
                                           character.level + 1) <= (
                                           obj_item[1] + obj_item[3]) * tile_size * scale)
                    if coll:
                        character.x = (obj_item[0] - 1) * tile_size * scale - delta

    def check_collision_left(self, character):
        for collided_obj in self.map:
            if collided_obj == "background":
                continue
            for ground_name in self.map[collided_obj]:
                for obj_item in self.map[collided_obj][ground_name]:
                    if len(obj_item) != 4:
                        obj_item += [1, 1]
                    coll = (obj_item[0] * tile_size * scale + delta <= character.x <= (
                            obj_item[0] + obj_item[2]) * tile_size * scale) and (
                                   character.y + tile_size * scale * (character.level + 1) - delta >= obj_item[
                               1] * tile_size * scale and character.y + tile_size * scale * (
                                           character.level + 1) <= (
                                           obj_item[1] + obj_item[3]) * tile_size * scale)
                    if coll:
                        character.x = (obj_item[0] + obj_item[2]) * tile_size * scale + delta
