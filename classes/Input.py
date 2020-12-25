import pygame
import sys


class Input:
    def check(self, res, name = "mario"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    res[1] = True
                elif event.key == pygame.K_RIGHT:
                    res[2] = True
                if event.key == pygame.K_UP:
                    res[3] = True
                elif event.key == pygame.K_DOWN:
                    res[4] = True
                if event.key == pygame.K_KP_ENTER:
                    print("enter")
                    res[0] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    res[1] = False
                if event.key == pygame.K_RIGHT:
                    res[2] = False
                if event.key == pygame.K_DOWN:
                    res[4] = False
        # print("running :",res[1],res[2])
        return res
