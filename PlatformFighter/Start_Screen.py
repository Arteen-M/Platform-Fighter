import pygame
from pygame.locals import *
import sys

vec = pygame.math.Vector2

pygame.init()
pygame.mixer.init()

HEIGHT = 600
WIDTH = 800
RED = (255, 0, 0)
WHITE = (255, 255, 255)

FPS = 60
FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rarefield Brawlers")


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def startScreen():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    intro = False

        displaysurface.fill((0, 0, 0))
        largeText = pygame.font.Font('freesansbold.ttf', 90)
        smallText = pygame.font.Font("freesansbold.ttf", 45)
        TextSurf, TextRect = text_objects("Platform Fighter", largeText, RED)  # Rarefield Brawlers
        smallTextSurf, smallTextRect = text_objects("Press Space to Start", smallText, RED)
        TextRect.center = ((WIDTH / 2), (HEIGHT / 2))
        smallTextRect.center = ((WIDTH / 2), (HEIGHT / 2 + 100))
        displaysurface.blit(TextSurf, TextRect)
        displaysurface.blit(smallTextSurf, smallTextRect)
        pygame.display.update()
        FramePerSec.tick(FPS)

