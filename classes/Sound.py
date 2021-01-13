import pygame
from pygame import mixer

pygame.mixer.init(44100, -16, 2, 2048)


class Sound:
    sounds = [mixer.Sound("./sounds/bg.ogg"), mixer.Sound("./sounds/coin.ogg"), mixer.Sound("./sounds/jump.ogg"),
              mixer.Sound("./sounds/death.wav"), mixer.Sound("./sounds/grow-up.ogg"),
              mixer.Sound("./sounds/shrink-down.ogg"), mixer.Sound("./sounds/mine.ogg")]

    def __init__(self, channel):
        self.channel = channel
        self.sound = mixer.Channel(channel)
        self.sound.set_volume(0.2)

    def play_sound(self, loop=False):
        if loop:
            self.sound.play(Sound.sounds[self.channel], -1)
        else:
            self.sound.play(Sound.sounds[self.channel])

    def is_playing(self):
        return self.sound.get_busy()

    def stop_sound(self):
        self.sound.stop()

    def pause_sound(self):
        self.sound.pause()

    def unpause_sound(self):
        self.sound.unpause()
