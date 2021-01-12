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
            self.dashboard.draw_text("YOU LOSE!", 90, 160, 70)
            self.dashboard.draw_text("Press [Enter] to back to menu", 140, 230, 20)
        elif self.character.state == 10:
            self.dashboard.draw_text("YOU WIN!", 90, 160, 70)
            self.dashboard.draw_text("Press [Enter] to back to menu", 140, 230, 20)
        else:
            self.dashboard.draw_text("PAUSED", 140, 160, 70)
            self.dashboard.draw_text("Press [Enter] to continue...", 140, 230, 20)

    def checkInput(self):
        self.get_input()
        if self.key_input["Enter"]:
            self.character.pause = False
            if self.character.state == 9 or self.character.state == 10:
                self.character.restart = True
