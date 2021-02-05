import pygame
from pygame.locals import *
import sys
import time

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


def button(msg, x, y, w, h, ic, ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(displaysurface, ac, (x, y, w, h))
        if click[0] == 1:
            return True

    else:
        pygame.draw.rect(displaysurface, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText, RED)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    displaysurface.blit(textSurf, textRect)


def charSelect(hitbox_toggle=False):
    player1_chosen = False
    char_tuple = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        displaysurface.fill((0, 0, 0))

        control_button = button("Controls", (WIDTH - 125), 25, 100, 50, (0, 255, 255), (0, 255, 0))
        option_button = button("Options", 25, 25, 100, 50, (0, 255, 255), (0, 255, 0))

        if hitbox_toggle:
            hitbox_display = button("ON", 75, 525, 50, 50, (0, 255, 255), (0, 255, 0))

            if hitbox_display:
                hitbox_toggle = False
                time.sleep(0.25)
        else:
            hitbox_display = button("OFF", 75, 525, 50, 50, (0, 255, 255), (0, 255, 0))

            if hitbox_display:
                hitbox_toggle = True
                time.sleep(0.25)

        if control_button:
            return "Controls"
        elif option_button:
            return "Options"

        largeText = pygame.font.Font('freesansbold.ttf', 30)

        hitboxSurf, hitboxRect = text_objects("Show Hitbox", largeText, RED)
        hitboxRect.center = (100, 500)

        stick_select = button("Stickman", (2 * WIDTH / 3), (2 * HEIGHT / 3), 100, 50, (0, 255, 255), (0, 255, 0))

        if stick_select and not player1_chosen:
            player1_chosen = True
            stick_select = False
            char_tuple.append("Stickman")
            time.sleep(0.25)

        if stick_select and player1_chosen:
            char_tuple.append("Stickman")
            time.sleep(0.25)
            return char_tuple, hitbox_toggle

        if player1_chosen:
            TextSurf, TextRect = text_objects("Player 2: Choose your character", largeText, WHITE)
            TextRect.center = ((WIDTH / 3 + 125), 55)
        else:
            TextSurf, TextRect = text_objects("Player 1: Choose your character", largeText, RED)
            TextRect.center = ((WIDTH / 3 + 125), 55)

        if len(char_tuple) == 2:
            return char_tuple, hitbox_toggle

        displaysurface.blit(TextSurf, TextRect)
        displaysurface.blit(hitboxSurf, hitboxRect)

        pygame.display.update()
        FramePerSec.tick(60)
