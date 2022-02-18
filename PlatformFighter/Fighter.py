import random
import sys
import time

import pygame
from pygame.locals import *

import Character_Select
import Controls
import PlayerStickman
import Start_Screen

vec = pygame.math.Vector2

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(1)

HEIGHT = 600
WIDTH = 800
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
DARK_GRAY = (125, 125, 150)

FPS = 60
FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Fighter")

attack_angle_1 = ()
attack_angle_2 = ()
hitbox_on_off = False
controlNames = (
    "Left Button", "Right Button", "Up Button", "Down Button", "Shield Button", "Attack Button", "Special Button")
songList = ["../PlatformFighter/MUSIC/PlatformBanger2 (3).wav"]

inputList = [K_TAB, K_CLEAR, K_RETURN, K_PAUSE, K_SPACE, K_QUOTE, K_MINUS,
             K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_SEMICOLON, K_EQUALS, K_LEFTBRACKET,
             K_BACKSLASH, K_RIGHTBRACKET, K_BACKQUOTE, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k,
             K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_KP0, K_KP1, K_KP2, K_KP3,
             K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9, K_KP_PERIOD, K_KP_DIVIDE, K_KP_MULTIPLY, K_KP_MINUS, K_KP_PLUS,
             K_KP_ENTER, K_KP_EQUALS, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RALT, K_LALT]

fonts = pygame.font.SysFont('mingliuextbpmingliuextbmingliuhkscsextb', 32)


class Percent(pygame.sprite.Sprite):
    def __init__(self, font, numPlayer):
        super().__init__()
        self.display = "0%"
        self.font = font
        self.numPlayer = numPlayer
        self.textSurf = 0
        self.textRect = 0
        if self.numPlayer == 1:
            self.colour = BLUE
        else:
            self.colour = RED

    def update(self, damage):
        self.display = str(damage) + "%"
        Text = pygame.font.SysFont("mingliuextbpmingliuextbmingliuhkscsextb", 36)
        self.textSurf, self.textRect = text_objects(self.display, Text, self.colour)

        if self.numPlayer == 1:
            self.textRect.center = (675, 550)
        else:
            self.textRect.center = (125, 550)


class timerClass:
    def __init__(self, timer, font):
        super().__init__()
        self.timer = timer
        self.font = font
        self.colour = WHITE
        self.display = "%d:00" % self.timer
        self.textSurf = 0
        self.text = self.font.render(self.display, True, self.colour, (0, 0, 0))
        self.textRect = self.text.get_rect(center=(WIDTH - 100, 100))
        self.seconds = 1
        self.minutes = 0
        self.counter = 0

    def update(self):

        if 60 - self.seconds < 10:
            self.display = "%d:0%d" % ((self.timer - self.minutes - 1), (60 - self.seconds))
        else:
            self.display = "%d:%d" % ((self.timer - self.minutes - 1), (60 - self.seconds))

        Text = pygame.font.SysFont("mingliuextbpmingliuextbmingliuhkscsextb", 50)
        self.textSurf, self.textRect = text_objects(self.display, Text, BLACK)
        self.textRect.center = (WIDTH - 100, 100)

        self.counter += 1

        if self.counter == 60:
            self.counter = 0
            self.seconds += 1

        if self.seconds == 60:
            self.seconds = 0
            self.minutes += 1

        if self.minutes == self.timer:
            return True
        else:
            return False


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
        if img is not None:
            self.surf = img
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


class Stage(pygame.sprite.Sprite):
    def __init__(self, dimensions, colour, center):
        super().__init__()
        self.surf = pygame.Surface(dimensions)
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center=center)


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


class Slider:
    def __init__(self, x, y, w, h, msg):
        self.sliderRect = pygame.Rect(x, y, w, h)
        self.volume = 0.3
        self.circle_x = self.volume * (self.sliderRect.w + self.sliderRect.x)
        self.circle_radius = self.sliderRect.h * 1.5
        self.mouse = 0
        self.msg = msg
        self.msg_display = msg
        smallText = pygame.font.SysFont("mingliuextbpmingliuextbmingliuhkscsextb", 20)
        self.textSurf, self.textRect = text_objects(msg, smallText, BLUE)
        self.textRect.center = (x + (w / 2), (y + 50))

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.sliderRect)
        pygame.draw.circle(screen, WHITE, (self.circle_x, self.sliderRect.y + self.sliderRect.h / 2),
                           self.circle_radius)

        smallText = pygame.font.SysFont("mingliuextbpmingliuextbmingliuhkscsextb", 20)
        self.msg_display = self.msg + ": %d" % (int(self.volume * 100))

        self.textSurf, self.textRect = text_objects(self.msg_display, smallText, BLUE)
        self.textRect.center = (self.sliderRect.x + (self.sliderRect.w / 2), (self.sliderRect.y + 50))
        screen.blit(self.textSurf, self.textRect)

    def volume_update(self):
        self.volume = self.circle_x / (self.sliderRect.w + self.sliderRect.x)
        if self.volume <= 0.24:
            self.volume = 0
        if self.volume >= 0.98:
            self.volume = 1

    def move(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.circle_x - self.circle_radius < mouse[0] < self.circle_x + self.circle_radius and \
                self.sliderRect.y - self.circle_radius < mouse[1] < self.sliderRect.y + self.circle_radius and \
                click[0] == 1:
            self.mouse = mouse[0]

        if click[0] == 1 and mouse[0] != self.mouse and \
                self.sliderRect.x <= mouse[0] <= self.sliderRect.x + self.sliderRect.w and \
                self.sliderRect.y - self.circle_radius < mouse[1] < self.sliderRect.y + self.circle_radius:
            self.circle_x = mouse[0]


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


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


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


def pause():
    escape = True
    while escape:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    escape = False

        largeText = pygame.font.SysFont("mingliuextbpmingliuextbmingliuhkscsextb", 90)
        TextSurf, TextRect = text_objects("Pause", largeText, RED)
        TextRect.center = (int(WIDTH / 2), int(HEIGHT / 2))

        displaysurface.blit(TextSurf, TextRect)

        pygame.display.update()
        FramePerSec.tick(30)


slider = Slider(150, 500, 500, 10, "Music Volume")


def optionMenu(timer=1, stockCount=3):
    timer_display = None

    if timer == 1:
        timer_display = "1:00"
    elif timer == 2:
        timer_display = "2:00"
    elif timer == 3:
        timer_display = "3:00"
    elif timer == 4:
        timer_display = "4:00"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        displaysurface.fill(GRAY)

        largeText = pygame.font.SysFont("mingliuextbpmingliuextbmingliuhkscsextb", 30)
        TextSurf, TextRect = text_objects(("Stock Count: %d" % stockCount), largeText, BLUE)
        TextRect.center = ((WIDTH / 3 - 100), 55)

        Text2Surf, Text2Rect = text_objects(("Timer: %s" % timer_display), largeText, BLUE)
        Text2Rect.center = ((2 * WIDTH / 3 + 100), 55)

        stock_1 = button("1 Stock", WIDTH / 3 - 175, 105, 100, 50, WHITE, DARK_GRAY)
        stock_2 = button("2 Stock", WIDTH / 3 - 175, 155, 100, 50, WHITE, DARK_GRAY)
        stock_3 = button("3 Stock", WIDTH / 3 - 175, 205, 100, 50, WHITE, DARK_GRAY)
        stock_4 = button("4 Stock", WIDTH / 3 - 175, 255, 100, 50, WHITE, DARK_GRAY)

        if stock_1:
            stockCount = 1
        elif stock_2:
            stockCount = 2
        elif stock_3:
            stockCount = 3
        elif stock_4:
            stockCount = 4

        timer_1 = button("1 Minute", (2 * WIDTH / 3) + 50, 105, 100, 52, WHITE, DARK_GRAY)
        timer_2 = button("2 Minutes", (2 * WIDTH / 3) + 50, 157, 100, 52, WHITE, DARK_GRAY)
        timer_3 = button("3 Minutes", (2 * WIDTH / 3) + 50, 209, 100, 52, WHITE, DARK_GRAY)
        timer_4 = button("4 Minutes", (2 * WIDTH / 3) + 50, 261, 100, 52, WHITE, DARK_GRAY)

        if timer_1:
            timer = 1
            timer_display = "1:00"
        elif timer_2:
            timer = 2
            timer_display = "2:00"
        elif timer_3:
            timer = 3
            timer_display = "3:00"
        elif timer_4:
            timer = 4
            timer_display = "4:00"

        slider.draw(displaysurface)
        slider.volume_update()
        slider.move()

        back_button = button("Back", 0, 0, 50, 50, (0, 255, 255), GREEN)

        if back_button:
            time.sleep(0.5)
            return stockCount, timer, slider.volume

        displaysurface.blit(TextSurf, TextRect)
        displaysurface.blit(Text2Surf, Text2Rect)

        pygame.display.update()
        FramePerSec.tick(30)


def main(attack_angle_1, attack_angle_2, P1, P2, P1Char, P2Char, player1Left, player1Right,
         player1Up, player1Down, player1Shield, player1Attack, player1Strong, player1Special, player2Left, player2Right,
         player2Up, player2Down, player2Shield, player2Attack, player2Strong, player2Special, song, song_volume):
    playMusic(song, volume=song_volume)

    Stage_image.update(pygame.image.load('../PlatformFighter/Stages/Training2.png'), (WIDTH / 2, HEIGHT / 2))

    pygame.event.set_allowed([QUIT, KEYDOWN])

    counter = 0

    while not (P1.end or P2.end):
        counter += 1

        pressed_keys = pygame.key.get_pressed()
        player_1_buffer = ""
        if pressed_keys[player1Left]:
            player_1_buffer += "Left"
        if pressed_keys[player1Right]:
            player_1_buffer += "Right"
        if pressed_keys[player1Up]:
            player_1_buffer += "Up"
        if pressed_keys[player1Down]:
            player_1_buffer += "Down"
        if not (pressed_keys[player1Left] or pressed_keys[player1Right] or pressed_keys[player1Up] or pressed_keys[
            player1Down]):
            player_1_buffer += "None"

        pressed_keys = pygame.key.get_pressed()
        player_2_buffer = ""
        if pressed_keys[player2Left]:
            player_2_buffer += "Left"
        if pressed_keys[player2Right]:
            player_2_buffer += "Right"
        if pressed_keys[player2Up]:
            player_2_buffer += "Up"
        if pressed_keys[player2Down]:
            player_2_buffer += "Down"
        if not (pressed_keys[player2Left] or pressed_keys[player2Right] or pressed_keys[player2Up] or pressed_keys[
            player2Down]):
            player_2_buffer += "None"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == player1Up:
                    P1.jump()
                    P1.try_jump = True
                else:
                    P1.try_jump = False
                if event.key == player2Up:
                    P2.jump()
                    P2.try_jump = True
                else:
                    P2.try_jump = False

                if event.key == player1Attack:
                    player_1_buffer += "Attack "
                if event.key == player2Attack:
                    player_2_buffer += "Attack "
                if event.key == player1Strong:
                    player_1_buffer += "Strong "
                if event.key == player2Strong:
                    player_2_buffer += "Strong "
                if event.key == player1Special:
                    player_1_buffer += "Special "
                if event.key == player2Special:
                    player_2_buffer += "Special "
                if event.key == K_ESCAPE:
                    pause()

        player_1_buffer += " %d" % counter
        if player_1_buffer != (" %d" % counter):
            if "Attack" in player_1_buffer and "Strong" in player_1_buffer:
                P1.frame_inputs = ["Super", None, counter]
            elif "Special" in player_1_buffer:
                if "Left" in player_1_buffer:
                    P1.frame_inputs = ["Special", "Left", counter]
                elif "Right" in player_1_buffer:
                    P1.frame_inputs = ["Special", "Right", counter]
                elif "Up" in player_1_buffer:
                    P1.frame_inputs = ["Special", "Up", counter]
                elif "Down" in player_1_buffer:
                    P1.frame_inputs = ["Special", "Down", counter]
                elif "None" in player_1_buffer:
                    P1.frame_inputs = ["Special", None, counter]
            elif "Attack" in player_1_buffer:
                if "Left" in player_1_buffer:
                    P1.frame_inputs = ["Attack", "Left", counter]
                elif "Right" in player_1_buffer:
                    P1.frame_inputs = ["Attack", "Right", counter]
                elif "Up" in player_1_buffer:
                    P1.frame_inputs = ["Attack", "Up", counter]
                elif "Down" in player_1_buffer:
                    P1.frame_inputs = ["Attack", "Down", counter]
                elif "None" in player_1_buffer:
                    P1.frame_inputs = ["Attack", None, counter]
            elif "Strong" in player_1_buffer:
                if "Left" in player_1_buffer:
                    P1.frame_inputs = ["Strong", "Left", counter]
                elif "Right" in player_1_buffer:
                    P1.frame_inputs = ["Strong", "Right", counter]
                elif "Up" in player_1_buffer:
                    P1.frame_inputs = ["Strong", "Up", counter]
                elif "Down" in player_1_buffer:
                    P1.frame_inputs = ["Strong", "Down", counter]
                elif "None" in player_1_buffer:
                    P1.frame_inputs = ["Strong", None, counter]
            else:
                P1.frame_inputs = [None, None, counter]

        player_2_buffer += " %d" % counter
        if player_2_buffer != (" %d" % counter):
            if "Attack" in player_2_buffer and "Strong" in player_2_buffer:
                P2.frame_inputs = ["Super", None, counter]
            elif "Special" in player_2_buffer:
                if "Left" in player_2_buffer:
                    P2.frame_inputs = ["Special", "Left", counter]
                elif "Right" in player_2_buffer:
                    P2.frame_inputs = ["Special", "Right", counter]
                elif "Up" in player_2_buffer:
                    P2.frame_inputs = ["Special", "Up", counter]
                elif "Down" in player_2_buffer:
                    P2.frame_inputs = ["Special", "Down", counter]
                elif "None" in player_2_buffer:
                    P2.frame_inputs = ["Special", None, counter]
            elif "Attack" in player_2_buffer:
                if "Left" in player_2_buffer:
                    P2.frame_inputs = ["Attack", "Left", counter]
                elif "Right" in player_2_buffer:
                    P2.frame_inputs = ["Attack", "Right", counter]
                elif "Up" in player_2_buffer:
                    P2.frame_inputs = ["Attack", "Up", counter]
                elif "Down" in player_2_buffer:
                    P2.frame_inputs = ["Attack", "Down", counter]
                elif "None" in player_2_buffer:
                    P2.frame_inputs = ["Attack", None, counter]
            elif "Strong" in player_2_buffer:
                if "Left" in player_2_buffer:
                    P2.frame_inputs = ["Strong", "Left", counter]
                elif "Right" in player_2_buffer:
                    P2.frame_inputs = ["Strong", "Right", counter]
                elif "Up" in player_2_buffer:
                    P2.frame_inputs = ["Strong", "Up", counter]
                elif "Down" in player_2_buffer:
                    P2.frame_inputs = ["Strong", "Down", counter]
                elif "None" in player_2_buffer:
                    P2.frame_inputs = ["Strong", None, counter]
            else:
                P2.frame_inputs = [None, None, counter]

        P1jumps = P1.get_Jumps()
        P2jumps = P2.get_Jumps()

        P1shield_dir = P1.shielding(player1Shield, player1Left, player1Right)
        P2shield_dir = P2.shielding(player2Shield, player2Left, player2Right)

        P1.move(player1Left, player1Right, player1Down)
        attack_angle_1 = P1.get_angle(attack_angle_1)

        P1.attack(player1Attack, player1Left, player1Right, player1Up, player1Down)
        P1.strong_attacks(player1Strong, player1Up, player1Down)
        P1.special_attack(player1Special, player1Left, player1Right, player1Up, player1Down)

        P1.update(P1, attack_angle_2, tops, sides_left, sides_right, plats, under_plats, P2jumps, P2shield_dir,
                  shield_2, player1Shield, player1Strong, player1Attack, player1Special, player1Left, player1Right,
                  player1Up, player1Down)

        P1box.update((P1.hitbox_length, P1.hitbox_height), (P1.hitbox_pos_x, P1.hitbox_pos_y))
        P1box2.update((P1.hitbox_length2, P1.hitbox_height2), (P1.hitbox_pos_x2, P1.hitbox_pos_y2))
        P1projBox.update((P1.hitbox_lengthProj, P1.hitbox_heightProj), (P1.hitbox_pos_xProj, P1.hitbox_pos_yProj))

        P1Dis.update((P1.hitbox_length, P1.hitbox_height), (P1.hitbox_pos_x, P1.hitbox_pos_y), P1.attack_colour)
        P1Dis2.update((P1.hitbox_length2, P1.hitbox_height2), (P1.hitbox_pos_x2, P1.hitbox_pos_y2), P1.attack_colour)
        P1DisProj.update((P1.hitbox_lengthProj, P1.hitbox_heightProj), (P1.hitbox_pos_xProj, P1.hitbox_pos_yProj),
                         P1.attack_colour)

        P1.getHit(P1, player2box_1, P1shield, player2box_2, player2box_projectile, P2.induce_shieldstun)
        P1.hit_opponent(P2, P2shield, player1box_1, player1box_2, P2.invincibility_frames, player1box_projectile)

        P1percent.update(P1.percentage)

        P1shield.update((P1.shield_length, P1.shield_height), (P1.shield_pos_x, P1.shield_pos_y))
        P1.roll(player1Left, player1Right, player1Down)
        P1.airdodge(player1Left, player1Right, player1Up, player1Down, player1Shield)

        P1hurt.update(P1.image, (P1.hurt_pos_x, P1.hurt_pos_y))
        P1proj.update(P1.proj_image, (P1.proj_pos_x, P1.proj_pos_y))

        if P1.proj_image is None:
            all_sprites.remove(P1proj)
        else:
            all_sprites.add(P1proj)

        P2.move(player2Left, player2Right, player2Down)
        attack_angle_2 = P2.get_angle(attack_angle_2)

        P2.attack(player2Attack, player2Left, player2Right, player2Up, player2Down)
        P2.strong_attacks(player2Strong, player2Up, player2Down)
        P2.special_attack(player2Special, player2Left, player2Right, player2Up, player2Down)

        P2.update(P2, attack_angle_1, tops, sides_left, sides_right, plats, under_plats, P1jumps, P1shield_dir,
                  shield_1, player2Shield, player2Strong, player2Attack, player2Special, player2Left, player2Right,
                  player2Up, player2Down)

        P2box.update((P2.hitbox_length, P2.hitbox_height), (P2.hitbox_pos_x, P2.hitbox_pos_y))
        P2box2.update((P2.hitbox_length2, P2.hitbox_height2), (P2.hitbox_pos_x2, P2.hitbox_pos_y2))
        P2projBox.update((P2.hitbox_lengthProj, P2.hitbox_heightProj), (P2.hitbox_pos_xProj, P2.hitbox_pos_yProj))

        P2Dis.update((P2.hitbox_length, P2.hitbox_height), (P2.hitbox_pos_x, P2.hitbox_pos_y), P2.attack_colour)
        P2Dis2.update((P2.hitbox_length2, P2.hitbox_height2), (P2.hitbox_pos_x2, P2.hitbox_pos_y2), P2.attack_colour)
        P2DisProj.update((P2.hitbox_lengthProj, P2.hitbox_heightProj), (P2.hitbox_pos_xProj, P2.hitbox_pos_yProj),
                         P2.attack_colour)

        P2.getHit(P2, player1box_1, P2shield, player1box_2, player1box_projectile, P1.induce_shieldstun)
        P2.hit_opponent(P1, P1shield, player2box_1, player2box_2, P1.invincibility_frames, player2box_projectile)

        P2percent.update(P2.percentage)

        P2shield.update((P2.shield_length, P2.shield_height), (P2.shield_pos_x, P2.shield_pos_y))
        P2.roll(player2Left, player2Right, player2Down)
        P2.airdodge(player2Left, player2Right, player2Up, player2Down, player2Shield)

        P2hurt.update(P2.image, (P2.hurt_pos_x, P2.hurt_pos_y))
        P2proj.update(P2.proj_image, (P2.proj_pos_x, P2.proj_pos_y))

        if P2.proj_image is None:
            all_sprites.remove(P2proj)
        else:
            all_sprites.add(P2proj)

        time_out = Gametime.update()
        if time_out:
            break

        displaysurface.blit(Stage_image.surf.convert(), Stage_image.rect)

        P1Flash.update(pygame.image.load("../PlatformFighter/Stickman Character/Flash/flash_image.png"), (670, 575))
        if P1.flash_percent < 100:
            pygame.draw.rect(displaysurface, BLUE, (625, 565, 0.875 * P1.flash_percent, 20))
        else:
            pygame.draw.rect(displaysurface, (255, 255, 0), (625, 565, 0.875 * P1.flash_percent, 20))

        P2Flash.update(pygame.image.load("../PlatformFighter/Stickman Character/Flash/flash_image.png"), (120, 575))
        if P2.flash_percent < 100:
            pygame.draw.rect(displaysurface, BLUE, (75, 565, 0.875 * P2.flash_percent, 20))
        else:
            pygame.draw.rect(displaysurface, (255, 255, 0), (75, 565, 0.875 * P2.flash_percent, 20))

        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
        for entity in texts:
            displaysurface.blit(entity.textSurf, entity.textRect)

        if P1Char == "Stickman":
            stockGraphicStick(P1.stocks, 1,
                              "../PlatformFighter/Stickman Character/stick_stock_graphic.png")

        if P2Char == "Stickman":
            stockGraphicStick(P2.stocks, 2,
                              "../PlatformFighter/Stickman Character/stick_stock_graphic.png")

        displaysurface.blit(Gametime.textSurf, Gametime.textRect)

        smallText = pygame.font.SysFont("mingliuextbpmingliuextbmingliuhkscsextb", 20)
        textSurf, textRect = text_objects("%.2f" % FramePerSec.get_fps(), smallText, BLACK)
        textRect.center = (700, 150)
        displaysurface.blit(textSurf, textRect)

        pygame.display.update()
        FramePerSec.tick(FPS)



player1ControlList = [K_LEFT, K_RIGHT, K_UP, K_DOWN, K_k, K_j, K_l, K_h]
player2ControlList = [K_a, K_d, K_w, K_s, K_e, K_f, K_r, K_q]
stockCount = 3
GameTimer = 1
music_volume = 0.3

Start_Screen.startScreen()

while True:

    playMusic("../PlatformFighter/MUSIC/MenuViber.wav", volume=(music_volume / 6))

    charLoop = True
    next_action = []
    # arteens
    while charLoop:

        next_action = Character_Select.charSelect()
        hitbox_on_off = next_action[1]
        code_check = next_action[2]

        if next_action == "Controls":
            player1ControlList, player2ControlList = Controls.controlMenu(player1ControlList, player2ControlList)
        elif next_action == "Options":
            stockCount, GameTimer, music_volume = optionMenu(GameTimer, stockCount)
            pygame.mixer.music.set_volume((music_volume / 6))
        else:
            charLoop = False

    if next_action[0][0] == "Stickman":
        P1 = PlayerStickman.PlayerStickman(BLUE, 1, hitbox_on_off, stockCount, code_check)
        P1Char = "Stickman"
    else:
        raise ReferenceError("Player 1 Character Choice Not Found")
    if next_action[0][1] == "Stickman":
        P2 = PlayerStickman.PlayerStickman(RED, 2, hitbox_on_off, stockCount, code_check)
        P2Char = "Stickman"
    else:
        raise ReferenceError("Player 2 Character Choice Not Found")

    #  INITIALIZATION
    # PT1 = Stage(((WIDTH / 2), 310), (0, 191, 255), ((WIDTH / 2), (HEIGHT - 10)))
    Stage_image = imageBox((0, 0), (0, 0))
    PT2 = StageTop(5, int(WIDTH / 2), int(WIDTH / 2), int(HEIGHT - 165))
    PT3 = StageSide(575, 50)
    PT4 = StageSide(225, 50)
    PT5 = StageTop(6, 100, 525, HEIGHT - 229)
    PT6 = StageTop(6, 100, 275, HEIGHT - 229)
    PT7 = StageTop(1, 100, 525, HEIGHT - 227)
    PT8 = StageTop(1, 100, 275, HEIGHT - 227)
    P1hurt = imageBox((0, 0), (0, 0))
    P2hurt = imageBox((0, 0), (0, 0))
    P1proj = imageBox((0, 0), (0, 0))
    P2proj = imageBox((0, 0), (0, 0))
    P1box = Hitbox((0, 0), (0, 0))
    P2box = Hitbox((0, 0), (0, 0))
    P1box2 = Hitbox((0, 0), (0, 0))
    P2box2 = Hitbox((0, 0), (0, 0))
    P1projBox = Hitbox((0, 0), (0, 0))
    P2projBox = Hitbox((0, 0), (0, 0))
    P1Dis = emptyBox((0, 0), (0, 0))
    P2Dis = emptyBox((0, 0), (0, 0))
    P1Dis2 = emptyBox((0, 0), (0, 0))
    P2Dis2 = emptyBox((0, 0), (0, 0))
    P1DisProj = emptyBox((0, 0), (0, 0))
    P2DisProj = emptyBox((0, 0), (0, 0))
    P1shield = Shield((0, 0), (0, 0), BLUE)
    P1shield2 = Shield((0, 0), (0, 0), BLUE)
    P1shield3 = Shield((0, 0), (0, 0), BLUE)
    P2shield = Shield((0, 0), (0, 0), RED)
    P2shield2 = Shield((0, 0), (0, 0), RED)
    P2shield3 = Shield((0, 0), (0, 0), RED)
    P1percent = Percent(fonts, 1)
    P2percent = Percent(fonts, 2)
    P1Flash = imageBox((0, 0), (0, 0))
    P2Flash = imageBox((0, 0), (0, 0))

    Gametime = timerClass(GameTimer, fonts)

    # All Sprites group
    all_sprites = pygame.sprite.Group()
    # all_sprites.add(Stage_image)
    all_sprites.add(P1shield)
    all_sprites.add(P1shield2)
    all_sprites.add(P1shield3)
    all_sprites.add(P2shield)
    all_sprites.add(P2shield2)
    all_sprites.add(P2shield3)
    all_sprites.add(P1hurt)
    all_sprites.add(P2hurt)
    all_sprites.add(P1proj)
    all_sprites.add(P2proj)
    # all_sprites.add(P1box)
    # all_sprites.add(P1box2)
    if hitbox_on_off:
        all_sprites.add(P1)  # HURTBOX DISPLAY
        all_sprites.add(P2)  # HURTBOX DISPLAY
        all_sprites.add(P1Dis)  # HITBOX DISPLAY
        all_sprites.add(P1Dis2)  # HITBOX DISPLAY
        all_sprites.add(P1DisProj)  # HITBOX DISPLAY
        all_sprites.add(P2Dis)  # HITBOX DISPLAY
        all_sprites.add(P2Dis2)  # HITBOX DISPLAY
        all_sprites.add(P2DisProj)  # HITBOX DISPLAY
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
    all_sprites.add(P1Flash)
    all_sprites.add(P2Flash)

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

    # Player 1 (Projectile) Group
    player1box_projectile = pygame.sprite.Group()
    player1box_projectile.add(P1projBox)

    # Player 2 (Projectile) Group
    player2box_projectile = pygame.sprite.Group()
    player2box_projectile.add(P2projBox)

    # Player 1 Shield group
    shield_1 = pygame.sprite.Group()
    shield_1.add(P1shield)
    shield_1.add(P1shield2)
    shield_1.add(P1shield3)

    # Player 2 Shield group
    shield_2 = pygame.sprite.Group()
    shield_2.add(P2shield)
    shield_2.add(P2shield2)
    shield_2.add(P2shield3)

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

    main(attack_angle_1, attack_angle_2, P1, P2, P1Char, P2Char,
         player1Left=player1ControlList[0], player1Right=player1ControlList[1], player1Up=player1ControlList[2],
         player1Down=player1ControlList[3], player1Shield=player1ControlList[4], player1Attack=player1ControlList[5],
         player1Strong=player1ControlList[6], player1Special=player1ControlList[7],
         player2Left=player2ControlList[0], player2Right=player2ControlList[1], player2Up=player2ControlList[2],
         player2Down=player2ControlList[3], player2Shield=player2ControlList[4], player2Attack=player2ControlList[5],
         player2Strong=player2ControlList[6], player2Special=player2ControlList[7],
         song=songList[random.randint(0, len(songList)-1)], song_volume=music_volume)
    time.sleep(2)
