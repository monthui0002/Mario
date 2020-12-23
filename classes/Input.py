import pygame
import sys

class Input:
    def __init__(self, entities):
        self.entities = entities
    def checkInput(self):
        eventt = [[0,0,0,0],[0,0,0,0]] # [boolean[KD_RIGHT, KD_LEFT, KD_UP, KD_DOWN], [boolean[KU_RIGHT, KU_LEFT, KU_UP, KU_DOWN]]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    eventt[0][0] = True
                    print("right")
                if event.key == pygame.K_UP:
                    eventt[0][2] = True
                    eventt[0][3] = True
                if event.key == pygame.K_LEFT:
                    eventt[0][1] = True
                if event.key == pygame.K_DOWN:
                    eventt[0][3] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    eventt[1][0] = False
                if event.key == pygame.K_UP:
                    eventt[1][2] = False
                if event.key == pygame.K_LEFT:
                    eventt[1][1] = False
                if event.key == pygame.K_DOWN:
                    eventt[1][3] = False
        return eventt