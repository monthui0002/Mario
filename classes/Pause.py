import pygame

from classes.Input import get

class Pause:
    image = pygame.image.load('./img/items.png')
    image1 = image.subsurface(311, 160, 9, 8)
    image2 = image.subsurface(23, 160, 9, 8)
    img = [pygame.transform.scale(image1, (18, 16)),pygame.transform.scale(image2, (18, 16))]

    def __init__(self, screen, entity, dashboard):
        self.screen = screen
        self.entity = entity
        self.dashboard = dashboard
        self.input = {"Enter": False, "Up": False, "Right": False}
        self.state = True # continue: True, back to menu : False

    def update(self):
        # self.screen.blit(self.pause_srfc, (0, 0))
        self.draw_pause()
        pygame.display.update()
        self.checkInput()

    def get_input(self):
        self.key_input = get({"Enter": False, "Up": False, "Down": False})

    def draw_pause(self):
        self.dashboard.drawText("PAUSED", 120, 160, 68)
        self.screen.blit(self.img[0], (130, 285))
        self.dashboard.drawText("CONTINUE", 150, 280, 32)
        self.screen.blit(self.img[0], (130, 325))
        self.dashboard.drawText("BACK TO MENU", 150, 320, 32)
        self.screen.blit(self.img[1],(130, 285 if self.state else 325))

    def checkInput(self):
        self.get_input()
        if self.key_input["Up"] or self.key_input["Down"]:
            self.state = not self.state
        if self.key_input["Enter"]:
            if self.state:
                self.entity.pause = False
            else:
                self.entity.restart = True
    # def createBackgroundBlur(self):
    #     self.pause_srfc = GaussianBlur().filter(self.screen, 0, 0, 640, 480)
