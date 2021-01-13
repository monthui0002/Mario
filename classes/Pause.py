import pygame

from classes.Input import get


class Pause:

    def __init__(self, screen, character, dashboard):
        self.screen = screen
        self.character = character
        self.dashboard = dashboard
        self.key_input = {"Enter": False}

    def update(self):
        self.draw_pause()
        pygame.display.update()
        self.checkInput()

    def get_input(self):
        self.key_input = get({"Enter": False})

    def draw_pause(self):
        if self.character.state == 9:
            self.dashboard.draw_text("Game Over!", 90, 160, 70, True)
            self.dashboard.draw_text("Press [Enter] to continue", 140, 230, 20, True)
        elif self.character.state == 10:
            self.dashboard.draw_text("Victory!", 90, 160, 70, True)
            self.dashboard.draw_text("Press [Enter] to back to menu", 140, 230, 20, True)
        else:
            self.dashboard.draw_text("Paused", 140, 160, 70, True)
            self.dashboard.draw_text("Press [Enter] to continue...", 140, 230, 20, True)

    def checkInput(self):
        self.get_input()
        if self.key_input["Enter"]:
            self.character.pause = False
            if self.character.state == self.character.DEAD:
                if self.dashboard.turn_avail > 0:
                    self.dashboard.turn_avail -= 1
                    self.character.x = 0
                    self.character.y = 0
                    self.character.level = 0
                    self.character.grow_lvl = 0
                    self.character.cur_frame = 0
                    self.character.cur_img = self.character.small_img
                    self.character.state = self.character.IN_AIR
                    self.character.cur_fall_speed = self.character.FALL_SPEED
                    self.character.key_input = {"KP_Enter": False, "Up": False, "Right": False, "Down": False,
                                                "Left": False, "Escape": False,
                                                "Enter": False}
                else:
                    self.character.restart = True
                if self.character.sound_player.allow_sound:
                    self.character.sound_player.bg_sound.play_sound()
            elif self.character.state == self.character.WIN:
                self.character.restart = True
            else:
                if self.character.sound_player.allow_sound:
                    self.character.sound_player.bg_sound.unpause_sound()
