import pygame, json
from classes.Sprites import Sprites
from classes.Animation import Animation

spriteCollection = Sprites().spriteCollection
# smallAnimation = Animation()

class Mario:
    def __init__(self, x, y, sound, screen, level=1):
        self.x = x
        self.y = y
        self.level = level
        self.sound = sound
        self.screen = screen

    def updateImage(self, up, down, right, left, screen, level = 1):
        sprite = spriteCollection['mario_small_stand']
        if up:
            sprite = spriteCollection['mario_small_jump'] if level == 1 else spriteCollection['mario_big_jump']
        elif down and self.x:
            sprite = spriteCollection['mario_small_stand'] if level == 1 else spriteCollection['mario_big_sit']
        elif right:
            sprite = spriteCollection['mario_small_run1'] if level == 1 else spriteCollection['mario_big_run1']
        elif left:
            sprite = spriteCollection['mario_small_run1'] if level == 1 else spriteCollection['mario_big_run1']
        else:
            sprite = spriteCollection['mario_small_stand'] if level == 1 else spriteCollection['mario_big_stand']
        img = pygame.image.load(sprite[0])
        img = img.subsurface(sprite[1])  # vì con to chỉ x2 chiều cao
        img = pygame.transform.scale(img, (sprite[2]))
        img = pygame.transform.flip(img, True, False)
        screen.blit(img, (int(self.x), int(self.y)))
