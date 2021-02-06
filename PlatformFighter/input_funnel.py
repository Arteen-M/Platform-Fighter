import pygame
from pygame.locals import *
import sys


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
counter = 0
left = False
right = False
up = False
down = False
attack = False
smash = False
shield = False

input_methods_1 = [left, right, up, down, attack, smash, shield]

left2 = False
right2 = False
up2 = False
down2 = False
attack2 = False
smash2 = False
shield2 = False

input_methods_2 = [left2, right2, up2, down2, attack2, smash2, shield2]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pressed_keys = pygame.key.get_pressed()
    pressed_keys_2 = pygame.key.get_pressed()

    if pressed_keys[K_LEFT]:
        left = True
    else:
        left = False
    if pressed_keys[K_RIGHT]:
        right = True
    else:
        right = False
    if pressed_keys[K_DOWN]:
        down = True
    else:
        down = False
    if pressed_keys[K_UP]:
        up = True
    else:
        up = False
    if pressed_keys[K_PERIOD]:
        attack = True
    else:
        attack = False
    if pressed_keys[K_COMMA]:
        shield = True
    else:
        shield = False
    if pressed_keys[K_SLASH]:
        smash = True
    else:
        smash = False

    input_methods_1 = [left, right, up, down, attack, smash, shield]

    if pressed_keys[K_a]:
        left2 = True
    else:
        left2 = False
    if pressed_keys[K_d]:
        right2 = True
    else:
        right2 = False
    if pressed_keys[K_s]:
        down2 = True
    else:
        down2 = False
    if pressed_keys[K_w]:
        up2 = True
    else:
        up2 = False
    if pressed_keys[K_e]:
        attack2 = True
    else:
        attack2 = False
    if pressed_keys[K_f]:
        shield2 = True
    else:
        shield2 = False
    if pressed_keys[K_r]:
        smash2 = True
    else:
        smash2 = False

    input_methods_2 = [left2, right2, up2, down2, attack2, smash2, shield2]

    counter += 1
    if counter == 60:
        counter = 0

    if attack:
        if left or right:
            print("F-tilt 1")
        elif up:
            print("Up-tilt 1")
        elif down:
            print("Down-tilt 1")
        else:
            print("Jab 1")

    elif smash:
        if left or right:
            print("F-Smash 1")
        elif up:
            print("Up-Smash 1")
        elif down:
            print("Down-Smash 1")
        else:
            print("F-Smash 1")

    elif shield:
        if left:
            print("Shield-Left 1")
        elif right:
            print("Shield-Right 1")
        else:
            print("Shield 1")

    if attack2:
        if left2 or right2:
            print("F-tilt 2")
        elif up2:
            print("Up-tilt 2")
        elif down2:
            print("Down-tilt 2")
        else:
            print("Jab 2")

    elif smash2:
        if left2 or right2:
            print("F-Smash 2")
        elif up2:
            print("Up-Smash 2")
        elif down2:
            print("Down-Smash 2")
        else:
            print("F-Smash 2")

    elif shield2:
        if left2:
            print("Shield-Left 2")
        elif right2:
            print("Shield-Right 2")
        else:
            print("Shield 2")

    print(input_methods_1)
    print(input_methods_2)

    FramePerSec.tick(FPS)
    pygame.display.update()
