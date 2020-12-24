import pygame, json
from classes.Sprites import Sprites
# from classes.Animation import Animation
from classes.Input import Input

spriteCollection = Sprites().spriteCollection
# smallAnimation = Animation()

class Mario:
    def __init__(self, x, y, sound, screen, level=1, width = 16): #16px
        self.x = x
        self.y = y
        self.width = width
        self.input = Input(self)
        self.level = level
        self.sound = sound # sound chưa có
        self.screen = screen

    def updateImage(self,name, screen,flip = False):
        sprite = spriteCollection[name]
        img = pygame.image.load(sprite[0])
        img = img.subsurface(sprite[1])  # vì con to chỉ x2 chiều cao
        img = pygame.transform.scale(img, (sprite[2]))
        if flip:
            img = pygame.transform.flip(img, True, False)
        screen.blit(img, (int(self.x), int(self.y)))
    def update(self, screen):
        eventt = self.input.checkInput()  # [boolean[KD_RIGHT, KD_LEFT, KD_UP, KD_DOWN], [boolean[KU_RIGHT, KU_LEFT, KU_UP, KU_DOWN]]
        if self.level == 1:
            if eventt[0][0]:
                self.updateImage('mario_small_run1',screen)
                self.x += 5
                return
            elif eventt[0][1]:
                self.updateImage('mario_small_run1',screen,True)
                self.x -= 5
                return
            elif eventt[0][2]:
                self.updateImage('mario_small_jump',screen)
                self.y -= 5
                return
            elif eventt[0][3]:
                self.updateImage('mario_small_stand',screen)
                self.y += 5
                return
            else:
                self.updateImage('mario_small_stand',screen)
        else:
            if eventt[0][0]:
                self.updateImage('mario_big_run1',screen)
                self.x += 5
                return
            elif eventt[0][1]:
                self.updateImage('mario_big_run1',screen,True)
                self.x -= 5
                return
            elif eventt[0][2]:
                self.updateImage('mario_big_jump',screen)
                self.y -= 5
                return
            elif eventt[0][3]:
                self.updateImage('mario_big_stand',screen)
                self.y += 5
                return
            else:
                self.updateImage('mario_big_stand',screen)