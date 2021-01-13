import pygame

from classes.Background import Background
from classes.Constants import *
from classes.Level import Level
from classes.Menu import Menu
from classes.SoundPlayer import SoundPlayer
from entities.Mario import Mario

fps_clock = pygame.time.Clock()
pygame.init()
window_size = (16 * tile_size * scale, 14 * tile_size * scale)  # 25*14
pygame.display.set_caption('MARIO')
screen = pygame.display.set_mode(window_size)
bg = pygame.transform.scale(screen, (w, h))
sound_player = SoundPlayer()

while True:
    menu = Menu(screen, sound_player)
    while not menu.pause:
        menu.update()
        pygame.display.update()
        fps_clock.tick(FPS / 6)
        if sound_player.allow_sound:
            if not sound_player.bg_sound.is_playing():
                sound_player.bg_sound.play_sound(True)
        else:
            sound_player.bg_sound.stop_sound()

    level = Level("levels/" + menu.level_name, screen)
    background = Background(0, 0, screen, level)
    mario = Mario(0, 0, Mario.DIRECTION_RIGHT, 0, Mario.IN_AIR, screen, background, level, sound_player)
    background.set_character(mario)

    while not mario.restart:
        if mario.pause:
            mario.pause_obj.update()
        else:
            background.update()
            mario.update()
        pygame.display.update()
        fps_clock.tick(FPS)
