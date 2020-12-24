import pygame
import sys


class Input:
    def __init__(self, entities):
        self.entities = entities

    def check(self, status, direction):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    status = 1
                    direction = 0
                elif event.key == pygame.K_UP:
                    status = 2
                elif event.key == pygame.K_LEFT:
                    status = 1
                    direction = 1
                elif event.key == pygame.K_DOWN:
                    status = 3
                else:
                    status = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    status = 0
                if event.key == pygame.K_RIGHT:
                    status = 0
                if event.key == pygame.K_UP:
                    status = 0
                if event.key == pygame.K_DOWN:
                    status = 0
        return status, direction
