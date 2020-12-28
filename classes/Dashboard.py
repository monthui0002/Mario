import pygame

class Dashboard():
    coin = pygame.image.load('./img/items.png')
    coin = coin.subsurface(144,160,6,8)
    coin = pygame.transform.scale(coin,(12,16))
    def __init__(self, screen):
        self.state = "menu"
        self.screen = screen
        self.levelName = "1 - 1"
        self.points = 0
        self.coins = 0
        self.ticks = 0
        self.time = 0

    # myfont = pygame.font.Font('freesansbold.ttf', 32)
    def update(self):
        self.drawText("MARIO", 50, 20, 15)
        self.drawText(self.pointString(), 50, 37, 15)
        self.screen.blit(Dashboard.coin,(235,37))
        self.drawText("x {}".format(self.coinString()), 250, 37, 16)

        self.drawText("WORLD", 450, 20, 15)
        self.drawText(str(self.levelName), 465, 37, 15)

        self.drawText("TIME", 670, 20, 15)
        # if self.state != "menu":
        self.drawText(self.timeString(), 660, 37, 15)

        # update Time
        self.ticks += 1
        if self.ticks == 60:
            self.ticks = 0
            self.time += 1

    def drawText(self, text, x, y, size):
        myfont = pygame.font.Font('freesansbold.ttf', size)
        textsurface = myfont.render(text, False, (255, 255, 255))
        self.screen.blit(textsurface, (x, y))

    def coinString(self):
        return "{:02d}".format(self.coins)

    def pointString(self):
        return "{:06d}".format(self.points)

    def timeString(self):
        return "{:02d}:{:02d}:{:02d}".format(self.time//3600,(self.time%3600)//60,(self.time%3600)%60)
