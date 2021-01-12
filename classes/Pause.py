import pygame

from classes.Input import get


class Pause:

    def __init__(self, screen, entity, dashboard):
        self.screen = screen
        self.entity = entity
        self.dashboard = dashboard
        self.key_input = {"Enter": False}

    def update(self):
        self.draw_pause()
        pygame.display.update()
        self.checkInput()

    def get_input(self):
        self.key_input = get({"Enter": False})

    def draw_pause(self):
        self.dashboard.drawText("PAUSE", 140, 160, 70)
        self.dashboard.drawText("press enter to continue", 140, 230, 20)

    def checkInput(self):
        self.get_input()
        if self.key_input["Enter"]:
            self.entity.pause = False
