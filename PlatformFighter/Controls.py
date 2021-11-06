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
DARK_RED = (125, 0, 0)
DARKER_RED = (75, 0, 0)
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
pygame.display.set_caption("Rarefield Brawlers")
controlNames = ("Left Button", "Right Button", "Up Button", "Down Button", "Shield Button", "Attack Button", "Strong Button", "Special Button")
inputList = [K_TAB, K_CLEAR, K_RETURN, K_PAUSE, K_SPACE, K_QUOTE, K_MINUS,
             K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_SEMICOLON, K_EQUALS, K_LEFTBRACKET,
             K_BACKSLASH, K_RIGHTBRACKET, K_BACKQUOTE, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k,
             K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_KP0, K_KP1, K_KP2, K_KP3,
             K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9, K_KP_PERIOD, K_KP_DIVIDE, K_KP_MULTIPLY, K_KP_MINUS, K_KP_PLUS,
             K_KP_ENTER, K_KP_EQUALS, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RALT, K_LALT]


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


def controlMenu(player1keys=None, player2keys=None):
    if player1keys is None:
        player1keys = [K_LEFT, K_RIGHT, K_UP, K_DOWN, K_k, K_j, K_l, K_h]
    if player2keys is None:
        player2keys = [K_a, K_d, K_w, K_s, K_e, K_f, K_r, K_q]
    player1KeyNames = []
    player2KeyNames = []
    for x in range(len(player1keys)):
        player1KeyNames.append(pygame.key.name(player1keys[x]))
        player2KeyNames.append(pygame.key.name(player2keys[x]))

    def controlChange(controlName, controlColour, playerNum, player1Controls, player2Controls, player1ControlNames,
                      player2ControlNames):

        smallerText = pygame.font.SysFont('mingliuextbpmingliuextbmingliuhkscsextb', 20)

        shade = pygame.Surface((WIDTH, HEIGHT))
        shade.fill(controlColour)
        shade.set_alpha(10)
        shaderect = shade.get_rect()

        TextDisplay, TextDisplayrect = text_objects(("Change %s controls?" % controlName), smallerText, (200, 200, 200))
        TextDisplayrect.center = ((WIDTH / 2), (HEIGHT / 2))

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    for x in range(len(inputList) - 1):
                        pressed_keys = pygame.key.get_pressed()
                        if pressed_keys[inputList[x]]:
                            for i in range(len(controlNames)):
                                if controlName == controlNames[i]:
                                    if playerNum == 1 and (inputList[x] not in player1Controls) and (
                                            inputList[x] not in player2Controls):
                                        player1Controls[i] = inputList[x]
                                        player1ControlNames[i] = pygame.key.name(inputList[x])
                                    elif playerNum == 2 and (inputList[x] not in player1Controls) and (
                                            inputList[x] not in player2Controls):
                                        player2Controls[i] = inputList[x]
                                        player2ControlNames[i] = pygame.key.name(inputList[x])

                    return player1Controls, player2Controls, player1ControlNames, player2ControlNames

            displaysurface.blit(TextDisplay, TextDisplayrect)
            displaysurface.blit(shade, shaderect)
            pygame.display.update()
            FramePerSec.tick(60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        displaysurface.fill(GRAY)
        largeText = pygame.font.SysFont('mingliuextbpmingliuextbmingliuhkscsextb', 40)

        Textsurf, Textrect = text_objects("Player 1 controls", largeText, BLUE)
        Textrect.center = (220, 75)

        up_button1 = button("%s" % player1KeyNames[2].upper(), 140, 135, 70, 70, WHITE, DARK_GRAY)
        down_button1 = button("%s" % player1KeyNames[3].upper(), 140, 215, 70, 70, WHITE, DARK_GRAY)
        left_button1 = button("%s" % player1KeyNames[0].upper(), 60, 215, 70, 70, WHITE, DARK_GRAY)
        right_button1 = button("%s" % player1KeyNames[1].upper(), 220, 215, 70, 70, WHITE, DARK_GRAY)
        shield_button1 = button("%s" % player1KeyNames[4].upper(), 240, 125, 70, 70, WHITE, DARK_GRAY)
        attack_button1 = button("%s" % player1KeyNames[5].upper(), 320, 125, 70, 70, WHITE, DARK_GRAY)
        strong_button1 = button("%s" % player1KeyNames[6].upper(), 320, 205, 70, 70, WHITE, DARK_GRAY)
        special_button1 = button("%s" % player1KeyNames[7].upper(), 40, 125, 70, 70, WHITE, DARK_GRAY)

        if up_button1:
            controlChange("Up Button", (125, 125, 125), 1, player1keys, player2keys, player1KeyNames, player2KeyNames)
        elif down_button1:
            controlChange("Down Button", (125, 125, 125), 1, player1keys, player2keys, player1KeyNames, player2KeyNames)
        elif left_button1:
            controlChange("Left Button", (125, 125, 125), 1, player1keys, player2keys, player1KeyNames, player2KeyNames)
        elif right_button1:
            controlChange("Right Button", (125, 125, 125), 1, player1keys, player2keys, player1KeyNames,
                          player2KeyNames)
        elif shield_button1:
            controlChange("Shield Button", (125, 125, 125), 1, player1keys, player2keys, player1KeyNames,
                          player2KeyNames)
        elif attack_button1:
            controlChange("Attack Button", (125, 125, 125), 1, player1keys, player2keys, player1KeyNames,
                          player2KeyNames)
        elif strong_button1:
            controlChange("Strong Button", (125, 125, 125), 1, player1keys, player2keys, player1KeyNames,
                          player2KeyNames)
        elif special_button1:
            controlChange("Special Button", (125, 125, 125), 1, player1keys, player2keys, player1KeyNames,
                          player2KeyNames)

        Textsurf2, Textrect2 = text_objects("Player 2 controls", largeText, RED)
        Textrect2.center = (580, 75)

        up_button2 = button("%s" % player2KeyNames[2].upper(), 500, 135, 70, 70, DARK_RED, DARKER_RED)
        down_button2 = button("%s" % player2KeyNames[3].upper(), 500, 215, 70, 70, DARK_RED, DARKER_RED)
        left_button2 = button("%s" % player2KeyNames[0].upper(), 420, 215, 70, 70, DARK_RED, DARKER_RED)
        right_button2 = button("%s" % player2KeyNames[1].upper(), 580, 215, 70, 70, DARK_RED, DARKER_RED)
        shield_button2 = button("%s" % player2KeyNames[4].upper(), 600, 125, 70, 70, DARK_RED, DARKER_RED)
        attack_button2 = button("%s" % player2KeyNames[5].upper(), 680, 125, 70, 70, DARK_RED, DARKER_RED)
        strong_button2 = button("%s" % player2KeyNames[6].upper(), 680, 205, 70, 70, DARK_RED, DARKER_RED)
        special_button2 = button("%s" % player2KeyNames[7].upper(), 400, 125, 70, 70, DARK_RED, DARKER_RED)

        if up_button2:
            controlChange("Up Button", (75, 0, 0), 2, player1keys, player2keys, player1KeyNames, player2KeyNames)
        elif down_button2:
            controlChange("Down Button", (75, 0, 0), 2, player1keys, player2keys, player1KeyNames, player2KeyNames)
        elif left_button2:
            controlChange("Left Button", (75, 0, 0), 2, player1keys, player2keys, player1KeyNames, player2KeyNames)
        elif right_button2:
            controlChange("Right Button", (75, 0, 0), 2, player1keys, player2keys, player1KeyNames, player2KeyNames)
        elif shield_button2:
            controlChange("Shield Button", (75, 0, 0), 2, player1keys, player2keys, player1KeyNames, player2KeyNames)
        elif attack_button2:
            controlChange("Attack Button", (75, 0, 0), 2, player1keys, player2keys, player1KeyNames, player2KeyNames)
        elif strong_button2:
            controlChange("Strong Button", (75, 0, 0), 2, player1keys, player2keys, player1KeyNames, player2KeyNames)
        elif special_button2:
            controlChange("Special Button", (75, 0, 0), 2, player1keys, player2keys, player1KeyNames, player2KeyNames)

        back_button = button("Back", 0, 0, 50, 50, (0, 255, 255), GREEN)

        if back_button:
            return player1keys, player2keys

        displaysurface.blit(Textsurf, Textrect)
        displaysurface.blit(Textsurf2, Textrect2)

        pygame.display.update()
        FramePerSec.tick(30)
