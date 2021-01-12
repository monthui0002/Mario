import pygame

from classes.Input import get
from classes.Constants import *


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
            self.dashboard.draw_text("YOU WIN!", 90, 160, 70, True)
            self.dashboard.draw_text("Press [Enter] to back to menu", 140, 230, 20, True)
        else:
            self.dashboard.draw_text("PAUSED", 140, 160, 70, True)
            self.dashboard.draw_text("Press [Enter] to continue...", 140, 230, 20, True)

    def checkInput(self):
        self.get_input()
        if self.key_input["Enter"]:
            self.character.pause = False
            if self.character.state == 9:
                if self.dashboard.turn_avail > 0:
                    self.dashboard.turn_avail -= 1
                    self.character.x = 0
                    self.character.y = 0
                    self.character.state = 4
                else:
                    self.character.restart = True
            elif self.character.state == 10:
                self.character.restart = True
