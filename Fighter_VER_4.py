import pygame
import sys
import time
from pygame.locals import *
from PlatformFighter import PlayerStickman

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
activity_1 = False
activity_2 = False
attack_angle_1 = ()
attack_angle_2 = ()
controlNames = ("Left Button", "Right Button", "Up Button", "Down Button", "Shield Button", "Attack Button")

inputList = [K_TAB, K_CLEAR, K_RETURN, K_PAUSE, K_SPACE, K_QUOTE, K_COMMA, K_MINUS, K_PERIOD, K_SLASH,
             K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_SEMICOLON, K_EQUALS, K_LEFTBRACKET,
             K_BACKSLASH, K_RIGHTBRACKET, K_BACKQUOTE, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k,
             K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_KP0, K_KP1, K_KP2, K_KP3,
             K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9, K_KP_PERIOD, K_KP_DIVIDE, K_KP_MULTIPLY, K_KP_MINUS, K_KP_PLUS,
             K_KP_ENTER, K_KP_EQUALS, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RALT, K_LALT]

fonts = pygame.font.Font('freesansbold.ttf', 32)


class Percent(pygame.sprite.Sprite):
    def __init__(self, font, numPlayer):
        super().__init__()
        self.display = "0%"
        self.font = font
        self.numPlayer = numPlayer
        if self.numPlayer == 1:
            self.colour = (255, 0, 0)
            self.text = self.font.render(self.display, True, self.colour, (0, 0, 0))
            self.textRect = self.text.get_rect(center=(675, 550))
        else:
            self.colour = (255, 255, 255)
            self.text = self.font.render(self.display, True, self.colour, (0, 0, 0))
            self.textRect = self.text.get_rect(center=(125, 550))

    def update(self, damage):
        self.display = str(damage) + "%"
        self.text = self.font.render(self.display, True, self.colour, (0, 0, 0))
        if self.numPlayer == 1:
            self.textRect = self.text.get_rect(center=(675, 550))
        else:
            self.textRect = self.text.get_rect(center=(125, 550))


class timerClass:
    def __init__(self, timer, font):
        super().__init__()
        self.timer = timer
        self.font = font
        self.colour = WHITE
        self.display = "%d:00" % self.timer
        self.text = self.font.render(self.display, True, self.colour, (0, 0, 0))
        self.textRect = self.text.get_rect(center=(WIDTH - 100, 100))

    def update(self, seconds, minutes):
        if 60 - seconds < 10:
            self.display = "%d:0%d" % ((self.timer - minutes - 1), (60 - seconds))
        else:
            self.display = "%d:%d" % ((self.timer - minutes - 1), (60 - seconds))
        self.text = self.font.render(self.display, True, self.colour, (0, 0, 0))
        self.textRect = self.text.get_rect(center=(WIDTH - 100, 100))


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, surface, center):
        super().__init__()
        self.surf = pygame.Surface(surface)
        self.rect = self.surf.get_rect(center=center)

    def update(self, surface, center):
        self.surf = pygame.Surface(surface)
        self.rect = self.surf.get_rect(center=center)


class emptyBox(pygame.sprite.Sprite):
    def __init__(self, surface, center):
        super().__init__()
        self.surf = pygame.Surface(surface)
        self.surf.set_alpha(100)
        self.rect = self.surf.get_rect(center=center)

    def update(self, surface, center, colour):
        if colour is not None:
            self.surf = pygame.Surface(surface)
            self.surf.fill(colour)
            self.surf.set_alpha(100)
        else:
            self.surf = pygame.Surface(surface)
            self.surf.set_alpha(0)

        self.rect = self.surf.get_rect(center=center)


class imageBox(pygame.sprite.Sprite):
    def __init__(self, surface, center):
        super().__init__()
        self.surf = pygame.Surface(surface)
        self.rect = self.surf.get_rect(center=center)

    def update(self, img, center):
        self.surf = pygame.image.load(img)
        self.rect = self.surf.get_rect(center=center)


class Shield(pygame.sprite.Sprite):
    def __init__(self, surface, center, colour):
        super().__init__()
        self.surf = pygame.Surface(surface)
        self.rect = self.surf.get_rect(center=center)
        self.colour = colour

    def update(self, surface, center):
        self.surf = pygame.Surface(surface)
        self.surf.fill(self.colour)
        self.rect = self.surf.get_rect(center=center)


# class Stage(pygame.sprite.Sprite):
#    def __init__(self, dimensions, colour, center):
#       super().__init__()
#        self.surf = pygame.Surface(dimensions)
#       self.surf.fill(colour)
#        self.rect = self.surf.get_rect(center=center)


class StageTop(pygame.sprite.Sprite):
    def __init__(self, width, length, cooX, cooY):
        super().__init__()
        self.surf = pygame.Surface((length, width))
        self.surf.fill((0, 0, 255))
        self.rect = self.surf.get_rect(center=(cooX, cooY))


class StageSide(pygame.sprite.Sprite):
    def __init__(self, position, width):
        super().__init__()
        self.surf = pygame.Surface((width, HEIGHT - 280))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(position, HEIGHT - 3))


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


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


# def stockGraphicSquare(numStocks, numPlayer):
#   for i in range(numStocks):
#      if numPlayer == 1:
#         pygame.draw.rect(displaysurface, RED, (100 + (i * 10), 520, 20, 10))
#    else:
#       pygame.draw.rect(displaysurface, WHITE, (675 - (i * 10), 520, 20, 10))


def stockGraphicStick(numStocks, numPlayer, img):
    for i in range(numStocks):
        if numPlayer == 1:
            displaysurface.blit(pygame.image.load(img), (650 - (i * 30), 470))
        else:
            displaysurface.blit(pygame.image.load(img), (50 + (i * 30), 470))


def playMusic(song, repeat=-1, start=0, volume=0.3):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(repeat, start=start)
    pygame.mixer.music.set_volume(volume)


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


def controlMenu(player1keys=None, player2keys=None):
    if player1keys is None:
        player1keys = [K_LEFT, K_RIGHT, K_UP, K_DOWN, K_COMMA, K_PERIOD]
    if player2keys is None:
        player2keys = [K_a, K_d, K_w, K_s, K_e, K_f]
    player1KeyNames = []
    player2KeyNames = []
    for x in range(len(player1keys)):
        player1KeyNames.append(pygame.key.name(player1keys[x]))
        player2KeyNames.append(pygame.key.name(player2keys[x]))

    def controlChange(controlName, controlColour, playerNum, player1Controls, player2Controls, player1ControlNames,
                      player2ControlNames):

        smallerText = pygame.font.Font('freesansbold.ttf', 20)

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

        displaysurface.fill((0, 0, 0))
        largeText = pygame.font.Font('freesansbold.ttf', 40)

        Textsurf, Textrect = text_objects("Player 1 controls", largeText, RED)
        Textrect.center = (220, 75)

        up_button1 = button("%s" % player1KeyNames[2].upper(), 140, 135, 70, 70, (125, 0, 0), (75, 0, 0))
        down_button1 = button("%s" % player1KeyNames[3].upper(), 140, 215, 70, 70, (125, 0, 0), (75, 0, 0))
        left_button1 = button("%s" % player1KeyNames[0].upper(), 60, 215, 70, 70, (125, 0, 0), (75, 0, 0))
        right_button1 = button("%s" % player1KeyNames[1].upper(), 220, 215, 70, 70, (125, 0, 0), (75, 0, 0))
        shield_button1 = button("%s" % player1KeyNames[4].upper(), 240, 125, 70, 70, (125, 0, 0), (75, 0, 0))
        attack_button1 = button("%s" % player1KeyNames[5].upper(), 320, 125, 70, 70, (125, 0, 0), (75, 0, 0))

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

        Textsurf2, Textrect2 = text_objects("Player 2 controls", largeText, WHITE)
        Textrect2.center = (580, 75)

        up_button2 = button("%s" % player2KeyNames[2].upper(), 500, 135, 70, 70, (255, 255, 255), (125, 125, 125))
        down_button2 = button("%s" % player2KeyNames[3].upper(), 500, 215, 70, 70, (255, 255, 255), (125, 125, 125))
        left_button2 = button("%s" % player2KeyNames[0].upper(), 420, 215, 70, 70, (255, 255, 255), (125, 125, 125))
        right_button2 = button("%s" % player2KeyNames[1].upper(), 580, 215, 70, 70, (255, 255, 255), (125, 125, 125))
        shield_button2 = button("%s" % player2KeyNames[4].upper(), 600, 125, 70, 70, (255, 255, 255), (125, 125, 125))
        attack_button2 = button("%s" % player2KeyNames[5].upper(), 680, 125, 70, 70, (255, 255, 255), (125, 125, 125))

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

        back_button = button("Back", 0, 0, 50, 50, (0, 255, 255), (0, 255, 0))

        if back_button:
            return player1keys, player2keys

        displaysurface.blit(Textsurf, Textrect)
        displaysurface.blit(Textsurf2, Textrect2)

        pygame.display.update()
        FramePerSec.tick(30)


def optionMenu(timer=1, stockCount=3):
    stock3 = False
    stock2 = False
    stock1 = False

    timer1 = False
    timer2 = False
    timer3 = False
    timer4 = False

    if stockCount == 3:
        stock3 = True
    elif stockCount == 2:
        stock2 = True
    elif stockCount == 1:
        stock1 = True

    if timer == 1:
        timer = "1:00"
        timer1 = True
    elif timer == 2:
        timer = "2:00"
        timer2 = True
    elif timer == 3:
        timer = "3:00"
        timer3 = True
    elif timer == 4:
        timer = "4:00"
        timer4 = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        displaysurface.fill((0, 0, 0))

        largeText = pygame.font.Font('freesansbold.ttf', 30)
        TextSurf, TextRect = text_objects(("Stock Count: %d" % stockCount), largeText, RED)
        TextRect.center = ((WIDTH / 3 - 100), 55)

        Text2Surf, Text2Rect = text_objects(("Timer: %s" % timer), largeText, RED)
        Text2Rect.center = ((2 * WIDTH / 3 + 100), 55)

        stock_1 = button("1 Stock", WIDTH / 3 - 175, 105, 100, 50, (0, 255, 255), (0, 255, 0))
        stock_2 = button("2 Stock", WIDTH / 3 - 175, 155, 100, 50, (0, 255, 255), (0, 255, 0))
        stock_3 = button("3 Stock", WIDTH / 3 - 175, 205, 100, 50, (0, 255, 255), (0, 255, 0))

        if stock_1:
            stockCount = 1
            stock1 = True
            stock2 = False
            stock3 = False
        elif stock_2:
            stockCount = 2
            stock2 = True
            stock3 = False
            stock1 = False
        elif stock_3:
            stockCount = 3
            stock3 = True
            stock2 = False
            stock1 = False

        timer_1 = button("1 Minute", (2 * WIDTH / 3) + 50, 105, 100, 52, (0, 255, 255), (0, 255, 0))
        timer_2 = button("2 Minutes", (2 * WIDTH / 3) + 50, 157, 100, 52, (0, 255, 255), (0, 255, 0))
        timer_3 = button("3 Minutes", (2 * WIDTH / 3) + 50, 209, 100, 52, (0, 255, 255), (0, 255, 0))
        timer_4 = button("4 Minutes", (2 * WIDTH / 3) + 50, 261, 100, 52, (0, 255, 255), (0, 255, 0))

        if timer_1:
            timer = "1:00"
            timer1 = True
            timer2 = False
            timer3 = False
            timer4 = False
        elif timer_2:
            timer = "2:00"
            timer1 = False
            timer2 = True
            timer3 = False
            timer4 = False
        elif timer_3:
            timer = "3:00"
            timer1 = False
            timer2 = False
            timer3 = True
            timer4 = False
        elif timer_4:
            timer = "4:00"
            timer1 = False
            timer2 = False
            timer3 = False
            timer4 = True

        back_button = button("Back", 0, 0, 50, 50, (0, 255, 255), (0, 255, 0))

        if back_button:

            if timer1:
                timer = 1
            elif timer2:
                timer = 2
            elif timer3:
                timer = 3
            elif timer4:
                timer = 4
            time.sleep(0.5)
            return stockCount, timer

        displaysurface.blit(TextSurf, TextRect)
        displaysurface.blit(Text2Surf, Text2Rect)

        pygame.display.update()
        FramePerSec.tick(30)


def main(attack_angle_1, attack_angle_2, activity_1, activity_2, P1, P2, P1Char, P2Char, player1Left, player1Right,
         player1Up, player1Down, player1Shield, player1Attack, player2Left, player2Right, player2Up, player2Down,
         player2Shield, player2Attack, song, timer=1):
    counter = 0
    seconds = 0
    minutes = 0
    # playMusic(song)
    while not (P1.end or P2.end):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == player1Up:
                    P1.jump()
                if event.key == player2Up:
                    P2.jump()

        displaysurface.fill((0, 0, 0))
        # P1.findBuffer(player1Left, player2Right, player1Up, player1Down, player1Attack, player1Shield)
        P1jumps = P1.get_Jumps()
        P2jumps = P2.get_Jumps()

        P1shield_dir = P1.shielding(player1Shield, player1Left, player1Right, player1Up, player1Down)
        P2shield_dir = P2.shielding(player2Shield, player2Left, player2Right, player2Up, player2Down)

        P1.move(player1Left, player1Right, player1Down)
        attack_angle_1 = P1.get_angle(attack_angle_1, attack_angle_2)
        P1.attack(player1Attack, player1Left, player1Right, player1Up, player1Down)
        P1.update(P1, attack_angle_2, tops, sides_left, sides_right, plats, under_plats, P2jumps, P2shield_dir,
                  shield_2, P2.pos.x)

        P1box.update((P1.hitbox_length, P1.hitbox_height), (P1.hitbox_pos_x, P1.hitbox_pos_y))
        P1box2.update((P1.hitbox_length2, P1.hitbox_height2), (P1.hitbox_pos_x2, P1.hitbox_pos_y2))

        P1Dis.update((P1.hitbox_length, P1.hitbox_height), (P1.hitbox_pos_x, P1.hitbox_pos_y), P1.attack_colour)
        P1Dis2.update((P1.hitbox_length2, P1.hitbox_height2), (P1.hitbox_pos_x2, P1.hitbox_pos_y2), P1.attack_colour)

        activity_1 = P1.createHit(activity_1, activity_2)

        P1.getHit(P1, player2box_1, activity_1, activity_2, P1shield, player2box_2)

        P1percent.update(P1.percentage)

        P1shield.update((P1.shield_length, P1.shield_height), (P1.shield_pos_x, P1.shield_pos_y))

        P1hurt.update(P1.image, (P1.hurt_pos_x, P1.hurt_pos_y))

        if P1Char == "Stickman":
            stockGraphicStick(P1.stocks, 1,
                              "../PlatformFighter/Stickman Character/stick_stock_graphic.png")
        # P2.findBuffer(player1Left, player1Right, player1Up, player1Down, player1Attack, player1Shield)
        P2.move(player2Left, player2Right, player2Down)
        attack_angle_2 = P2.get_angle(attack_angle_1, attack_angle_2)
        P2.attack(player2Attack, player2Left, player2Right, player2Up, player2Down)
        P2.update(P2, attack_angle_1, tops, sides_left, sides_right, plats, under_plats, P1jumps, P1shield_dir,
                  shield_1, P1.pos.x)

        P2box.update((P2.hitbox_length, P2.hitbox_height), (P2.hitbox_pos_x, P2.hitbox_pos_y))
        P2box2.update((P2.hitbox_length2, P2.hitbox_height2), (P2.hitbox_pos_x2, P2.hitbox_pos_y2))

        P2Dis.update((P2.hitbox_length, P2.hitbox_height), (P2.hitbox_pos_x, P2.hitbox_pos_y), P2.attack_colour)
        P2Dis2.update((P2.hitbox_length2, P2.hitbox_height2), (P2.hitbox_pos_x2, P2.hitbox_pos_y2), P2.attack_colour)

        activity_2 = P2.createHit(activity_1, activity_2)

        P2.getHit(P2, player1box_1, activity_1, activity_2, P2shield, player1box_2)

        P2percent.update(P2.percentage)

        P2shield.update((P2.shield_length, P2.shield_height), (P2.shield_pos_x, P2.shield_pos_y))

        P2hurt.update(P2.image, (P2.hurt_pos_x, P2.hurt_pos_y))

        Gametime.update(seconds, minutes)
        if P2Char == "Stickman":
            stockGraphicStick(P2.stocks, 2,
                              "../PlatformFighter/Stickman Character/stick_stock_graphic.png")
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
        for entity in texts:
            displaysurface.blit(entity.text, entity.textRect)

        displaysurface.blit(Gametime.text, Gametime.textRect)

        counter += 1

        if counter == 60:
            counter = 0
            seconds += 1
        if seconds == 60:
            seconds = 0
            minutes += 1
        if minutes == timer:
            print("TIME!")
            break

        pygame.display.update()
        FramePerSec.tick(FPS)

    pygame.mixer.music.stop()


startScreen()

player1ControlList = [K_LEFT, K_RIGHT, K_UP, K_DOWN, K_COMMA, K_PERIOD]
player2ControlList = [K_a, K_d, K_w, K_s, K_e, K_f]
stockCount = 3
GameTimer = 1

while True:
    charLoop = True
    next_action = []
    while charLoop:
        next_action = charSelect()
        hitbox_on_off = next_action[1]

        if next_action == "Controls":
            controlList = controlMenu(player1ControlList, player2ControlList)
            player1ControlList = controlList[0]
            player2ControlList = controlList[1]
        elif next_action == "Options":
            optionsList = optionMenu(GameTimer, stockCount)
            stockCount = optionsList[0]
            GameTimer = optionsList[1]
        else:
            charLoop = False

    if next_action[0][0] == "Stickman":
        P1 = PlayerStickman.PlayerStickman(RED, 1, hitbox_on_off, stockCount)
        P1Char = "Stickman"
    else:
        P1 = PlayerStickman.PlayerStickman(RED, 1, hitbox_on_off, stockCount)
        P1Char = "Stickman"
    if next_action[0][1] == "Stickman":
        P2 = PlayerStickman.PlayerStickman(WHITE, 2, hitbox_on_off, stockCount)
        P2Char = "Stickman"
    else:
        P2 = PlayerStickman.PlayerStickman(WHITE, 2, hitbox_on_off, stockCount)
        P2Char = "Stickman"

    #  INITIALIZATION
    # PT1 = Stage(((WIDTH/2), 310), (0, 191, 255), ((WIDTH/2), (HEIGHT - 10)))
    PT2 = StageTop(5, WIDTH / 2, WIDTH / 2, HEIGHT - 165)
    PT3 = StageSide(575, 50)
    PT4 = StageSide(225, 50)
    PT5 = StageTop(6, 100, 525, HEIGHT - 229)
    PT6 = StageTop(6, 100, 275, HEIGHT - 229)
    PT7 = StageTop(1, 100, 525, HEIGHT - 227)
    PT8 = StageTop(1, 100, 275, HEIGHT - 227)
    P1hurt = imageBox((0, 0), (0, 0))
    P2hurt = imageBox((0, 0), (0, 0))
    P1box = Hitbox((0, 0), (0, 0))
    P2box = Hitbox((0, 0), (0, 0))
    P1box2 = Hitbox((0, 0), (0, 0))
    P2box2 = Hitbox((0, 0), (0, 0))
    P1Dis = emptyBox((0, 0), (0, 0))
    P2Dis = emptyBox((0, 0), (0, 0))
    P1Dis2 = emptyBox((0, 0), (0, 0))
    P2Dis2 = emptyBox((0, 0), (0, 0))
    P1shield = Shield((0, 0), (0, 0), RED)
    P2shield = Shield((0, 0), (0, 0), WHITE)
    P1percent = Percent(fonts, 1)
    P2percent = Percent(fonts, 2)
    Gametime = timerClass(GameTimer, fonts)

    # All Sprites group
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(P2)
    all_sprites.add(P1shield)
    all_sprites.add(P2shield)
    all_sprites.add(P1hurt)
    all_sprites.add(P2hurt)
    # all_sprites.add(P1box)
    # all_sprites.add(P1box2)
    if hitbox_on_off:
        all_sprites.add(P1Dis)  # HITBOX DISPLAY
        all_sprites.add(P1Dis2)  # HITBOX DISPLAY
        all_sprites.add(P2Dis)  # HITBOX DISPLAY
        all_sprites.add(P2Dis2)  # HITBOX DISPLAY
    # all_sprites.add(P2box)
    # all_sprites.add(P2box2)
    all_sprites.add(PT2)
    all_sprites.add(PT3)
    all_sprites.add(PT4)
    # all_sprites.add(PT1)
    all_sprites.add(PT5)
    all_sprites.add(PT6)
    all_sprites.add(PT7)
    all_sprites.add(PT8)

    # Text groups
    texts = pygame.sprite.Group()
    texts.add(P1percent)
    texts.add(P2percent)

    # Player (hurtbox) group
    all_players = pygame.sprite.Group()
    all_players.add(P1)
    all_players.add(P2)

    # Player 1 group
    player1box_1 = pygame.sprite.Group()
    player1box_1.add(P1box)

    # Player 2 group
    player2box_1 = pygame.sprite.Group()
    player2box_1.add(P2box)

    # Player 1 (2) Group
    player1box_2 = pygame.sprite.Group()
    player1box_2.add(P1box2)

    # Player 2 (2) Group
    player2box_2 = pygame.sprite.Group()
    player2box_2.add(P2box2)

    # Player 1 Shield group
    shield_1 = pygame.sprite.Group()
    shield_1.add(P1shield)

    # Player 2 Shield group
    shield_2 = pygame.sprite.Group()
    shield_2.add(P2shield)

    # Stage top
    tops = pygame.sprite.Group()
    tops.add(PT2)

    # Platforms
    plats = pygame.sprite.Group()
    plats.add(PT5)
    plats.add(PT6)

    under_plats = pygame.sprite.Group()
    under_plats.add(PT7)
    under_plats.add(PT8)

    # Stage sides
    sides_left = pygame.sprite.Group()
    sides_left.add(PT4)

    sides_right = pygame.sprite.Group()
    sides_right.add(PT3)

    # All stage elements
    stage_elements = pygame.sprite.Group()
    # stage_elements.add(PT1)
    stage_elements.add(PT2)
    stage_elements.add(PT3)
    stage_elements.add(PT4)
    stage_elements.add(PT5)
    stage_elements.add(PT6)

    main(attack_angle_1, attack_angle_2, activity_1, activity_2, P1, P2, P1Char, P2Char,
         player1Left=player1ControlList[0], player1Right=player1ControlList[1], player1Up=player1ControlList[2],
         player1Down=player1ControlList[3], player1Shield=player1ControlList[4], player1Attack=player1ControlList[5],
         player2Left=player2ControlList[0], player2Right=player2ControlList[1], player2Up=player2ControlList[2],
         player2Down=player2ControlList[3], player2Shield=player2ControlList[4], player2Attack=player2ControlList[5],
         song="../PlatformFighter/MUSIC/DontStop (1).wav", timer=GameTimer)
    time.sleep(2)
