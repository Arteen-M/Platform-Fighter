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
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
DARK_GRAY = (125, 125, 150)

FPS = 60
FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Fighter")


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
    pygame.draw.rect(displaysurface, BLACK, (x, y, w, h), 1)

    smallText = pygame.font.SysFont("mingliuextbpmingliuextbmingliuhkscsextb", 20)
    textSurf, textRect = text_objects(msg, smallText, BLUE)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    displaysurface.blit(textSurf, textRect)


def charSelect(hitbox_toggle=False):
    player1_chosen = False
    char_tuple = []
    code = [False, False, False, False, False, False, False]
    code_check = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_a:
                    code[0] = True
                if event.key == K_r and code[0]:
                    code[1] = True
                if event.key == K_t and code[1]:
                    code[2] = True
                if event.key == K_e and code[2]:
                    code[3] = True
                if event.key == K_e and code[3]:
                    code[4] = True
                if event.key == K_n and code[4]:
                    code[5] = True
                if event.key == K_s and code[5]:
                    code[6] = True

        if code[0] and code[1] and code[2] and code[3] and code[4] and code[5] and code[6]:
            code_check = True
        displaysurface.fill(GRAY)

        control_button = button("Controls", (WIDTH - 125), 25, 100, 50, WHITE, DARK_GRAY)
        option_button = button("Options", 25, 25, 100, 50, WHITE, DARK_GRAY)

        if hitbox_toggle:
            hitbox_display = button("ON", 75, 525, 50, 50, WHITE, DARK_GRAY)

            if hitbox_display:
                hitbox_toggle = False
                time.sleep(0.25)
        else:
            hitbox_display = button("OFF", 75, 525, 50, 50, WHITE, DARK_GRAY)

            if hitbox_display:
                hitbox_toggle = True
                time.sleep(0.25)

        if control_button:
            return "Controls"
        elif option_button:
            return "Options"

        largeText = pygame.font.SysFont('mingliuextbpmingliuextbmingliuhkscsextb', 30)

        hitboxSurf, hitboxRect = text_objects("Show Hitbox", largeText, BLUE)
        hitboxRect.center = (100, 500)

        stick_select = button("Stickman", (2 * WIDTH / 3), (2 * HEIGHT / 3), 100, 50, WHITE, DARK_GRAY)

        if stick_select and not player1_chosen:
            player1_chosen = True
            stick_select = False
            char_tuple.append("Stickman")
            time.sleep(0.25)

        if stick_select and player1_chosen:
            char_tuple.append("Stickman")
            time.sleep(0.25)
            return char_tuple, hitbox_toggle, code_check

        if player1_chosen:
            TextSurf, TextRect = text_objects("Player 2: Choose your character", largeText, RED)
            TextRect.center = ((WIDTH / 3 + 125), 55)
        else:
            TextSurf, TextRect = text_objects("Player 1: Choose your character", largeText, BLUE)
            TextRect.center = ((WIDTH / 3 + 125), 55)

        if len(char_tuple) == 2:
            return char_tuple, hitbox_toggle, code_check

        displaysurface.blit(TextSurf, TextRect)
        displaysurface.blit(hitboxSurf, hitboxRect)

        pygame.display.update()
        FramePerSec.tick(60)

