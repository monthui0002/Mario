import pygame, json
from classes.Sprites import Sprites
# from classes.Animation import Animation
from classes.Input import Input

spriteCollection = Sprites().spriteCollection
# smallAnimation = Animation()

class Mario:
    def __init__(self, x, y, sound, screen, level=1):
        self.x = x
        self.y = y
        self.input = Input(self)
        self.level = level
        self.sound = sound # sound chưa có
        self.screen = screen

    def updateImage(self,name, screen,flip = False):
        # self.input.checkInput()
        sprite = spriteCollection[name]
        # if up:
        #     sprite = spriteCollection['mario_small_jump'] if level == 1 else spriteCollection['mario_big_jump']
        # elif down and self.x:
        #     sprite = spriteCollection['mario_small_stand'] if level == 1 else spriteCollection['mario_big_sit']
        # elif right:
        #     sprite = spriteCollection['mario_small_run1'] if level == 1 else spriteCollection['mario_big_run1']
        # elif left:
        #     sprite = spriteCollection['mario_small_run1'] if level == 1 else spriteCollection['mario_big_run1']
        # else:
        #     sprite = spriteCollection['mario_small_stand'] if level == 1 else spriteCollection['mario_big_stand']
        img = pygame.image.load(sprite[0])
        img = img.subsurface(sprite[1])  # vì con to chỉ x2 chiều cao
        img = pygame.transform.scale(img, (sprite[2]))
        img = pygame.transform.flip(img, True, False)
        screen.blit(img, (int(self.x), int(self.y)))
    def update(self, screen):
        eventt = self.input.checkInput()  # [boolean[KD_RIGHT, KD_LEFT, KD_UP, KD_DOWN], [boolean[KU_RIGHT, KU_LEFT, KU_UP, KU_DOWN]]
        if self.level == 1:
            if eventt[0][1]:
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
            if eventt[0][1]:
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


        # if inputt[0]:
        #     self.x += 5
        # elif inputt[1]:
        #     self.x -= 5
        # elif inputt[2]:
        #     self.y -= 5
        # elif inputt[3]:
        #     self.y += 5
