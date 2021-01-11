import sys

import pygame


def get(cur):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            flag = True if event.type == pygame.KEYDOWN else False
            if event.key == pygame.K_LEFT:
                cur["Left"] = flag
            if event.key == pygame.K_RIGHT:
                cur["Right"] = flag
            if event.key == pygame.K_UP:
                cur["Up"] = flag
            if event.key == pygame.K_DOWN:
                cur["Down"] = flag
            if event.key == pygame.K_KP_ENTER:
                cur["KP_Enter"] = flag
            if event.key == pygame.K_RETURN:
                cur["Enter"] = flag
            if event.key == pygame.K_ESCAPE:
                cur["Escape"] = flag
    return cur
