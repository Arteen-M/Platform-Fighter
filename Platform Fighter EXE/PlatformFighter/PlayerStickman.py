import pygame
from pygame.locals import *

import math
import time
import sys

vec = pygame.math.Vector2
pygame.mixer.init()

HEIGHT = 600  # STAGE HEIGHT
WIDTH = 800  # STAGE WIDTH
ACC = 0.5  # ACCELERATION (REMOVE MAYBE?)
GROUND_FRIC = -0.12  # TRACTION
AIR_FRIC = -0.12  # AIR DECELERATION


def playSFX(song, volume=0.3):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(volume)


class PlayerStickman(pygame.sprite.Sprite):
    def __init__(self, colour, numPlayer, show_hitbox=False, stockNum=3, arteen_cheat=False):
        super().__init__()
        self.colour = colour  # HURTBOX COLOUR (TESTING ONLY)
        # FIRST INSTANCE OF PLAYER IMAGE
        self.surf = pygame.image.load("Stickman Character/Walk cycle/stick_char_run_60fps-1.png").convert_alpha()
        # SET PLAYER SPAWNPOINT (X)
        if numPlayer == 1:
            spawnpos = 500
        else:
            spawnpos = 300
        # SET PLAYER CENTER
        center = (spawnpos, HEIGHT - 160)
        self.rect = self.surf.get_rect(center=center)

        # SET PLAYER POSITION
        self.pos = vec(center)
        # SET PLAYER VELOCITY
        self.vel = vec(0, 0.17)
        # SET PLAYER ACCELERATION
        self.acc = vec(0, 0)
        self.gravity = 0.17
        self.fall_speed = 3.7  # Fall Speed
        self.fast_fall = 5.12  # 60% Increase
        self.groundACC = 0.6  # GROUNDED ACCELERATION
        self.airACC = 0.45  # AIR ACCELERATION
        self.jumpACC = -4.8  # JUMP ACCELERATION
        if arteen_cheat:
            self.gravity = 0.17 * 5 / 3
            self.fall_speed = 3.7 * 50 / 3
            self.fast_fall = 5.12 * 50 / 3
            self.groundACC = 0.6 * 50 / 3
            self.airACC = 0.45 * 50 / 3
            self.jumpACC = -4.8 * 7 / 3

        self.show_hitbox = show_hitbox

        self.sfxObj = pygame.mixer.Sound("../PlatformFighter/MUSIC/HitSfX.wav")
        self.sfxObj.set_volume(1)

        self.shieldSFX = pygame.mixer.Sound("../PlatformFighter/MUSIC/shield7.wav")
        self.shieldSFX.set_volume(1)

        # CURRENT ATTACK ATTRIBUTES
        self.current_attack_attributes = 0
        self.in_hitstop = 0
        self.hitstop_counter = 0

        self.shieldstun = 0
        self.induce_shieldstun = 0

        self.prev_vel_x = 0
        self.prev_vel_y = 0

        # SET PLAYER JUMPSQUAT
        self.jumpsquat_right = [
            pygame.image.load("../PlatformFighter/Stickman Character/Jump Squat Frames/stick_char_jump-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jump Squat Frames/stick_char_jump-2.png").convert_alpha(),
            pygame.transform.flip(pygame.image.load("../PlatformFighter/Stickman Character/Jump Squat Frames/stick_char_jump_reverse-3.png"), True, False).convert_alpha()]
        self.jumpsquat_left = [
            pygame.image.load("../PlatformFighter/Stickman Character/Jump Squat Frames/stick_char_jump_reverse-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jump Squat Frames/stick_char_jump_reverse-2.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jump Squat Frames/stick_char_jump_reverse-3.png").convert_alpha()]
        self.in_jumpsquat = 0

        self.hitstunLeft = pygame.image.load("../PlatformFighter/Stickman Character/Hitstun/stick_char_hitstun-1.png").convert_alpha()
        self.hitstunRight = pygame.image.load("../PlatformFighter/Stickman Character/Hitstun/stick_char_hitstun_clone-1.png").convert_alpha()

        # AERIAL DRIFT ANIMATION
        self.jump_left = pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-4.png").convert_alpha()
        self.jump_right = pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-18.png").convert_alpha()
        self.drift_cycle = 0

        # SET PLAYER IDLE CYCLE
        self.idle_cycle = [
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha()]
        self.in_idle_cycle = 0

        self.idle_cycle_left = []
        for x in range(len(self.idle_cycle)):
            self.idle_cycle_left.append(pygame.transform.flip(self.idle_cycle[x], True, False))

        self.in_idle_cycle_left = 0

        # SET PLAYER WALK CYCLE
        self.walk_cycle_right = [
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-11.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-11.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-11.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-11.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-18.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-18.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-18.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-18.png").convert_alpha()]
        self.in_walk_cycle_right = 0

        self.walk_cycle_left = []
        for x in range(len(self.walk_cycle_right)):
            self.walk_cycle_left.append(pygame.transform.flip(self.walk_cycle_right[x], True, False))
        self.in_walk_cycle_left = 0

        # SET PLAYER CROUCH CYCLE
        self.crouch_right = [
            pygame.image.load("../PlatformFighter/Stickman Character/Crouch/stick_char_crouch-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Crouch/stick_char_crouch-2.png").convert_alpha()]
        self.crouch_left = [
            pygame.image.load("../PlatformFighter/Stickman Character/Crouch/stick_char_crouch_clone-2.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Crouch/stick_char_crouch_clone-3.png").convert_alpha()]
        self.crouch_frames = 0

        # SETS PLAYER JAB CYCLE AND ATTRIBUTES
        self.jab_right = [
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-2.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-2.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-2.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-3.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-3.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-3.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-5.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-5.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-5.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-8.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-8.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-8.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-9.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-9.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-9.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-10.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-10.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Jab/stick_char_jab-10.png").convert_alpha()]

        self.jab_left = []
        for x in range(len(self.jab_right)):
            self.jab_left.append(pygame.transform.flip(self.jab_right[x], True, False))

        self.in_jab_right = 0
        self.in_jab_left = 0

        self.jab_1_x = 0.01
        self.jab_1_y = 1
        self.jab_1_dmg = 1
        self.jab_1_base = 0.5
        self.jab_1_scale = 0
        self.jab_1_hitstun = 7

        self.jab_2_x = math.sin(math.radians(70))
        self.jab_2_y = math.sin(math.radians(20))
        self.jab_2_dmg = 4
        self.jab_2_base = 1
        self.jab_2_scale = 0.15
        self.jab_2_hitstun = 6

        # SET PLAYER F-TILT CYCLE (RIGHT) + ATTRIBUTES
        self.f_tilt_right = [
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-2.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-2.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-3.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-3.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-5.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-5.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-8.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-8.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-9.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-9.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-10.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-10.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-11.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-11.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-12.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-12.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-13.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-13.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-14.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-14.png").convert_alpha()]
        self.in_f_tilt = 0

        # SET PLAYER F-TILT CYCLE (LEFT) + ATTRIBUTES

        self.f_tilt_left = []
        for x in range(len(self.f_tilt_right)):
            self.f_tilt_left.append(pygame.transform.flip(self.f_tilt_right[x], True, False))

        self.in_f_tilt_left = 0

        self.f_tilt_x = math.sin(math.radians(65))
        self.f_tilt_y = math.sin(math.radians(25))
        self.f_tilt_dmg = 12
        self.f_tilt_base = 1.05
        self.f_tilt_scale = 0.14
        self.f_tilt_hitstun = 7

        # SET PLAYER DOWN-TILT CYCLE + ATTRIBUTES
        self.down_tilt_right = [
            pygame.image.load("../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-2.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-2.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-3.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-3.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-5.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-5.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-6.png").convert_alpha()]
        self.in_down_tilt_right = 0

        self.down_tilt_left = []
        for x in range(len(self.down_tilt_right)):
            self.down_tilt_left.append(pygame.transform.flip(self.down_tilt_right[x], True, False))

        self.in_down_tilt_left = 0

        self.down_tilt_x = math.sin(math.radians(20))
        self.down_tilt_y = math.sin(math.radians(70))
        self.down_tilt_dmg = 3
        self.down_tilt_base = 3
        self.down_tilt_scale = 0.03
        self.down_tilt_hitstun = 7

        # SET PLAYER UP-TILT CYCLE
        self.up_tilt_right = [
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-2.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-2.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-3.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-3.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-5.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-5.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-8.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-8.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-9.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-9.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-10.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-10.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-11.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-11.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-12.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-12.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-13.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-13.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-14.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-14.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-15.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-15.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-16.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-16.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-17.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-17.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-18.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-18.png").convert_alpha()]

        self.up_tilt_left = []
        for x in range(len(self.up_tilt_right)):
            self.up_tilt_left.append(pygame.transform.flip(self.up_tilt_right[x], True, False))

        self.in_up_tilt = 0

        self.up_tilt1_x = math.sin(math.radians(45))
        self.up_tilt1_y = math.sin(math.radians(45))
        self.up_tilt1_dmg = 4
        self.up_tilt1_base = 4
        self.up_tilt1_scale = 0
        self.up_tilt1_hitstun = 5

        self.up_tilt2_x = 0
        self.up_tilt2_y = 1
        self.up_tilt2_dmg = 10
        self.up_tilt2_base = 0.5
        self.up_tilt2_scale = 0.1
        self.up_tilt2_hitstun = 5

        # SET PLAYER FORWARD AIR CYCLE
        self.f_air_right = [
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-1.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-2.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-3.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-4.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-5.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-6.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-7.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-8.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-9.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-10.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-11.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-12.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-13.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-14.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-15.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-16.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-17.png").convert_alpha(),
            pygame.image.load("../PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-18.png").convert_alpha()]

        self.f_air_left = []
        for x in range(len(self.f_air_right)):
            self.f_air_left.append(pygame.transform.flip(self.f_air_right[x], True, False))

        self.in_f_air_right = 0
        self.in_f_air_left = 0

        self.f_air_x = math.sin(math.radians(60))
        self.f_air_y = math.sin(math.radians(30))
        self.f_air_dmg = 9
        self.f_air_base = 2.5
        self.f_air_scale = 0.13
        self.f_air_hitstun = 6

        # SET PLAYER DOWN AIR CYCLE AND ATTRIBUTES
        self.down_air_right = [pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-1.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-1.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-2.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-2.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-3.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-3.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-4.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-4.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-5.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-5.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-6.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-6.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-7.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-7.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-8.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-8.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-9.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-9.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-10.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-10.png").convert_alpha()]

        self.down_air_left = []
        for x in range(len(self.down_air_right)):
            self.down_air_left.append(pygame.transform.flip(self.down_air_right[x], True, False))

        self.in_down_air = 0

        self.down_air_x = 0
        self.down_air_y = -1
        self.down_air_dmg = 15
        self.down_air_base = 3
        self.down_air_scale = 0.17
        self.down_air_hitstun = 5

        # SET PLAYER UP AIR CYCLE AND ATTRIBUTES
        self.up_air_right = [pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-1.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-1.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-2.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-2.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-3.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-3.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-4.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-4.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-5.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-5.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-6.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-6.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-7.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-7.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-8.png").convert_alpha(),
                             pygame.image.load("../PlatformFighter/Stickman Character/Up Air/stick_char_upair-8.png").convert_alpha()]

        self.up_air_left = []
        for x in range(len(self.up_air_right)):
            self.up_air_left.append(pygame.transform.flip(self.up_air_right[x], True, False))

        self.in_up_air_right = 0
        self.in_up_air_left = 0

        self.up_air_x = math.sin(math.radians(10))
        self.up_air_y = math.sin(math.radians(80))
        self.up_air_dmg = 8
        self.up_air_base = 0.7
        self.up_air_scale = 0.12
        self.up_air_hitstun = 6

        # SET PLAYER BACK AIR ATTRIBUTES
        self.back_air_left = [pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-1.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-1.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-2.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-2.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-3.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-3.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-4.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-4.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-5.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-5.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-6.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-6.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-7.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-7.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-8.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-8.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-9.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-9.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-10.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-10.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-11.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-11.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-12.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-12.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-13.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-13.png").convert_alpha()]

        self.back_air_right = []
        for x in range(len(self.back_air_left)):
            self.back_air_right.append(pygame.transform.flip(self.back_air_left[x], True, False))

        self.in_back_air_right = 0
        self.in_back_air_left = 0

        self.back_air_x = math.sin(math.radians(75))
        self.back_air_y = math.sin(math.radians(15))
        self.back_air_dmg = 10
        self.back_air_base = 1
        self.back_air_scale = 0.2
        self.back_air_hitstun = 6

        # NEUTRAL AIR SETUP AND ATTRIBUTES
        self.neutral_air = [pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_0.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_1.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_2.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_3.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_4.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_5.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_6.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_7.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_8.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_9.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_10.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_11.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_12.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_13.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_14.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_15.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_16.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_17.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_18.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_19.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_20.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_21.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_22.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_23.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_24.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_25.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_26.png").convert_alpha(),
                            pygame.image.load("../PlatformFighter/Stickman Character/Neutral Air/Nair_27.png").convert_alpha()]
        self.in_neutral_air_right = 0
        self.in_neutral_air_left = 0

        self.neutral_air_13_x = 0.001
        self.neutral_air_13_y = 3
        self.neutral_air_13_dmg = 2
        self.neutral_air_13_base = 0.5
        self.neutral_air_13_scale = 0
        self.neutral_air_13_hitstun = 9

        self.neutral_air_4_x = math.sin(math.radians(20))
        self.neutral_air_4_y = math.sin(math.radians(60))
        self.neutral_air_4_dmg = 7
        self.neutral_air_4_base = 0.3
        self.neutral_air_4_scale = 0.1
        self.neutral_air_4_hitstun = 4

        # FORWARD STRONG SETUP AND ATTRIBUTES
        self.f_strong_right = [pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-1.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-1.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-2.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-2.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-3.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-3.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-4.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-4.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-5.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-5.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-6.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-6.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-7.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-7.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-8.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-8.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-9.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-9.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-10.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-10.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-11.png").convert_alpha(),
                               pygame.image.load("../PlatformFighter/Stickman Character/Forward Strong/stick-f-smash-11.png").convert_alpha()]
        self.in_f_strong_right = 0

        self.f_strong_left = []
        for x in range(len(self.f_strong_right)):
            self.f_strong_left.append(pygame.transform.flip(self.f_strong_right[x], True, False))

        self.in_f_strong_left = 0

        self.f_strong_x = math.sin(math.radians(80))
        self.f_strong_y = math.sin(math.radians(10))
        self.f_strong_dmg = 19
        self.f_strong_base = 1.1
        self.f_strong_scale = 0.14
        self.f_strong_hitstun = 10
        self.charge_boost_fs = 0.01

        # UP STRONG SETUP AND ATTRIBUTES
        self.up_strong_right = [pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 0.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 1.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 2.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 3.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 4.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 5.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 6.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 7.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 8.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 9.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 10.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 11.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 12.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 13.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 14.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 15.png").convert_alpha(),
                                pygame.image.load("../PlatformFighter/Stickman Character/Up Strong/Up Strong 16.png").convert_alpha()]

        self.up_strong_left = []
        for x in range(len(self.up_strong_right)):
            self.up_strong_left.append(pygame.transform.flip(self.up_strong_right[x], True, False))

        self.in_up_strong_right = 0
        self.in_up_strong_left = 0

        self.up_strong_x = math.sin(math.radians(20))
        self.up_strong_y = math.sin(math.radians(60))
        self.up_strong_dmg = 15
        self.up_strong_base = 1.2
        self.up_strong_scale = 0.12
        self.up_strong_hitstun = 10
        self.charge_boost_us = 0.0017

        # DOWN STRONG SETUP AND ATTRIBUTES
        self.down_strong_right = [pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_1.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_1.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_2.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_2.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_3.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_3.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_4.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_4.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_5.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_5.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_6.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_6.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_7.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_7.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_8.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_8.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_9.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_9.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_10.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_10.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_11.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_11.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_12.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_12.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_13.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_13.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_14.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_14.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_15.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_15.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_16.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_16.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_17.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_17.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_18.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_18.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_19.png").convert_alpha(),
                                  pygame.image.load("../PlatformFighter/Stickman Character/Down Strong/Stickman_Down_Smash_19.png").convert_alpha()]

        self.down_strong_left = []
        for x in range(len(self.down_strong_right)):
            self.down_strong_left.append(pygame.transform.flip(self.down_strong_right[x], True, False))

        self.in_down_strong = 0

        self.down_strong_x = math.sin(math.radians(20))
        self.down_strong_y = math.sin(math.radians(60))
        self.down_strong_dmg = 15
        self.down_strong_base = 1.2
        self.down_strong_scale = 0.12
        self.down_strong_hitstun = 10
        self.charge_boost_ds = 0.0017

        # FLASH SETUP AND ATTRIBUTES
        self.flash_percent = 100

        self.flash_attack_right = [pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 0 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 0 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 1 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 1 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 2 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 2 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 3 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 3 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 4 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 4 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 5 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 5 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 6 Reverse.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Flash/Flash 6 Reverse.png").convert_alpha()]

        self.flash_attack_left = []
        for x in range(len(self.flash_attack_right)):
            self.flash_attack_left.append(pygame.transform.flip(self.flash_attack_right[x], True, False))

        self.in_flash = 0

        self.flash_x = math.sin(math.radians(45))
        self.flash_y = math.sin(math.radians(45))
        self.flash_dmg = 6
        self.flash_base = 6
        self.flash_scale = 0
        self.flash_hitstun = 6

        # NEUTRAL SPECIAL SETUP AND ATTRIBUTES

        self.neutral_special_right = [pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_0.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_0.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_1.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_1.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_2.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_2.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_3.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_3.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_4.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_4.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_5.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_5.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_6.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_6.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_7.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_7.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_8.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_8.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_9.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_9.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_10.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_10.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_11.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_11.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_12.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_12.png").convert_alpha(),
                                      # "../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_13.png",
                                      # "../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_13.png",
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha(),
                                      pygame.image.load("../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_14.png").convert_alpha()]

        self.neutral_special_left = []
        for x in range(len(self.neutral_special_right)):
            self.neutral_special_left.append(pygame.transform.flip(self.neutral_special_right[x], True, False))

        self.in_neutral_special_right = 0
        self.in_neutral_special_left = 0

        self.projectile_active = 0
        self.projectile_active_left = 0

        self.neutral_b_x = 1
        self.neutral_b_y = 0
        self.neutral_b_dmg = 9
        self.neutral_b_base = 4
        self.neutral_b_scale = 0.01
        self.neutral_b_hitstun = 5

        # SIDE SPECIAL SETUP AND ATTRIBUTES
        self.side_special_right = [pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_0.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_0.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_1.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_1.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_2.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_2.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_3.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_3.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_4.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_4.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_5.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_5.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_6.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_6.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_7.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_7.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_8.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_8.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_9.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_9.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_10.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_10.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_11.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_11.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_12.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_12.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_13.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_13.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_14.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_14.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_15.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_15.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_16.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_16.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_16.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_16.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_16.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_16.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_16.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_16.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_16.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_16.png").convert_alpha(),
                                   pygame.image.load("../PlatformFighter/Stickman Character/Side Special/Side_Special_16.png").convert_alpha()]

        self.side_special_left = []
        for x in range(len(self.side_special_right)):
            self.side_special_left.append(pygame.transform.flip(self.side_special_right[x], True, False))

        self.in_side_special_right = 0
        self.in_side_special_left = 0

        self.side_special_x = math.sin(math.radians(70))
        self.side_special_y = math.sin(math.radians(20))
        self.side_special_dmg = 7
        self.side_special_base = 5
        self.side_special_scale = 0.01
        self.side_special_hitstun = 7

        # UP SPECIAL SETUP AND ATTRIBUTES
        self.up_special_right = [pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_0.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_1.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_2.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_3.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_4.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_5.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_6.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_7.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_8.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_9.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_10.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_11.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_12.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_13.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_14.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_15.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_16.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_17.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_18.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_18.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_19.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_19.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_20.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_20.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_21.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_21.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_22.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_22.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_23.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_23.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_24.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_24.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_25.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_25.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_26.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_26.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_27.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_27.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_28.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_28.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_29.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_29.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_30.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_30.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_31.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_31.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_32.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_32.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha(),
                                 pygame.image.load("../PlatformFighter/Stickman Character/Up Special/Up_Special_33.png").convert_alpha()]

        self.up_special_left = []
        for x in range(len(self.up_special_right)):
            self.up_special_left.append(pygame.transform.flip(self.up_special_right[x], True, False))

        self.in_up_special_right = 0
        self.in_up_special_left = 0

        self.up_special_x1 = math.sin(math.radians(10))
        self.up_special_y1 = math.sin(math.radians(80))
        self.up_special_dmg1 = 14
        self.up_special_base1 = 1.2
        self.up_special_scale1 = 0.12
        self.up_special_hitstun1 = 14

        self.up_special_x2 = math.sin(math.radians(10))
        self.up_special_y2 = math.sin(math.radians(80))
        self.up_special_dmg2 = 6
        self.up_special_base2 = 2
        self.up_special_scale2 = 0.05
        self.up_special_hitstun2 = 14

        self.up_special_hit = False

        # DOWN SPECIAL SETUP AND ATTRIBUTES

        self.down_special_ground_right = [pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_0.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_1.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_2.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_3.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_4.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_5.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_6.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_7.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_8.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_9.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_10.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_11.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_12.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_13.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_14.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_15.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_16.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_17.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_18.png").convert_alpha(),
                                          pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_19.png").convert_alpha()]

        self.down_special_ground_left = []
        for x in range(len(self.down_special_ground_right)):
            self.down_special_ground_left.append(pygame.transform.flip(self.down_special_ground_right[x], True, False))

        self.down_special_air_right = [pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_0.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_1.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_2.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_3.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_4.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_5.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_6.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_7.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_8.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_9.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_10.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_11.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_12.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_13.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_14.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_15.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_16.png").convert_alpha(),
                                       pygame.image.load("../PlatformFighter/Stickman Character/Down Special/Down_Special_air_16.png").convert_alpha()]

        self.down_special_air_left = []
        for x in range(len(self.down_special_air_right)):
            self.down_special_air_left.append(pygame.transform.flip(self.down_special_air_right[x], True, False))

        self.in_down_special_right = 0
        self.in_down_special_air_right = 0

        self.in_down_special_left = 0
        self.in_down_special_air_left = 0

        self.down_special_ground_x = math.sin(math.radians(10))
        self.down_special_ground_y = math.sin(math.radians(80))
        self.down_special_ground_dmg = 7
        self.down_special_ground_base = 0.5
        self.down_special_ground_scale = 0.005
        self.down_special_ground_hitstun = 12

        self.down_special_air_x = math.sin(math.radians(15))
        self.down_special_air_y = math.sin(math.radians(75))
        self.down_special_air_dmg = 2
        self.down_special_air_base = 1
        self.down_special_air_scale = 0.005
        self.down_special_air_hitstun = 7

        # ROLL ACTIVATION AND ATTRIBUTES
        self.roll_left = [pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_0.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_0.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_1.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_1.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_2.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_2.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_3.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_3.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_4.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_4.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_5.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_5.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_6.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_6.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_7.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_7.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_8.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_8.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_9.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_9.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_10.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_10.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_11.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_11.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_12.png").convert_alpha(),
                          pygame.image.load("../PlatformFighter/Stickman Character/Roll/Roll_left_12.png").convert_alpha()]

        self.roll_right = []
        for x in range(len(self.roll_left)):
            self.roll_right.append(pygame.transform.flip(self.roll_left[x], True, False))

        self.roll_left_active = False
        self.roll_right_active = False

        self.roll_left_frames = 0
        self.roll_right_frames = 0

        # AIR DODGE ACTIVATION AND ATTRIBUTES
        self.airdodge_left = [pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_1.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_1.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_2.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_2.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_3.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_3.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_4.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_4.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_5.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_5.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_6.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_6.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_7.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_7.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_8.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_8.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_9.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_9.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_10.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_10.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_11.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_11.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_12.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_12.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_13.png").convert_alpha(),
                              pygame.image.load("../PlatformFighter/Stickman Character/Air Dodge/airdodge_left_13.png").convert_alpha()]

        self.airdodge_right = []
        for x in range(len(self.airdodge_left)):
            self.airdodge_right.append(pygame.transform.flip(self.airdodge_left[x], True, False))

        self.airdodge_left_frames = 0
        self.airdodge_right_frames = 0

        self.set_velocity = None

        self.num_rotations = 0
        self.num_lag = 0  # SETS LAG (TYPE: STARTUP/ENDLAG)
        self.special_lag = 0  # SETS LAG (TYPE: SPECIAL FALL)
        self.in_lag = False  # SETS LAG (TYPE: ALL)
        self.num_active = 0  # HITBOX FRAMES (JAB 1/2)
        self.num_active_b = 0  # HITBOX FRAMES (BACK AIR)
        self.num_active_n13 = 0  # HITBOX FRAMES (NAIR, 1-3)
        self.num_active_n4 = 0  # HITBOX FRAMES (NAIR, 4)
        self.jab_1 = False  # JAB 1 IDENTIFIER
        self.jab_2 = False  # JAB 2 IDENTIFIER
        self.num_active_f = 0  # HITBOX FRAMES (F-TILT LEFT and RIGHt) and (FAIR and BAIR)
        self.num_active_d = 0  # HITBOX FRAMES (DOWN-TILT)
        self.num_active_u = 0  # HITBOX FRAMES (UP-TILT, 1)
        self.num_active_u2 = 0  # HITBOX FRAMES (UP-TILT, 2)
        self.num_active_fs = 0  # HITBOX FRAMES (F-SMASH)
        self.num_active_us = 0  # HITBOX FRAMES (UP-SMASH)
        self.num_active_ds = 0  # HITBOX FRAMES (DOWN-SMASH)
        self.num_active_flash = 0  # HITBOX FRAMES (FLASH ATTACK)
        self.num_active_ss = 0  # HITBOX FRAMES (SIDE SPECIAL)
        self.num_active_ub1 = 0  # HITBOX FRAMES (UP SPECIAL/B, 1)
        self.num_active_ub2 = 0  # HITBOX FRAMES (UP SPECIAL/B, 2)
        self.num_active_dsg = 0  # HITBOX FRAMES (DOWN SPECIAL/B, GROUND)
        self.num_active_dsa = 0  # HITBOX FRAMES (DOWN SPECIAL/B, AIR)

        self.hit = None

        self.numPlayer = numPlayer  # DEFINES YOUR PLAYER NUMBER
        self.minHitstun = 0  # DEFINES THE MINIMUM HITSTUN INDUCED BY AN OPPONENT ATTACK
        self.numHitstun = 0  # SETS LAG (TYPE: HITSTUN)
        self.take_knockback = False  # SETS KNOCKBACK (TRUE OR FALSE)
        self.percentage = 0  # SETS PERCENTAGE
        self.opponent_damage = 0  # SETS OPPONENTS ATTACKS DAMAGE
        self.weight = 80  # SET WEIGHT VALUE
        self.base_knockback = 0  # SETS BASE KNOCKBACK OF ATTACKS
        self.knockback_scale = 0  # SETS KNOCKBACK SCALING OF ATTACKS
        self.knockback_frames = 0  # SETS TAKE KNOCKBACK FRAMES
        self.knockback_num_x = 0  # TAKE KNOCKBACK (VELOCITY AFTER HIT)
        self.knockback_num_y = 0  # TAKE KNOCKBACK (VELOCITY AFTER HIT)
        self.total_knockback = 0  # NUM KNOCKBACK FRAMES
        self.platform_hitstun = 0  # SETS LAG (TYPE: RESPAWN)
        self.in_special = False  # IF PERFORMING A SPECIAL
        self.current_action = None  # CURRENT ACTION BEING PERFORMED
        self.next_action = None  # NEXT PREDICTED ACTION PERFORMED
        if self.numPlayer == 1:  # SETS PLAYER DIRECTION (FACING WHICH WAY)
            self.direction = False  # False -> Left
        else:
            self.direction = True  # True -> Right
        # SETS HITBOX (1) SIZE AND POSITION
        self.hitbox_length = 0
        self.hitbox_height = 0
        self.hitbox_pos_x = 0
        self.hitbox_pos_y = 0

        # SETS HITBOX (2) SIZE AND POSITION
        self.hitbox_length2 = 0
        self.hitbox_height2 = 0
        self.hitbox_pos_x2 = 0
        self.hitbox_pos_y2 = 0

        # SETS HITBOX (Projectile) SIZE AND POSITION
        self.hitbox_lengthProj = 0
        self.hitbox_heightProj = 0
        self.hitbox_pos_xProj = 0
        self.hitbox_pos_yProj = 0

        # SETS SHIELD SIZE AND POSITION
        self.shield_length = 0
        self.shield_height = 0
        self.shield_pos_x = 0
        self.shield_pos_y = 0

        self.stocks = stockNum  # SETS NUMBER OF STOCKS
        self.end = False  # SETS END OF GAME
        self.take_momentum = False  # SETS MOMENTUM (ACTIONABLE KNOCKBACK)
        self.in_momentum = 0  # SETS IN MOMENTUM FRAMES (ACTIONABLE KNOCKBACK)
        self.attack_colour = self.colour  # SETS HITBOX COLOUR (FOR TESTING ONLY)
        self.jumps = 5  # SETS NUMBER OF JUMPS
        self.airdodge_capable = True  # CAN AIRDODGE
        self.opponent_jumps = 0  # SETS NUMBER OF OPPONENT JUMPS (FOR KNOCKBACK ONLY)
        self.is_shielding = False  # SETS SHIELDING VARIABLE
        self.invincibility_frames = 0  # SETS INVINCIBILITY FRAMES
        self.in_dash = 0  # SETS DASH FRAMES
        self.check_dash = False  # CHECK FOR A DASH INPUT (CANCELS)

        # SETS ON STAGE VARIABLES
        self.on_stage = False
        self.on_platform = False
        self.on_ground = False

        self.pressing_right = False  # IF PRESSING RIGHT KEY
        self.press_right_frames = 0  # SETS FRAMES AFTER RIGHT PRESS (FOR DASHING ONLY)
        self.pressing_left = False  # IF PRESSING LEFT KEY
        self.press_left_frames = 0  # SAME, BUT FOR LEFT
        self.press_down_frames = 0  # SAME, BUT FOR DOWN
        self.press_left_check_frames = 0  # CHECKS FOR DASH INPUTS, WITHOUT DASHING (CANCELS)
        self.press_right_check_frames = 0  # SAME
        self.going_down = False  # SETS FAST-FALLING (GOING THROUGH PLATFORMS)
        self.last_dash = None  # LAST DIRECTION DASHED
        self.dash_wait = 0  # TIME TO WAIT UNTIL NEXT DASH
        self.try_jump = None  # ATTEMPT TO JUMP (FOR CANCELS)

        self.hurt_pos_x = 0  # HURTBOX POSITION (X)
        self.hurt_pos_y = 0  # HURTBOX POSITION (Y)
        # SETS DEFAULT IMAGE
        self.image = pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha()
        self.proj_image = None
        # SETS IMAGE POSITION
        self.size = (30, 50)
        self.proj_size = (0, 0)
        self.proj_pos_x = 0
        self.proj_pos_y = 0

        self.hitbox_1 = False  # HITBOX (1) VARIABLE
        self.hitbox_2 = False  # HITBOX (2) VARIABLE

        self.frames_after_jump = 0

        self.counter = 0
        self.frame_inputs = [None, None, 0]
        self.in_buffer = [None, None, 0]
        self.next_frame_inputs = None

    # WHEN TO GO INTO IDLE CYCLE
    def idleCycle(self):
        if self.on_ground and not (self.pressing_left or self.pressing_right) and self.vel.y <= 0.17:
            if self.direction:
                if self.in_idle_cycle == 0:
                    self.in_idle_cycle = len(self.idle_cycle)
                else:
                    self.in_idle_cycle -= 1
                self.hurtbox_alteration(self.idle_cycle[(len(self.idle_cycle) - 1) - self.in_idle_cycle],
                                        (self.pos.x, self.pos.y - 50))
            else:
                if self.in_idle_cycle_left == 0:
                    self.in_idle_cycle_left = len(self.idle_cycle_left)
                else:
                    self.in_idle_cycle_left -= 1
                self.hurtbox_alteration(self.idle_cycle_left[(len(self.idle_cycle_left) - 1) - self.in_idle_cycle_left],
                                        (self.pos.x, self.pos.y - 50))
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))

    # WHAT TO DO AFTER RESPAWNING
    def respawn(self):
        self.stocks -= 1
        self.pos.x = 400
        self.pos.y = 200
        self.platform_hitstun = 100
        self.percentage = 0
        self.invincibility_frames = 220
        self.vel.x = 0
        self.vel.y = 0

        if self.flash_percent < 85:
            self.flash_percent += 15
        else:
            self.flash_percent = 100

    # CHANGING HITBOX SIZE/ POSITION
    def hitbox_alteration(self, numBox, l, h, x, y):
        if numBox == 1:
            self.hitbox_length = l
            self.hitbox_height = h
            self.hitbox_pos_x = x
            self.hitbox_pos_y = y
        elif numBox == 2:
            self.hitbox_length2 = l
            self.hitbox_height2 = h
            self.hitbox_pos_x2 = x
            self.hitbox_pos_y2 = y
        elif numBox == "Projectile":
            self.hitbox_lengthProj = l
            self.hitbox_heightProj = h
            self.hitbox_pos_xProj = x
            self.hitbox_pos_yProj = y

    # CHANGING HURTBOX IMAGE/ POSITION
    def hurtbox_alteration(self, img, center):
        self.image = img
        self.hurt_pos_x = center[0]
        self.hurt_pos_y = center[1]

    # ACTUAL HURTBOX SIZE/ POSITION CHANGES
    def hurtbox_size_alteration(self, size, center):
        self.size = size
        self.surf = pygame.Surface(self.size)
        if self.show_hitbox:
            self.surf.fill(self.colour)  # FOR TESTING ONLY, REMOVE LATER
            self.surf.set_alpha(100)
        self.rect = self.surf.get_rect(center=center)

    # CHANGE SHIELD SIZE/ POSITION
    def shield_size(self, l, h, x, y, l2, h2, x2, y2, y3):
        self.shield_length = l
        self.shield_height = h
        self.shield_pos_x = x
        self.shield_pos_y = y

    def find_hitstop(self, dmg, multiplyer):
        return math.floor(((dmg * 0.45) + 2) * multiplyer + 3)

    def hitstop_state(self):
        if self.in_hitstop > 0:

            self.vel.x = 0
            self.vel.y = 0

            self.in_hitstop -= 1

            if self.in_hitstop == 0:
                self.vel.x = self.prev_vel_x
                self.vel.y = self.prev_vel_y

    def knockback_formula(self, angle):
        velocity = angle * (((((self.percentage / 10) + (self.percentage * (self.opponent_damage / 2) / 20) * (
                (200 / (self.weight + 100)) * 1.4) + 18) * self.knockback_scale) + self.base_knockback))
        return velocity

    # GETTING HIT FUNCTION
    def call_hit(self, component_x, component_y, dmg):
        velocityX = self.knockback_formula(component_x)
        velocityY = self.knockback_formula(component_y)
        velocity = math.sqrt(velocityX ** 2 + velocityY ** 2)
        self.numHitstun = round(
            velocity / (2 * self.gravity) - (2 * velocity) + (0.1 * self.percentage)) + self.minHitstun + \
                          self.find_hitstop(dmg, 1)
        self.knockback_frames = self.numHitstun
        self.total_knockback = self.numHitstun

    # CALL WHEN TO RESPAWN
    def call_respawn(self):
        if self.pos.x > WIDTH + 100:
            self.respawn()
        elif self.pos.x < -100:
            self.respawn()
        elif self.pos.y < -100:
            self.respawn()
        elif self.pos.y > 700:
            self.respawn()

    # RETURN HOW MANY JUMPS YOU HAVE
    def get_Jumps(self):
        return self.jumps

    def CheckDash(self, left_key, right_key, press_frames, press_frames_2):
        pressed_keys = pygame.key.get_pressed()
        if self.pressing_right:
            neg = 1
        else:
            neg = -1

        if (pressed_keys[left_key] and 0 < press_frames <= 6) or (pressed_keys[right_key] and 0 < press_frames_2 <= 6):
            self.check_dash = True
            if not self.in_lag:
                if self.on_ground and not self.take_momentum:
                    if neg > 0:  # and self.dash_wait <= 0:
                        # self.dash_wait = 30
                        self.vel.x = 12
                        self.vel.y = 0
                    elif neg < 0:  # and self.dash_wait <= 0:
                        # self.dash_wait = 30
                        self.vel.x = -12
                        self.vel.y = 0
                else:
                    self.take_momentum = False
                    if neg > 0:
                        self.vel.x = 12
                        self.vel.y = 0
                        self.in_dash = 5
                    elif neg < 0:
                        self.vel.x = -12
                        self.vel.y = 0
                        self.in_dash = 5
        else:
            self.check_dash = False

        if press_frames > 0:
            press_frames -= 1

        if press_frames_2 > 0:
            press_frames_2 -= 1

        if pressed_keys[left_key]:
            press_frames = 7

        if pressed_keys[right_key]:
            press_frames_2 = 7

        return press_frames, press_frames_2

    # WHEN TO DASH/ WHAT HAPPENS
    def dash(self, press_frames):
        if self.pressing_right:
            neg = 1
        else:
            neg = -1

        if 0 < press_frames <= 6:
            if not self.in_lag:
                if self.on_ground and not self.take_momentum:
                    if neg > 0:  # and self.dash_wait <= 0:
                        # self.dash_wait = 30
                        self.vel.x = 12
                        self.vel.y = 0
                    elif neg < 0:  # and self.dash_wait <= 0:
                        # self.dash_wait = 30
                        self.vel.x = -12
                        self.vel.y = 0
                else:
                    self.take_momentum = False
                    if neg > 0:
                        self.vel.x = 12
                        self.vel.y = 0
                        self.in_dash = 5
                    elif neg < 0:
                        self.vel.x = -12
                        self.vel.y = 0
                        self.in_dash = 5

                press_frames = 7


        else:
            press_frames = 7

        return press_frames

    # WHEN YOU ARE IN ABSOLUTE LAG
    def inLag(self):
        if self.num_lag > 0 or self.numHitstun > 0 or self.platform_hitstun > 0 or self.in_jumpsquat > 0 or self.in_hitstop > 0 or self.special_lag > 0:
            self.in_lag = True
        else:
            self.in_lag = False

    # DI COMPONENT
    def momentumChange(self):
        if self.pressing_left or self.pressing_right:
            if self.numHitstun == 0 and self.take_momentum:
                self.in_momentum += (self.airACC / 4)
            else:
                self.in_momentum = 0

    # PUSHBACK ON SHIELD
    def shieldPush(self, shield_dir):
        # print(True)
        if shield_dir == "Right":
            self.vel.x += 0.5
        elif shield_dir == "Left":
            self.vel.x -= 0.5

    # WHEN YOU ARE ON THE GROUND (AVOID REDUNDANT CODE)
    def groundCheck(self):
        if self.on_stage or self.on_platform:
            self.on_ground = True
        else:
            self.on_ground = False

    # WHAT HAPPENS WHEN YOU ARE INVINCIBLE
    def invincibleState(self):
        if self.invincibility_frames > 0:
            self.invincibility_frames -= 1
            self.knockback_frames = 0
            self.numHitstun = 0
            self.take_momentum = False

    # HALO PLATFORM INVINCIBILITY (AKA PLATFORM HITSTUN FOR SOME REASON)
    def platformHitstun(self):
        if self.platform_hitstun > 0:
            self.image = pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha()
            self.platform_hitstun -= 1
            self.knockback_frames = 0
            self.numHitstun = 0
            self.take_momentum = False
            self.vel.y = 0
            self.vel.x = 0

    # HITSTUN COUNTDOWN
    def hitstunState(self):
        if self.numHitstun > 0:
            self.numHitstun -= 1

    # WHEN TO END THE GAME
    def determineEnd(self):
        if self.stocks == 0:
            self.end = True

    def lowerNumLag(self):
        if self.num_lag > 0:
            self.num_lag -= 1

    def lowerSpecialLag(self):
        if self.special_lag > 0:
            self.special_lag -= 1

    def lowerShieldStun(self):
        if self.shieldstun > 0:
            self.shieldstun -= 1

    def buffer_check(self):
        if self.in_lag and self.frame_inputs[0] is not None:  # and (self.counter <= self.frame_inputs[2] + 12)
            self.in_buffer = self.frame_inputs
            # print(self.in_buffer, self.counter-self.in_buffer[2], self.num_lag)
        elif self.counter - self.in_buffer[2] >= 12:
            self.in_buffer = [None, None, 0]

    def Current_Next_Action(self, press_left_key, press_right_key, press_up_key, press_down_key, attack_key):
        pressed_keys = pygame.key.get_pressed()
        if self.num_lag > 0:
            if pressed_keys[attack_key]:
                if pressed_keys[press_left_key] or pressed_keys[press_right_key]:
                    if self.on_ground:
                        self.next_action = "FTilt"
                    else:
                        if (pressed_keys[press_left_key] and not self.direction) or (
                                pressed_keys[press_right_key] and self.direction):
                            self.next_action = "FAir"
                        else:
                            self.next_action = "BAir"
                elif pressed_keys[press_up_key]:
                    if self.on_ground:
                        self.next_action = "UTilt"
                    else:
                        self.next_action = "UAir"
                elif pressed_keys[press_down_key]:
                    if self.on_ground:
                        self.next_action = "DTilt"
                    else:
                        self.next_action = "DAir"

                else:
                    if self.on_ground:
                        pass
                        # self.next_action = "Jab"
                    else:
                        self.next_action = "NAir"
            elif self.try_jump and self.on_ground:
                self.next_action = "Jump"
            elif pressed_keys[press_down_key] and self.going_down:
                self.next_action = "FastFall"
            elif self.check_dash:
                self.next_action = "Dash"

    def flash(self, shield_key, strong_key):

        pressed_keys = pygame.key.get_pressed()

        if self.flash_percent >= 100 and not self.on_ground and (
                pressed_keys[shield_key] or self.airdodge_left_frames > 0 or self.airdodge_right_frames > 0) and \
                pressed_keys[strong_key] and (
                self.num_lag <= 0 or self.airdodge_left_frames > 0 or self.airdodge_right_frames > 0):
            self.flash_percent = 0
            self.in_flash = len(self.flash_attack_right) - 1
            self.num_lag = len(self.flash_attack_right) + 24
            self.invincibility_frames = 10
            self.airdodge_left_frames = 0
            self.airdodge_right_frames = 0
            self.airdodge_capable = False

    def press_check(self, attack_key, shield_key, strong_key, special_key):
        pygame.event.set_allowed([QUIT, KEYDOWN])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == attack_key or event.key == shield_key or event.key == strong_key or event.key == special_key:
                    return True

    # MOVING/ MOVEMENT FUNCTION (PLACE ALL MOVEMENT RELATED THINGS HERE)
    def move(self, player_key_left, player_key_right, player_key_down):
        self.acc = vec(0, self.gravity)  # GRAVITY
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[player_key_left] and self.on_ground and self.platform_hitstun == 0 and not self.is_shielding \
                and self.num_lag <= 0 and self.crouch_frames == 0 and self.in_jumpsquat == 0 and self.in_hitstop <= 0 \
                and self.special_lag <= 0:
            # WHEN CAN YOU MOVE LEFT
            # self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))

            if self.on_ground:  # GROUNDED MOVEMENT

                # BEGIN THE WALK CYCLE
                if self.in_walk_cycle_left == 0:
                    self.in_walk_cycle_left = len(self.walk_cycle_left)

                # MAYBE INITIAL DASH HERE IN THE FUTURE?

                if self.in_walk_cycle_left > 0:
                    self.in_walk_cycle_left -= 1

                self.direction = False  # SET DIRECTION (LEFT)

                self.acc.x -= self.groundACC  # GROUNDED MOVEMENT

                self.pressing_left = True  # PRESSING LEFT IS ALWAYS TRUE HERE

        elif pressed_keys[
            player_key_left] and not self.on_ground and self.platform_hitstun == 0 and self.in_hitstop <= 0 and self.special_lag <= 0:  # AIRBORNE MOVEMENT

            self.acc.x -= self.airACC  # AIR MOVEMENT

            self.in_walk_cycle_left = 0  # ENDS WALK CYCLE

            self.pressing_left = True  # PRESSING LEFT IS ALWAYS TRUE HERE

        else:
            self.pressing_left = False  # IF YOU'RE NOT PRESSING LEFT
            self.in_walk_cycle_left = 0  # END WALK CYCLE (MAYBE START IDLE CYCLE? IDLE CYCLE DEPENDANT ON PRESS OR
            # ON ANIMATION)
            # LOWERS PRESS FRAMES
            if self.press_left_frames > 0:
                self.press_left_frames -= 1

        if pressed_keys[player_key_right] and self.on_ground and self.platform_hitstun == 0 and not self.is_shielding \
                and self.num_lag == 0 and self.crouch_frames == 0 and self.in_jumpsquat == 0 and self.in_hitstop <= 0 and self.special_lag <= 0:
            # WHEN YOU CAN MOVE RIGHT

            if self.on_ground:  # GROUNDED MOVEMENT

                # BEGIN WALK CYCLE
                if self.in_walk_cycle_right == 0:
                    self.in_walk_cycle_right = len(self.walk_cycle_right)

                # MAYBE INITIAL DASH HERE IN THE FUTURE?

                if self.in_walk_cycle_right > 0:
                    self.in_walk_cycle_right -= 1

                self.direction = True  # SET DIRECTION (RIGHT))

                self.acc.x += self.groundACC  # GROUNDED MOVEMENT

                self.pressing_right = True  # PRESSING RIGHT IS ALWAYS TRUE HERE

        elif pressed_keys[
            player_key_right] and not self.on_ground and self.platform_hitstun == 0 and self.in_hitstop <= 0 and self.special_lag <= 0:  # AIRBORNE MOVEMENT
            self.acc.x += self.airACC  # AIR MOVEMENT
            self.in_walk_cycle_right = 0  # ENDS WALK CYCLE WHEN AIRBORNE

            self.pressing_right = True  # PRESSING RIGHT IS ALWAYS TRUE HERE

        else:
            self.pressing_right = False  # IF YOU'RE NOT PRESSING LEFT
            self.in_walk_cycle_right = 0  # END WALK CYCLE
            # LOWERS PRESS FRAMES
            if self.press_right_frames > 0:
                self.press_right_frames -= 1

        if pressed_keys[
            player_key_down] and self.numHitstun == 0 and self.platform_hitstun == 0 and (
                self.num_lag == 0 or not self.on_ground) and self.in_jumpsquat == 0 and self.special_lag <= 0:
            # self.dash_wait = 0
            if self.on_ground and self.crouch_frames < 2:
                self.crouch_frames += 1

            if 0 < self.press_down_frames <= 6:  # FALLING THROUGH PLATFORMS
                self.going_down = True
                self.press_down_frames = 7
                self.vel.y = self.fast_fall  # FASTFALL SPEED
            else:
                self.press_down_frames = 7
        else:
            self.crouch_frames = 0
            if self.press_down_frames > 0:
                self.press_down_frames -= 1

        # MOVEMENT (VELOCITY, ACCELERATION AND POSITION)
        if self.on_ground:
            self.acc.x += self.vel.x * GROUND_FRIC
        else:
            self.acc.x += self.vel.x * AIR_FRIC
        self.vel.x += self.acc.x
        if self.vel.y <= self.fall_speed:
            self.vel.y += self.acc.y
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

    def jump(self):
        self.going_down = False
        self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))

        if not self.in_lag and self.crouch_frames == 0:  # CANNOT JUMP IN THESE TWO CASES
            self.take_momentum = False
            if self.on_ground and self.frames_after_jump == 0:
                self.in_jumpsquat = len(self.jumpsquat_left)  # START JUMPSQUAT
                self.frames_after_jump = len(self.jumpsquat_left) + 3
            elif self.jumps > 0:  # OTHERWISE, FRAME 1 JUMP (CHANGE WHEN AERIAL JUMPS HAVE ANIMATIONS)
                self.vel.y = self.jumpACC  # -4.8
                self.jumps -= 1

    def update(self, player, attack_angle_p_1, tops_1, sides_left_1, sides_right_1, platforms, under_platforms, jumps,
               shield_dir, other_shield, shield_key, strong_key, attack_key, special_key, left_key, right_key, up_key,
               down_key):
        hitsGround = pygame.sprite.spritecollide(player, tops_1, False)
        hitsSideLeft = pygame.sprite.spritecollide(player, sides_left_1, False)
        hitsSideRight = pygame.sprite.spritecollide(player, sides_right_1, False)
        hitsPlatform = pygame.sprite.spritecollide(player, platforms, False)
        hitsUnderPlat = pygame.sprite.spritecollide(player, under_platforms, False)
        hitsShield = pygame.sprite.spritecollide(player, other_shield, False)

        self.counter += 1

        self.press_left_check_frames, self.press_right_check_frames = self.CheckDash(left_key, right_key,
                                                                                     self.press_left_check_frames,
                                                                                     self.press_right_check_frames)

        self.Current_Next_Action(left_key, right_key, up_key, down_key, attack_key)
        if self.numPlayer == 1:
            self.buffer_check()
        self.call_respawn()
        self.inLag()
        self.momentumChange()
        self.groundCheck()
        self.invincibleState()
        self.platformHitstun()
        self.hitstunState()
        self.determineEnd()
        self.lowerNumLag()
        self.lowerSpecialLag()
        self.hitstop_state()
        self.flash(shield_key, strong_key)
        self.lowerShieldStun()
        self.opponent_jumps = jumps

        if self.hit and not self.in_special and self.current_action != self.next_action:
            self.num_lag = 0
            self.current_action = self.next_action

            if self.current_action != "UTilt":
                self.in_up_tilt = 0
            if self.current_action != "Jab":
                self.in_jab_left = 0
                self.in_jab_right = 0
            if self.current_action != "NAir":
                self.in_neutral_air_right = 0
                self.in_neutral_air_left = 0

            if self.next_action == "Jump":
                self.jump()

            if self.next_action == "Dash" and self.flash_percent >= 25:
                self.flash_percent -= 25
                if self.press_right_check_frames > 0:
                    self.vel.x = 12
                    self.vel.y = 0
                elif self.press_left_check_frames > 0:
                    self.vel.x = -12
                    self.vel.y = 0
                self.next_action = None

            self.num_active = 0  # HITBOX FRAMES (JAB 1/2)
            self.num_active_b = 0  # HITBOX FRAMES (BACK AIR)
            self.num_active_n13 = 0  # HITBOX FRAMES (NAIR, 1-3)
            self.num_active_n4 = 0  # HITBOX FRAMES (NAIR, 4)
            self.num_active_f = 0  # HITBOX FRAMES (F-TILT LEFT and RIGHt) and (FAIR and BAIR)
            self.num_active_d = 0  # HITBOX FRAMES (DOWN-TILT)
            self.num_active_u = 0  # HITBOX FRAMES (UP-TILT, 1)
            self.num_active_u2 = 0  # HITBOX FRAMES (UP-TILT, 2)
            self.num_active_fs = 0  # HITBOX FRAMES (F-SMASH)
            self.num_active_us = 0  # HITBOX FRAMES (UP-SMASH)
            self.num_active_ds = 0  # HITBOX FRAMES (DOWN-SMASH)
            self.num_active_flash = 0  # HITBOX FRAMES (FLASH ATTACK)
            self.num_active_ss = 0  # HITBOX FRAMES (SIDE SPECIAL)
            self.num_active_ub1 = 0  # HITBOX FRAMES (UP SPECIAL/B, 1)
            self.num_active_ub2 = 0  # HITBOX FRAMES (UP SPECIAL/B, 2)
            self.num_active_dsg = 0  # HITBOX FRAMES (DOWN SPECIAL/B, GROUND)
            self.num_active_dsa = 0  # HITBOX FRAMES (DOWN SPECIAL/B, AIR)

        if self.in_neutral_special_left > 0 or self.in_neutral_special_right > 0 or self.in_side_special_left > 0 or self.in_side_special_right > 0 or self.in_up_special_left > 0 or self.in_up_special_right > 0 or self.in_down_special_right > 0 or self.in_down_special_air_right > 0 or self.in_down_special_left > 0 or self.in_down_special_air_left > 0:
            self.in_special = True
        else:
            self.in_special = False

        if self.on_ground:
            self.airdodge_capable = True

        if self.up_special_hit > 0:
            self.up_special_hit -= 1

        if self.in_dash > 0:
            self.vel.y = 0
            self.in_dash -= 1

        if self.dash_wait > 0:
            self.dash_wait -= 1

        if hitsGround:
            self.on_stage = True
            self.pos.y = hitsGround[0].rect.top + 1
            self.vel.y = 0
            self.take_momentum = False
            self.jumps = 10
            self.going_down = False
        else:
            self.on_stage = False

        if hitsSideLeft and not hitsGround:
            self.pos.x = hitsSideLeft[0].rect.left - 15
            self.vel.x = 0

        if hitsSideRight and not hitsGround:
            self.pos.x = hitsSideRight[0].rect.right + 15
            self.vel.x = 0

        if hitsPlatform and self.vel.y >= 0 and not self.going_down and not hitsUnderPlat and self.numHitstun <= 0:
            self.on_platform = True
            self.pos.y = hitsPlatform[0].rect.top + 1
            self.vel.y = 0
            self.jumps = 5
            self.take_momentum = False
            # self.knockback_frames = 0
        else:
            self.on_platform = False

        if hitsShield:
            self.shieldPush(shield_dir)

        if self.on_ground:
            self.last_dash = None

        # JUMPSQUAT ANIMATION PLAY
        if self.in_jumpsquat > 0:
            self.current_action = "Jump"
            self.in_jumpsquat -= 1

            if self.in_jumpsquat == 0:
                self.on_ground = False
                self.vel.y = self.jumpACC

        if self.frames_after_jump > 0:
            self.frames_after_jump -= 1

        # ATTACKING ANIMATIONS PLAY
        if self.in_f_tilt > 0 or self.in_f_tilt_left > 0:

            self.current_action = "FTilt"
            self.current_attack_attributes = self.f_tilt_dmg - 2

            if self.in_f_tilt > 0:  # ACTIVATE F-TILT RIGHT
                if self.in_hitstop <= 0:
                    self.in_f_tilt -= 1  # LOWER ANIMATION FRAMES

                if self.in_f_tilt == 13:  # HITBOX FLAG 1
                    self.num_active_f = 8  # TOTAL ACTIVE FRAMES

                if self.num_active_f > 0:  # IF ACTIVE
                    self.hitbox_alteration(1, 30, 15, (self.pos.x + 15), (self.pos.y - 30))  # HITBOX SIZE
                    self.num_active_f -= 1  # LOWER ACTIVE FRAMES
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)  # HITBOX 1 REMOVAL
                    self.hitbox_alteration(2, 0, 0, 0, 0)  # HITBOX 2 REMOVAL

                if not self.on_ground:
                    self.in_f_tilt = 0  # FOR EDGE CANCELING
                    self.num_active_f = 0
                    self.num_lag = 0

            elif self.in_f_tilt_left > 0:  # ACTIVATE F-TILT LEFT
                if self.in_hitstop <= 0:
                    self.in_f_tilt_left -= 1  # LOWER ANIMATION FRAMES

                if self.in_f_tilt_left == 13:  # HITBOX FLAG 1
                    self.num_active_f = 8  # TOTAL ACTIVE FRAMES

                if self.num_active_f > 0:  # IF ACTIVE
                    self.hitbox_alteration(1, 30, 15, (self.pos.x - 15), (self.pos.y - 30))  # HITBOX SIZE
                    self.num_active_f -= 1  # LOWER ACTIVE FRAMES
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)  # HITBOX 1 REMOVAL
                    self.hitbox_alteration(2, 0, 0, 0, 0)  # HITBOX 2 REMOVAL

                if not self.on_ground:
                    self.in_f_tilt_left = 0  # FOR EDGE CANCELING
                    self.in_f_tilt_left = 0
                    self.num_lag = 0

        elif self.in_up_tilt > 0:

            self.current_action = "UTilt"

            if self.in_hitstop <= 0:
                self.in_up_tilt -= 1  # LOWER ANIMATION FRAMES

            if self.in_up_tilt == 17:  # HITBOX FLAG 1
                self.num_active_u = 10  # TOTAL ACTIVE FRAMES (1)

                self.current_attack_attributes = self.up_tilt1_dmg

            if self.in_up_tilt == 25:  # HITBOX FLAG 2
                self.num_active_u2 = 4  # TOTAL ACTIVE FRAMES (2)

                self.current_attack_attributes = self.up_tilt2_dmg

            if self.num_active_u > 0:  # IF ACTIVE (1)
                self.hitbox_alteration(1, 15, 60, self.pos.x,
                                       (self.pos.y - 45) - (3 * (10 - self.num_active_u)))  # HITBOX SIZE (1)
                self.num_active_u -= 1  # LOWER ACTIVE FRAMES
            elif self.num_active_u2 > 0:  # IF ACTIVE (2)
                self.hitbox_alteration(1, 30, 30, self.pos.x + 25, (self.pos.y - 15))  # HITBOX (1) SIZE
                self.hitbox_alteration(2, 30, 30, self.pos.x - 25, (self.pos.y - 15))  # HITBOX (2) SIZE
                self.num_active_u2 -= 1  # LOWER ACTIVE FRAMES
            else:
                self.hitbox_alteration(1, 0, 0, 0, 0)  # HITBOX 1 REMOVAL
                self.hitbox_alteration(2, 0, 0, 0, 0)  # HITBOX 2 REMOVAL

            if not self.on_ground:
                self.in_up_tilt = 0  # FOR EDGE CANCELING
                self.num_active_u = 0
                self.num_active_u2 = 0
                self.num_lag = 0

        elif self.in_down_tilt_left > 0:

            self.current_action = "DTilt"

            self.current_attack_attributes = self.down_tilt_dmg

            if self.in_hitstop <= 0:
                self.in_down_tilt_left -= 1  # LOWER ANIMATION FRAMES

            if self.in_down_tilt_left == 3:  # HITBOX FLAG (1)
                self.num_active_d = 4  # TOTAL ACTIVE FRAMES

            if self.num_active_d > 0:  # IF ACTIVE
                self.hitbox_alteration(1, 30, 10, (self.pos.x - 15), self.pos.y - 10)  # HITBOX SIZE
                self.num_active_d -= 1  # LOWER ACTIVE
            else:
                self.hitbox_alteration(1, 0, 0, 0, 0)  # HITBOX 1 REMOVAL
                self.hitbox_alteration(2, 0, 0, 0, 0)  # HITBOX 2 REMOVAL

            if not self.on_ground:
                self.in_down_tilt_left = 0  # FOR EDGE CANCELING
                self.num_active_d = 0
                self.num_lag = 0

        elif self.in_down_tilt_right > 0:

            self.current_action = "DTilt"

            self.current_attack_attributes = self.down_tilt_dmg

            if self.in_hitstop <= 0:
                self.in_down_tilt_right -= 1

            if self.in_down_tilt_right == 3:
                self.num_active_d = 4

            if self.num_active_d > 0:
                self.hitbox_alteration(1, 30, 10, (self.pos.x + 15), self.pos.y - 10)
                self.num_active_d -= 1
            else:
                self.hitbox_alteration(1, 0, 0, 0, 0)  # HITBOX 1 REMOVAL
                self.hitbox_alteration(2, 0, 0, 0, 0)  # HITBOX 2 REMOVAL

            if not self.on_ground:
                self.in_down_tilt_right = 0
                self.num_active_d = 0
                self.num_lag = 0

        elif self.in_jab_right > 0 or self.in_jab_left > 0:

            if self.in_jab_right > 0:
                if self.in_hitstop <= 0:
                    self.in_jab_right -= 1

                if self.in_jab_right == 20:
                    self.num_active = 6
                    self.jab_1 = True

                    self.current_attack_attributes = self.jab_1_dmg

                elif self.in_jab_right == 9:
                    self.num_active = 6
                    self.jab_2 = True

                    self.current_attack_attributes = self.jab_2_dmg

                else:
                    self.jab_1 = False
                    self.jab_2 = False

                if not self.on_ground:
                    self.in_jab_right = 0
                    self.num_active = 0
                    self.num_lag = 0

                if self.num_active > 0:
                    if self.jab_1:
                        self.hitbox_alteration(1, 15, 10, (self.pos.x + 15), self.pos.y - 15)
                    elif self.jab_2:
                        self.hitbox_alteration(1, 25, 10, (self.pos.x + 15), self.pos.y - 20)
                    self.num_active -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

            elif self.in_jab_left > 0:
                if self.in_hitstop <= 0:
                    self.in_jab_left -= 1

                if self.in_jab_left == 20:
                    self.num_active = 6
                    self.jab_1 = True

                    self.current_attack_attributes = self.jab_1_dmg

                elif self.in_jab_left == 9:
                    self.num_active = 6
                    self.jab_2 = True

                    self.current_attack_attributes = self.jab_2_dmg

                else:
                    self.jab_1 = False
                    self.jab_2 = False

                if not self.on_ground:
                    self.in_jab_left = 0
                    self.num_active = 0
                    self.num_lag = 0

                if self.num_active > 0:
                    if self.jab_1:
                        self.hitbox_alteration(1, 15, 10, (self.pos.x - 15), self.pos.y - 15)
                    elif self.jab_2:
                        self.hitbox_alteration(1, 25, 10, (self.pos.x - 15), self.pos.y - 20)
                    self.num_active -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

        elif self.in_f_air_right > 0 or self.in_f_air_left > 0:

            self.current_action = "FAir"

            self.current_attack_attributes = self.f_air_dmg

            if self.in_f_air_right > 0:
                if self.in_hitstop <= 0:
                    self.in_f_air_right -= 1

                if self.in_f_air_right == 15:
                    self.num_active_f = 12

                if self.num_active_f > 0:
                    self.hitbox_alteration(1, 50, 30, self.pos.x + 30, self.pos.y - 50)
                    self.num_active_f -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if self.on_ground:
                    self.in_f_air_right = 0
                    self.num_active_f = 0
                    self.num_lag = 0

            elif self.in_f_air_left > 0:
                if self.in_hitstop <= 0:
                    self.in_f_air_left -= 1

                if self.in_f_air_left == 15:
                    self.num_active_f = 12

                if self.num_active_f > 0:
                    self.hitbox_alteration(1, 50, 30, self.pos.x - 30, self.pos.y - 50)
                    self.num_active_f -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if self.on_ground:
                    self.in_f_air_left = 0
                    self.num_active_f = 0
                    self.num_lag = 0

        elif self.in_down_air > 0:

            self.current_action = "DAir"

            self.current_attack_attributes = self.down_air_dmg

            if self.direction:
                if self.in_hitstop <= 0:
                    self.in_down_air -= 1

                if self.in_down_air == 9:
                    self.num_active_d = 6

                if self.num_active_d > 0:
                    self.hitbox_alteration(1, 30, 30, self.pos.x, self.pos.y - 15)
                    self.num_active_d -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if self.on_ground:
                    self.in_down_air = 0
                    self.num_active_d = 0
                    self.num_lag = 0
            else:
                if self.in_hitstop <= 0:
                    self.in_down_air -= 1

                if self.in_down_air == 9:
                    self.num_active_d = 6

                if self.num_active_d > 0:
                    self.hitbox_alteration(1, 30, 30, self.pos.x, self.pos.y - 15)
                    self.num_active_d -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if self.on_ground:
                    self.in_down_air = 0
                    self.num_active_d = 0
                    self.num_lag = 0

        elif self.in_up_air_right > 0 or self.in_up_air_left > 0:

            self.current_action = "UAir"

            self.current_attack_attributes = self.up_air_dmg

            if self.in_up_air_right > 0:
                if self.in_hitstop <= 0:
                    self.in_up_air_right -= 1

                if self.in_up_air_right == 10:
                    self.num_active_u = 6

                if self.num_active_u > 0:
                    self.hitbox_alteration(1, 40, 30, self.pos.x, self.pos.y - 40)
                    self.num_active_u -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if self.on_ground:
                    self.in_up_air_right = 0
                    self.num_active_u = 0
                    self.num_lag = 0

            if self.in_up_air_left > 0:
                if self.in_hitstop <= 0:
                    self.in_up_air_left -= 1

                if self.in_up_air_left == 10:
                    self.num_active_u = 6

                if self.num_active_u > 0:
                    self.hitbox_alteration(1, 30, 30, self.pos.x, self.pos.y - 40)
                    self.num_active_u -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if self.on_ground:
                    self.in_up_air_left = 0
                    self.num_active_u = 0
                    self.num_lag = 0

        elif self.in_back_air_right > 0 or self.in_back_air_left > 0:

            self.current_action = "BAir"

            self.current_attack_attributes = self.back_air_dmg

            if self.in_back_air_right > 0:
                if self.in_hitstop <= 0:
                    self.in_back_air_right -= 1

                if self.in_back_air_right == 9:
                    self.num_active_b = 4

                if self.num_active_b > 0:
                    self.hitbox_alteration(1, 30, 15, self.pos.x - 25, self.pos.y - 30)
                    self.num_active_b -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if self.on_ground:
                    self.in_back_air_right = 0
                    self.num_active_b = 0
                    self.num_lag = 0

            elif self.in_back_air_left > 0:
                if self.in_hitstop <= 0:
                    self.in_back_air_left -= 1

                if self.in_back_air_left == 9:
                    self.num_active_b = 4

                if self.num_active_b > 0:
                    self.hitbox_alteration(1, 30, 15, self.pos.x + 25, self.pos.y - 30)
                    self.num_active_b -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if self.on_ground:
                    self.in_back_air_left = 0
                    self.num_active_b = 0
                    self.num_lag = 0

        elif self.in_neutral_air_right > 0 or self.in_neutral_air_left > 0:

            self.current_action = "NAir"

            if self.in_neutral_air_right > 0:
                if self.in_hitstop <= 0:
                    self.in_neutral_air_right -= 1

                if self.in_neutral_air_right == 21 or self.in_neutral_air_right == 14 or self.in_neutral_air_right == 8:
                    self.num_active_n13 = 2

                    self.current_attack_attributes = self.neutral_air_13_dmg

                elif self.in_neutral_air_right == 2:
                    self.num_active_n4 = 2

                    self.current_attack_attributes = self.neutral_air_4_dmg

                if self.num_active_n13 > 0:
                    self.hitbox_alteration(1, 40, 50, self.pos.x, self.pos.y - 27)
                    self.num_active_n13 -= 1
                elif self.num_active_n4 > 0:
                    self.hitbox_alteration(1, 40, 50, self.pos.x, self.pos.y - 27)
                    self.num_active_n4 -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if self.on_ground:
                    self.in_neutral_air_right = 0
                    self.num_active_n13 = 0
                    self.num_active_n4 = 0
                    self.num_lag = 0

            elif self.in_neutral_air_left > 0:
                if self.in_hitstop <= 0:
                    self.in_neutral_air_left -= 1

                if self.in_neutral_air_left == 21 or self.in_neutral_air_left == 14 or self.in_neutral_air_left == 8:
                    self.num_active_n13 = 2

                    self.current_attack_attributes = self.neutral_air_13_dmg

                elif self.in_neutral_air_left == 2:
                    self.num_active_n4 = 2

                    self.current_attack_attributes = self.neutral_air_4_dmg

                if self.num_active_n13 > 0:
                    self.hitbox_alteration(1, 40, 50, self.pos.x, self.pos.y - 27)
                    self.num_active_n13 -= 1
                elif self.num_active_n4 > 0:
                    self.hitbox_alteration(1, 40, 50, self.pos.x, self.pos.y - 27)
                    self.num_active_n4 -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if self.on_ground:
                    self.in_neutral_air_left = 0
                    self.num_active_n13 = 0
                    self.num_active_n4 = 0
                    self.num_lag = 0

        elif self.in_up_strong_right > 0 or self.in_up_strong_left > 0:

            self.current_attack_attributes = self.up_strong_dmg

            if self.in_up_strong_right > 0:
                if self.in_up_strong_right == 7:
                    self.num_active_us = 4

                if self.num_active_us > 0:
                    self.hitbox_alteration(1, 20, 30, self.pos.x + 25, self.pos.y - 30)
                    self.num_active_us -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if not self.on_ground:
                    self.in_up_strong_right = 0
                    self.num_active_us = 0
                    self.num_lag = 0

            elif self.in_up_strong_left > 0:
                if self.in_up_strong_left == 7:
                    self.num_active_us = 4

                if self.num_active_us > 0:
                    self.hitbox_alteration(1, 20, 30, self.pos.x - 25, self.pos.y - 30)
                    self.num_active_us -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if not self.on_ground:
                    self.in_up_strong_left = 0
                    self.num_active_us = 0
                    self.num_lag = 0

        elif self.in_down_strong > 0:

            self.current_attack_attributes = self.down_strong_dmg

            if self.in_down_strong == 25:
                self.num_active_ds = 2

            if self.num_active_ds > 0:
                self.hitbox_alteration(1, 35, 60, self.pos.x + 18, self.pos.y - 30)
                self.hitbox_alteration(2, 35, 60, self.pos.x - 18, self.pos.y - 30)
                self.num_active_ds -= 1
            else:
                self.hitbox_alteration(1, 0, 0, 0, 0)
                self.hitbox_alteration(2, 0, 0, 0, 0)

            if not self.on_ground:
                self.in_down_strong = 0
                self.num_active_ds = 0
                self.num_lag = 0

        elif self.in_f_strong_right > 0 or self.in_f_strong_left > 0:

            self.current_attack_attributes = self.f_strong_dmg

            if self.in_f_strong_right > 0:
                if self.in_f_strong_right == 12:
                    self.num_active_fs = 6

                if self.num_active_fs > 0:
                    self.hitbox_alteration(1, 30, 20, self.pos.x + 25, self.pos.y - 30)
                    self.num_active_fs -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

                if not self.on_ground:
                    self.in_f_strong_right = 0
                    self.num_active_fs = 0
                    self.num_lag = 0

            elif self.in_f_strong_left > 0:
                if self.in_f_strong_left == 12:
                    self.num_active_fs = 6

                if self.num_active_fs > 0:
                    self.hitbox_alteration(1, 30, 20, self.pos.x - 25, self.pos.y - 30)
                    self.num_active_fs -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

        elif self.in_flash > 0:

            self.current_attack_attributes = self.flash_dmg

            if self.in_hitstop <= 0:
                self.in_flash -= 1

            self.vel.y = 0
            self.vel.x = 0

            if self.in_flash == 9:
                self.num_active_flash = 5

            if self.num_active_flash > 0:
                self.hitbox_alteration(1, 40, 73, self.pos.x + 20, self.pos.y - 27)  # HITBOX (1) SIZE
                self.hitbox_alteration(2, 40, 73, self.pos.x - 20, self.pos.y - 27)  # HITBOX (2) SIZE
                self.num_active_flash -= 1  # LOWER ACTIVE FRAMES
            else:
                self.hitbox_alteration(1, 0, 0, 0, 0)
                self.hitbox_alteration(2, 0, 0, 0, 0)

        elif self.in_neutral_special_right > 0 or self.in_neutral_special_left > 0:

            self.current_attack_attributes = 0

            if self.in_neutral_special_right > 0:

                self.in_neutral_special_right -= 1

                if self.in_neutral_special_right == 13:
                    self.projectile_active = 60
                    self.proj_pos_y = self.pos.y - 50
                    self.proj_pos_x = self.pos.x

            elif self.in_neutral_special_left > 0:
                self.in_neutral_special_left -= 1

                if self.in_neutral_special_left == 13:
                    self.projectile_active_left = 60
                    self.proj_pos_y = self.pos.y - 50
                    self.proj_pos_x = self.pos.x

        elif self.in_side_special_right > 0 or self.in_side_special_left > 0:
            self.current_attack_attributes = self.side_special_dmg
            if self.in_side_special_right > 0:

                if self.in_hitstop <= 0:
                    self.in_side_special_right -= 1

                if self.in_side_special_right == 19:
                    self.vel.x = 20

                if self.in_side_special_right == 10:
                    self.num_active_ss = 5

                if self.num_active_ss > 0:
                    self.hitbox_alteration(1, 50, 10, self.pos.x, self.pos.y - 27)
                    self.num_active_ss -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

            else:
                if self.in_hitstop <= 0:
                    self.in_side_special_left -= 1

                if self.in_side_special_left == 19:
                    self.vel.x = -20

                if self.in_side_special_left == 10:
                    self.num_active_ss = 5

                if self.num_active_ss > 0:
                    self.hitbox_alteration(1, 50, 10, self.pos.x, self.pos.y - 27)
                    self.num_active_ss -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)
                    self.hitbox_alteration(2, 0, 0, 0, 0)

        elif self.in_up_special_right > 0 or self.in_up_special_left > 0:
            self.current_attack_attributes = self.up_special_dmg1

            if self.in_up_special_right > 0:

                if self.in_up_special_right == len(self.up_special_right) - 7:
                    self.vel.y = -6
                    self.vel.x = 0.75

                if self.in_hitstop <= 0:
                    self.in_up_special_right -= 1

                if self.in_up_special_right == 69:
                    self.num_active_ub1 = 3

                if self.in_up_special_right == 65 and self.up_special_hit == 0:
                    self.num_active_ub2 = 20

                if self.num_active_ub1 > 0:
                    self.hitbox_alteration(1, 20, 30, self.pos.x + 20, self.pos.y - 27)
                    self.num_active_ub1 -= 1
                elif self.num_active_ub2 > 0:
                    self.hitbox_alteration(1, 20, 60, self.pos.x + 20, self.pos.y - 30)
                    self.num_active_ub2 -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)

            else:

                if self.in_up_special_left == len(self.up_special_left) - 7:
                    self.vel.y = -6
                    self.vel.x = - 0.75

                if self.in_hitstop <= 0:
                    self.in_up_special_left -= 1

                if self.in_up_special_left == 69:
                    self.num_active_ub1 = 3

                if self.in_up_special_left == 65 and self.up_special_hit == 0:
                    self.num_active_ub2 = 20

                if self.num_active_ub1 > 0:
                    self.hitbox_alteration(1, 20, 30, self.pos.x - 20, self.pos.y - 27)
                    self.num_active_ub1 -= 1
                elif self.num_active_ub2 > 0:
                    self.hitbox_alteration(1, 20, 60, self.pos.x - 20, self.pos.y - 30)
                    self.num_active_ub2 -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)

        elif self.in_down_special_right > 0 or self.in_down_special_left > 0:
            self.current_attack_attributes = self.down_special_ground_dmg

            if self.in_down_special_right > 0:

                if self.in_hitstop <= 0:
                    self.in_down_special_right -= 1

                if self.in_down_special_right == 17:
                    self.vel.x = 10

                if self.in_down_special_right == 16:
                    self.num_active_dsg = 10

                if self.num_active_dsg > 0:
                    self.hitbox_alteration(1, 40, 20, self.pos.x + 25, self.pos.y - 25)
                    self.num_active_dsg -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)

            else:
                if self.in_hitstop <= 0:
                    self.in_down_special_left -= 1

                if self.in_down_special_left == 17:
                    self.vel.x = -10

                if self.in_down_special_left == 16:
                    self.num_active_dsg = 10

                if self.num_active_dsg > 0:
                    self.hitbox_alteration(1, 40, 20, self.pos.x - 25, self.pos.y - 25)
                    self.num_active_dsg -= 1
                else:
                    self.hitbox_alteration(1, 0, 0, 0, 0)

        elif self.in_down_special_air_right > 0 or self.in_down_special_air_left > 0:
            if self.in_down_special_air_right > 0:

                if self.in_hitstop <= 0:
                    self.in_down_special_air_right -= 1

                if self.in_down_special_air_right == 16:
                    self.vel.x = 2
                    self.vel.y = 6

                if self.on_ground:
                    self.num_lag = 0
                    self.in_down_special_air_right = 0
                    self.num_active_dsa = 0

                if self.in_down_special_air_right == 13 or self.in_down_special_air_right == 6:
                    self.num_active_dsa = 5

                if self.num_active_dsa > 0:
                    self.hitbox_alteration(1, 20, 30, self.pos.x + 15, self.pos.y - 25)
                    self.num_active_dsa -= 1

            else:
                if self.in_hitstop <= 0:
                    self.in_down_special_air_left -= 1

                if self.in_down_special_air_left == 16:
                    self.vel.x = -2
                    self.vel.y = 6

                if self.on_ground:
                    self.num_lag = 0
                    self.in_down_special_air_left = 0
                    self.num_active_dsa = 0

                if self.in_down_special_air_left == 13 or self.in_down_special_air_left == 6:
                    self.num_active_dsa = 5

                if self.num_active_dsa > 0:
                    self.hitbox_alteration(1, 20, 30, self.pos.x - 15, self.pos.y - 25)
                    self.num_active_dsa -= 1
        else:
            self.hitbox_alteration(1, 0, 0, 0, 0)
            self.hitbox_alteration(2, 0, 0, 0, 0)

        # THIS WHOLE KNOCKBACK SYSTEM NEEDS A REWORK
        if self.take_knockback or self.knockback_frames > 0:

            if self.hitbox_1:
                component_x = attack_angle_p_1[0]
                component_y = attack_angle_p_1[1]
            elif self.hitbox_2:
                component_x = attack_angle_p_1[2]
                component_y = attack_angle_p_1[3]
            else:
                component_x = attack_angle_p_1[0]
                component_y = attack_angle_p_1[1]

            self.minHitstun = attack_angle_p_1[len(attack_angle_p_1) - 4]
            self.opponent_damage = attack_angle_p_1[len(attack_angle_p_1) - 3]
            self.base_knockback = attack_angle_p_1[len(attack_angle_p_1) - 2]
            self.knockback_scale = attack_angle_p_1[len(attack_angle_p_1) - 1]

            self.hitstop_counter += 1

            if self.hitstop_counter == 1:
                self.in_hitstop = self.find_hitstop(self.opponent_damage, 1)

            if self.take_knockback:
                self.call_hit(component_x, -1 * component_y, self.opponent_damage)
                self.take_knockback = False

            if self.in_hitstop > 0:
                self.knockback_num_x = 0
                self.knockback_num_y = 0

                self.knockback_frames = round(math.sqrt(self.knockback_formula(component_x) ** 2 +
                                                        self.knockback_formula(component_y) ** 2) / (2 * self.gravity) -
                                              (2 * math.sqrt(self.knockback_formula(component_x) ** 2 +
                                                             self.knockback_formula(component_y) ** 2)) + (
                                                      0.1 * self.percentage)) + \
                                        self.minHitstun + self.find_hitstop(self.opponent_damage, 1) + 1

            if self.knockback_frames == self.total_knockback and self.in_hitstop <= 0:
                self.knockback_num_x = self.knockback_formula(component_x)
                self.knockback_num_y = self.knockback_formula((-1 * component_y))

            if self.knockback_frames == (self.total_knockback - 1):
                self.percentage += self.opponent_damage
                if self.flash_percent <= 100 - self.opponent_damage * 2:
                    self.flash_percent += self.opponent_damage * 2
                else:
                    self.flash_percent = 100

            self.vel.x = self.knockback_num_x
            self.vel.y = self.knockback_num_y

            self.hitbox_alteration(1, 0, 0, 0, 0)
            self.hitbox_alteration(2, 0, 0, 0, 0)

            self.knockback_frames -= 1
            self.take_momentum = True

        if self.take_momentum and self.knockback_frames == 0:
            self.vel.x = self.knockback_num_x
            if self.vel.x < -0.2:
                self.knockback_num_x += 0.04
            elif self.vel.x > 0.2:
                self.knockback_num_x -= 0.04

            if abs(self.in_momentum) >= abs(self.vel.x) / 2:
                self.take_momentum = False

        # END OF KNOCKBACK SYSTEM

        # ANIMATION PRIORITY
        # HITSTUN
        if self.platform_hitstun > 0:
            if self.direction:
                self.hurtbox_alteration(pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png").convert_alpha(),
                                        (self.pos.x, self.pos.y - 50))
            else:
                self.hurtbox_alteration(
                    pygame.image.load("../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png").convert_alpha(),
                    (self.pos.x, self.pos.y - 50))
        elif self.numHitstun > 0:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.direction:
                self.hurtbox_alteration(self.hitstunLeft, (self.pos.x, self.pos.y - 50))
            else:
                self.hurtbox_alteration(self.hitstunRight, (self.pos.x, self.pos.y - 50))
        # JUMPSQUAT
        elif self.in_jumpsquat > 0:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.direction:
                self.hurtbox_alteration(self.jumpsquat_right[(len(self.jumpsquat_right) - 1) - self.in_jumpsquat],
                                        (self.pos.x, self.pos.y - 50))
            else:
                self.hurtbox_alteration(self.jumpsquat_left[(len(self.jumpsquat_left) - 1) - self.in_jumpsquat],
                                        (self.pos.x, self.pos.y - 50))
        # DOUBLE JUMPING

        # ROLLS/ AIRDODGES
        # ROLLS
        elif self.roll_right_frames > 0 or self.roll_left_frames > 0:
            self.hurtbox_size_alteration((30, 30), (self.pos.x, self.pos.y - 17))
            if self.roll_right_frames > 0:
                self.hurtbox_alteration(self.roll_right[(len(self.roll_right) - 1) - self.roll_right_frames],
                                        (self.pos.x, self.pos.y - 50))
            elif self.roll_left_frames > 0:
                self.hurtbox_alteration(self.roll_left[(len(self.roll_left) - 1) - self.roll_left_frames],
                                        (self.pos.x, self.pos.y - 50))

        # AIRDODGES
        elif self.airdodge_left_frames > 0 or self.airdodge_right_frames > 0:
            self.hurtbox_size_alteration((30, 30), (self.pos.x, self.pos.y - 27))
            if self.set_velocity == "Left":
                self.vel.x = -1
            elif self.set_velocity == "Right":
                self.vel.x = 1
            elif self.set_velocity == "Up":
                self.vel.y = -4
            elif self.set_velocity == "Down":
                self.vel.y = 4
            elif self.set_velocity == "Up-Left":
                self.vel.x = -1
                self.vel.y = -4
            elif self.set_velocity == "Up-Right":
                self.vel.x = 1
                self.vel.y = -4
            elif self.set_velocity == "Down-Left":
                self.vel.x = -1
                self.vel.y = 4
            elif self.set_velocity == "Down-Right":
                self.vel.x = 1
                self.vel.y = 4

            if self.airdodge_left_frames > 0:
                self.hurtbox_alteration(self.airdodge_left[(len(self.airdodge_left) - 1) - self.airdodge_left_frames],
                                        (self.pos.x, self.pos.y - 50))
            elif self.airdodge_right_frames > 0:
                self.hurtbox_alteration(
                    self.airdodge_right[(len(self.airdodge_right) - 1) - self.airdodge_right_frames],
                    (self.pos.x, self.pos.y - 50))

        # SPECIAL ATTACKS

        # NEUTRAL SPECIAL
        elif self.in_neutral_special_right > 0 or self.in_neutral_special_left > 0:
            # time.sleep(1)
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.in_neutral_special_right > 0:
                self.hurtbox_alteration(
                    self.neutral_special_right[(len(self.neutral_special_right) - 1) - self.in_neutral_special_right],
                    (self.pos.x, self.pos.y - 50))
            else:
                self.hurtbox_alteration(
                    self.neutral_special_left[(len(self.neutral_special_left) - 1) - self.in_neutral_special_left],
                    (self.pos.x, self.pos.y - 50))

        # SIDE SPECIAL
        elif self.in_side_special_right > 0 or self.in_side_special_left > 0:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            # time.sleep(1)
            if self.in_side_special_right > 0:
                self.hurtbox_alteration(
                    self.side_special_right[(len(self.side_special_right) - 1) - self.in_side_special_right],
                    (self.pos.x, self.pos.y - 50))
            else:
                self.hurtbox_alteration(
                    self.side_special_left[(len(self.side_special_left) - 1) - self.in_side_special_left],
                    (self.pos.x, self.pos.y - 50))

        # UP SPECIAL
        elif self.in_up_special_right > 0 or self.in_up_special_left > 0:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.in_up_special_right > 0:
                self.hurtbox_alteration(
                    self.up_special_right[(len(self.up_special_right) - 1) - self.in_up_special_right],
                    (self.pos.x, self.pos.y - 50))
            else:
                self.hurtbox_alteration(
                    self.up_special_left[(len(self.up_special_left) - 1) - self.in_up_special_left],
                    (self.pos.x, self.pos.y - 50))

        # DOWN SPECIAL
        elif self.in_down_special_right > 0 or self.in_down_special_left > 0 or self.in_down_special_air_right > 0 or self.in_down_special_air_left > 0:
            if self.on_ground:
                self.hurtbox_size_alteration((40, 40), (self.pos.x, self.pos.y - 27))
            else:
                self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 42))

            if self.in_down_special_right > 0:
                self.hurtbox_alteration(
                    self.down_special_ground_right[
                        (len(self.down_special_ground_right) - 1) - self.in_down_special_right],
                    (self.pos.x, self.pos.y - 50))
            elif self.in_down_special_left > 0:
                self.hurtbox_alteration(
                    self.down_special_ground_left[(len(self.down_special_ground_left) - 1) - self.in_down_special_left],
                    (self.pos.x, self.pos.y - 50))
            elif self.in_down_special_air_right > 0:
                self.hurtbox_alteration(
                    self.down_special_air_right[
                        (len(self.down_special_air_right) - 1) - self.in_down_special_air_right],
                    (self.pos.x, self.pos.y - 50))
            else:
                self.hurtbox_alteration(
                    self.down_special_air_left[(len(self.down_special_air_left) - 1) - self.in_down_special_air_left],
                    (self.pos.x, self.pos.y - 50))

        # FLASH ATTACK
        elif self.in_flash > 0:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.direction:
                self.hurtbox_alteration(self.flash_attack_right[self.in_flash], (self.pos.x - 15, self.pos.y - 40))
            else:
                self.hurtbox_alteration(self.flash_attack_left[self.in_flash], (self.pos.x + 15, self.pos.y - 40))

        # UP SMASH
        elif self.in_up_strong_right > 0 or self.in_up_strong_left > 0 and self.on_ground:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.in_up_strong_right > 0:
                self.hurtbox_alteration(self.up_strong_right[self.in_up_strong_right],
                                        (self.pos.x, self.pos.y - 50))
            elif self.in_up_strong_left > 0:
                self.hurtbox_alteration(self.up_strong_left[self.in_up_strong_left],
                                        (self.pos.x + 11, self.pos.y - 50))

        # DOWN SMASH
        elif self.in_down_strong > 0 and self.on_ground:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.direction:
                self.hurtbox_alteration(self.down_strong_right[self.in_down_strong],
                                        (self.pos.x, self.pos.y - 25))
            else:
                self.hurtbox_alteration(self.down_strong_left[self.in_down_strong],
                                        (self.pos.x, self.pos.y - 25))

        # FORWARD SMASH
        elif self.in_f_strong_right > 0 or self.in_f_strong_left > 0 and self.on_ground:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.in_f_strong_right > 0:
                self.hurtbox_alteration(self.f_strong_right[self.in_f_strong_right],
                                        (self.pos.x - 2, self.pos.y - 26))
            if self.in_f_strong_left > 0:
                self.hurtbox_alteration(self.f_strong_left[self.in_f_strong_left],
                                        (self.pos.x - 2, self.pos.y - 26))

        # FORWARD AIR
        elif self.in_f_air_right > 0 or self.in_f_air_left > 0:
            if self.in_f_air_right > 0:
                self.hurtbox_alteration(self.f_air_right[(len(self.f_air_right) - 1) - self.in_f_air_right],
                                        (self.pos.x, self.pos.y - 50))
                if 3 <= self.in_f_air_right <= 15:
                    self.hurtbox_size_alteration((50, 30), (self.pos.x, self.pos.y - 50))
                else:
                    self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))

            elif self.in_f_air_left > 0:
                self.hurtbox_alteration(self.f_air_left[(len(self.f_air_left) - 1) - self.in_f_air_left],
                                        (self.pos.x, self.pos.y - 50))
                if 3 <= self.in_f_air_left <= 15:
                    self.hurtbox_size_alteration((50, 30), (self.pos.x, self.pos.y - 50))
                else:
                    self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))

        # BACK AIR
        elif self.in_back_air_right > 0 or self.in_back_air_left > 0:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.in_back_air_right > 0:
                self.hurtbox_alteration(self.back_air_right[(len(self.back_air_right) - 1) - self.in_back_air_right],
                                        (self.pos.x, self.pos.y - 50))

            elif self.in_back_air_left > 0:
                self.hurtbox_alteration(self.back_air_left[(len(self.back_air_left) - 1) - self.in_back_air_left],
                                        (self.pos.x, self.pos.y - 50))

        # UP AIR
        elif self.in_up_air_left > 0 or self.in_up_air_right > 0:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.in_up_air_right > 0:
                self.hurtbox_alteration(self.up_air_right[(len(self.up_air_right) - 1) - self.in_up_air_right],
                                        (self.pos.x, self.pos.y - 50))
            elif self.in_up_air_left > 0:
                self.hurtbox_alteration(self.up_air_left[(len(self.up_air_left) - 1) - self.in_up_air_left],
                                        (self.pos.x, self.pos.y - 50))

        # DOWN AIR
        elif self.in_down_air > 0:
            self.hurtbox_size_alteration((30, 60), (self.pos.x, self.pos.y - 37))
            if self.direction:
                self.hurtbox_alteration(self.down_air_right[(len(self.down_air_right) - 1) - self.in_down_air],
                                        (self.pos.x, self.pos.y - 50))
            else:
                self.hurtbox_alteration(self.down_air_left[(len(self.down_air_left) - 1) - self.in_down_air],
                                        (self.pos.x, self.pos.y - 50))

        # NEUTRAL AIR
        elif self.in_neutral_air_right > 0 or self.in_neutral_air_left > 0:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.in_neutral_air_right > 0:
                self.hurtbox_alteration(self.neutral_air[(len(self.neutral_air) - 1) -
                                                         self.in_neutral_air_right], (self.pos.x, self.pos.y - 25))
            elif self.in_neutral_air_left > 0:
                self.hurtbox_alteration(self.neutral_air[(len(self.neutral_air) - 1) -
                                                         self.in_neutral_air_left], (self.pos.x, self.pos.y - 25))

        # FORWARD TILT
        elif self.in_f_tilt > 0 or self.in_f_tilt_left > 0:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.in_f_tilt > 0:
                self.hurtbox_alteration(self.f_tilt_right[(len(self.f_tilt_right) - 1) - self.in_f_tilt],
                                        (self.pos.x, self.pos.y - 50))
            elif self.in_f_tilt_left > 0:
                self.hurtbox_alteration(self.f_tilt_left[(len(self.f_tilt_left) - 1) - self.in_f_tilt_left],
                                        (self.pos.x, self.pos.y - 50))
        # UP TILT
        elif self.in_up_tilt > 0:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.direction:
                self.hurtbox_alteration(self.up_tilt_right[(len(self.up_tilt_right) - 1) - self.in_up_tilt],
                                        (self.pos.x, self.pos.y - 50))
            else:
                self.hurtbox_alteration(self.up_tilt_left[(len(self.up_tilt_left) - 1) - self.in_up_tilt],
                                        (self.pos.x, self.pos.y - 50))
        # DOWN TILT
        elif self.in_down_tilt_left > 0 or self.in_down_tilt_right > 0:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.in_down_tilt_left > 0:
                self.hurtbox_alteration(self.down_tilt_left[(len(self.down_tilt_left) - 1) - self.in_down_tilt_left],
                                        (self.pos.x, self.pos.y - 50))
            elif self.in_down_tilt_right > 0:
                self.hurtbox_alteration(self.down_tilt_right[(len(self.down_tilt_right) - 1) - self.in_down_tilt_right],
                                        (self.pos.x, self.pos.y - 50))
        # JAB (NEUTRAL TILT)
        elif self.in_jab_left > 0 or self.in_jab_right > 0:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.in_jab_right > 0:
                self.hurtbox_alteration(self.jab_right[(len(self.jab_right) - 1) - self.in_jab_right],
                                        (self.pos.x, self.pos.y - 50))
            elif self.in_jab_left > 0:
                self.hurtbox_alteration(self.jab_left[(len(self.jab_left) - 1) - self.in_jab_left],
                                        (self.pos.x, self.pos.y - 50))

        # WALKING + CROUCHING
        elif self.on_ground:
            if self.pressing_right:
                self.hurtbox_alteration(
                    self.walk_cycle_right[(len(self.walk_cycle_right) - 1) - self.in_walk_cycle_right],
                    (self.pos.x, self.pos.y - 50))
                self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))

            elif self.pressing_left:
                self.hurtbox_alteration(self.walk_cycle_left[(len(self.walk_cycle_left) - 1) - self.in_walk_cycle_left],
                                        (self.pos.x, self.pos.y - 50))
                self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))

            elif self.crouch_frames > 0:
                self.hurtbox_size_alteration((30, 40), (self.pos.x, self.pos.y - 22))
                if self.direction:
                    self.hurtbox_alteration(self.crouch_right[(len(self.crouch_right) - 1) - self.crouch_frames],
                                            (self.pos.x, self.pos.y - 50))
                else:
                    self.hurtbox_alteration(self.crouch_left[(len(self.crouch_left) - 1) - self.crouch_frames],
                                            (self.pos.x, self.pos.y - 50))
            else:
                self.idleCycle()

        # AIR DRIFTING
        elif not self.on_ground:
            self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))
            if self.direction:
                self.hurtbox_alteration(self.jump_right, (self.pos.x, self.pos.y - 50))
            else:
                self.hurtbox_alteration(self.jump_left, (self.pos.x, self.pos.y - 50))

    def attack(self, attack_key, left_key, right_key, up_key, down_key):
        pressed_keys = pygame.key.get_pressed()

        if (pressed_keys[attack_key] and (pressed_keys[left_key] or pressed_keys[right_key]) and not (
                self.in_lag or self.is_shielding)) or \
                (not self.in_lag and self.in_buffer[0] == "Attack" and (
                        self.in_buffer[1] == "Right" or self.in_buffer[1] == "Left")):
            if pressed_keys[right_key] or self.in_buffer[1] == "Right":
                if self.on_ground:
                    self.num_lag = len(self.f_tilt_right)
                    self.in_f_tilt = len(self.f_tilt_right)
                elif not self.on_ground and self.direction:
                    self.num_lag = len(self.f_air_right) + 3
                    self.in_f_air_right = len(self.f_air_right)
                elif not self.on_ground and not self.direction:
                    self.num_lag = len(self.back_air_left)
                    self.in_back_air_left = len(self.back_air_left)
            elif pressed_keys[left_key] or self.in_buffer[1] == "Left":
                if self.on_ground:
                    self.num_lag = len(self.f_tilt_left)
                    self.in_f_tilt_left = len(self.f_tilt_left)
                elif not self.on_ground and not self.direction:
                    self.num_lag = len(self.f_air_left) + 3
                    self.in_f_air_left = len(self.f_air_left)
                elif not self.on_ground and self.direction:
                    self.num_lag = len(self.back_air_right)
                    self.in_back_air_right = len(self.back_air_right)
        elif (pressed_keys[attack_key] and pressed_keys[up_key] and not (self.in_lag or self.is_shielding)) or \
                (not self.in_lag and self.in_buffer[0] == "Attack" and self.in_buffer[1] == "Up"):
            if self.on_ground:
                self.num_lag = len(self.up_tilt_right)
                self.in_up_tilt = len(self.up_tilt_right)
            else:
                self.num_lag = len(self.up_air_right)
                if self.direction:
                    self.in_up_air_right = len(self.up_air_right)
                else:
                    self.in_up_air_left = len(self.up_air_left)
        elif pressed_keys[attack_key] and pressed_keys[down_key] and not (self.in_lag or self.is_shielding) or \
                (not self.in_lag and self.in_buffer[0] == "Attack" and self.in_buffer[1] == "Down"):
            if self.on_ground:
                self.num_lag = len(self.down_tilt_right) + 1
                if self.direction:
                    self.in_down_tilt_right = len(self.down_tilt_right)
                else:
                    self.in_down_tilt_left = len(self.down_tilt_left)
            elif not self.on_ground:
                self.num_lag = len(self.down_air_right)
                self.in_down_air = len(self.down_air_right)

        elif pressed_keys[attack_key] and not (self.in_lag or self.is_shielding) or \
                (not self.in_lag and self.in_buffer[0] == "Attack" and self.in_buffer[1] is None):
            if self.on_ground:
                self.num_lag = len(self.jab_right)
                if self.direction:
                    self.in_jab_right = len(self.jab_right)
                else:
                    self.in_jab_left = len(self.jab_left)
            else:
                self.num_lag = len(self.neutral_air)
                if self.direction:
                    self.in_neutral_air_right = len(self.neutral_air)
                else:
                    self.in_neutral_air_left = len(self.neutral_air)

    def special_attack(self, special_button, left_button, right_button, up_button, down_button):
        pressed_keys = pygame.key.get_pressed()

        if (pressed_keys[special_button] and (pressed_keys[left_button] or pressed_keys[right_button])
            and self.numHitstun <= 0 and not self.in_lag) or \
                (not self.in_lag and self.numHitstun <= 0 and self.in_buffer[0] == "Special" and (
                        self.in_buffer[1] == "Right" or self.in_buffer[1] == "Left")):
            self.num_lag = len(self.side_special_right)
            if self.direction:
                self.in_side_special_right = len(self.side_special_right)
            else:
                self.in_side_special_left = len(self.side_special_left)

        elif pressed_keys[special_button] and pressed_keys[up_button] and self.numHitstun <= 0 and not self.in_lag or \
                (not self.in_lag and self.numHitstun <= 0 and self.in_buffer[0] == "Special" and self.in_buffer[
                    1] == "Up"):
            self.num_lag = len(self.up_special_right)
            self.special_lag = len(self.up_special_right)
            if self.direction:
                self.in_up_special_right = len(self.up_special_right)
            else:
                self.in_up_special_left = len(self.up_special_left)

        elif pressed_keys[special_button] and pressed_keys[down_button] and self.numHitstun <= 0 and not self.in_lag or \
                (not self.in_lag and self.numHitstun <= 0 and self.in_buffer[0] == "Special" and self.in_buffer[
                    1] == "Down"):
            if self.on_ground:
                self.num_lag = len(self.down_special_ground_right)
                if self.direction:
                    self.in_down_special_right = len(self.down_special_ground_right)
                else:
                    self.in_down_special_left = len(self.down_special_ground_left)
            else:
                self.num_lag = len(self.down_special_air_right)
                if self.direction:
                    self.in_down_special_air_right = len(self.down_special_air_right)
                else:
                    self.in_down_special_air_left = len(self.down_special_air_left)

        elif pressed_keys[special_button] and self.numHitstun <= 0 and not self.in_lag and \
                self.projectile_active <= 0 and self.projectile_active_left <= 0 or \
                (not self.in_lag and self.numHitstun <= 0 and self.in_buffer[0] == "Special" and
                 self.in_buffer[1] is None and self.projectile_active <= 0 and self.projectile_active_left <= 0):
            self.num_lag = len(self.neutral_special_right)
            if self.direction:
                self.in_neutral_special_right = len(self.neutral_special_right)
            else:
                self.in_neutral_special_left = len(self.neutral_special_left)

        if self.projectile_active > 0:
            self.proj_image = "../PlatformFighter/Stickman Character/Neutral Special/Neutral_B_Projectile.png"

            self.proj_pos_x += 5

            self.projectile_active -= 1

            self.hitbox_alteration("Projectile", 20, 20, self.proj_pos_x, self.proj_pos_y + 30)

        elif self.projectile_active_left > 0:
            self.proj_image = "../PlatformFighter/Stickman Character/Neutral " \
                              "Special/Neutral_B_projectile_reverse.png "

            self.proj_pos_x -= 5

            self.projectile_active_left -= 1

            self.hitbox_alteration("Projectile", 20, 20, self.proj_pos_x, self.proj_pos_y + 30)

        else:
            self.proj_image = None
            self.proj_pos_x = 0
            self.proj_pos_y = 0

            self.hitbox_alteration("Projectile", 0, 0, 0, 0)

    def strong_attacks(self, strong_key, up_key, down_key):
        pressed_keys = pygame.key.get_pressed()

        if ((pressed_keys[strong_key] and pressed_keys[up_key]) and not (self.in_lag or self.is_shielding)
            and self.on_ground) or (not self.in_lag and self.on_ground and self.in_buffer[0] == "Strong" and (self.in_buffer[1] == "Up")) or \
                (pressed_keys[strong_key] and (self.in_up_strong_right > 0 or self.in_up_strong_left > 0) and self.num_rotations <= 24 and self.on_ground):
            if self.direction:
                self.num_lag = 2
                self.in_up_strong_right += 1

                if self.in_up_strong_right == 6:
                    self.in_up_strong_right = 5
                    self.num_rotations += 1
            else:
                self.num_lag = 2
                self.in_up_strong_left += 1

                if self.in_up_strong_left == 6:
                    self.in_up_strong_left = 5
                    self.num_rotations += 1

        elif ((pressed_keys[strong_key] and pressed_keys[down_key]) and not (self.in_lag or self.is_shielding)
              and self.on_ground) or (not self.in_lag and self.on_ground and self.in_buffer[0] == "Strong" and (self.in_buffer[1] == "Down")) \
                or (pressed_keys[strong_key] and self.in_down_strong > 0 and self.num_rotations <= 12 and self.on_ground):
            self.num_lag = 2
            self.in_down_strong += 1

            if self.in_down_strong == 21:
                self.in_down_strong = 19
                self.num_rotations += 1

        elif pressed_keys[strong_key] and not (self.in_lag or self.is_shielding) and self.on_ground or \
                (not self.in_lag and self.on_ground and self.in_buffer[0] == "Strong" and (self.in_buffer[1] == "Right" or self.in_buffer[1] == "Left" or self.in_buffer[1] is None)) \
                or (pressed_keys[strong_key] and (self.in_f_strong_right > 0 or self.in_f_strong_left > 0) and self.num_rotations <= 4 and self.on_ground):
            if self.direction:
                self.num_lag = 2

                self.in_f_strong_right += 1

                if self.in_f_strong_right == 10:
                    self.in_f_strong_right = 4
                    self.num_rotations += 1

            else:
                self.num_lag = 2

                self.in_f_strong_left += 1

                if self.in_f_strong_left == 10:
                    self.in_f_strong_left = 4
                    self.num_rotations += 1

        if self.in_hitstop <= 0:
            if (not pressed_keys[strong_key] or self.num_rotations > 24) and \
                    self.in_up_strong_right > 0 and self.on_ground:
                self.in_up_strong_right += 1
                self.num_lag = 2

            if self.in_up_strong_right >= len(self.up_strong_right) - 1 and self.on_ground:
                self.in_up_strong_right = 0
                self.num_lag = 10
                self.num_rotations = 0

        if self.in_hitstop <= 0:
            if (not pressed_keys[strong_key] or self.num_rotations > 24) and \
                    self.in_up_strong_left > 0 and self.on_ground:
                self.in_up_strong_left += 1
                self.num_lag = 2

            if self.in_up_strong_left >= len(self.up_strong_left) - 1 and self.on_ground:
                self.in_up_strong_left = 0
                self.num_lag = 10
                self.num_rotations = 0

        if self.in_hitstop <= 0:
            if (not pressed_keys[strong_key] or self.num_rotations > 12) and self.in_down_strong > 0 and self.on_ground:
                self.in_down_strong += 1
                self.num_lag = 2

            if self.in_down_strong >= len(self.down_strong_right) - 1 and self.on_ground:
                self.in_down_strong = 0
                self.num_lag = 5
                self.num_rotations = 0

        if self.in_hitstop <= 0:
            if (not pressed_keys[strong_key] or self.num_rotations > 4) and \
                    self.in_f_strong_right > 0 and self.on_ground:
                self.in_f_strong_right += 1
                self.num_lag = 2

            if self.in_f_strong_right >= len(self.f_strong_right) - 1 and self.on_ground:
                self.in_f_strong_right = 0
                self.num_lag = 10
                self.num_rotations = 0

            if (not pressed_keys[
                strong_key] or self.num_rotations > 4) and self.in_f_strong_left > 0 and self.on_ground:
                self.in_f_strong_left += 1
                self.num_lag = 2

            if self.in_f_strong_left >= len(self.f_strong_left) - 1 and self.on_ground:
                self.in_f_strong_left = 0
                self.num_lag = 10
                self.num_rotations = 0

    def shielding(self, shield_key, left_key, right_key):
        pressed_keys = pygame.key.get_pressed()
        shield_direction = None

        if (pressed_keys[shield_key] and self.on_ground and self.numHitstun == 0 and
            self.num_lag == 0 and self.frames_after_jump == 0) or self.shieldstun > 0:
            self.is_shielding = True
            if pressed_keys[left_key]:
                self.shield_size(15, 65, self.pos.x - 25, self.pos.y - 30, 30, 15, self.pos.x - 17, self.pos.y - 60,
                                 self.pos.y)
                self.vel.x = 0
                self.direction = False
                shield_direction = "Left"
            elif pressed_keys[right_key]:
                self.shield_size(15, 65, self.pos.x + 25, self.pos.y - 30, 30, 15, self.pos.x + 18, self.pos.y - 60,
                                 self.pos.y)
                self.vel.x = 0
                self.direction = True
                shield_direction = "Right"
            else:
                if self.direction:
                    self.shield_size(15, 65, self.pos.x + 25, self.pos.y - 30, 30, 15, self.pos.x + 18, self.pos.y - 60,
                                     self.pos.y)
                    self.vel.x = 0
                    shield_direction = "Right"
                else:
                    self.shield_size(15, 65, self.pos.x - 25, self.pos.y - 30, 30, 15, self.pos.x - 17, self.pos.y - 60,
                                     self.pos.y)
                    self.vel.x = 0
                    shield_direction = "Left"
        else:
            self.is_shielding = False
            self.shield_size(0, 0, 0, 0, 0, 0, 0, 0, 0)

        return shield_direction

    def roll(self, left_key, right_key, down_key):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[
            left_key] and self.is_shielding and 0 < self.press_left_frames <= 5 and not self.roll_left_active and self.roll_left_frames == 0:
            self.roll_left_active = True
            self.vel.x = -9
        elif pressed_keys[
            right_key] and self.is_shielding and 0 < self.press_right_frames <= 5 and not self.roll_right_active and self.roll_right_frames == 0:
            self.roll_right_active = True
            self.vel.x = 9
        elif pressed_keys[left_key] and self.is_shielding:
            self.press_left_frames = 7
        elif pressed_keys[right_key] and self.is_shielding:
            self.press_right_frames = 7
        elif pressed_keys[down_key] and self.is_shielding:
            pass
            # print("spotdodge")
        else:
            self.roll_left_active = False
            self.roll_right_active = False

        if self.roll_left_active:
            self.roll_left_frames = len(self.roll_left)
            self.num_lag = len(self.roll_left)
        elif self.roll_right_active:
            self.roll_right_frames = len(self.roll_right)
            self.num_lag = len(self.roll_right)

        if self.roll_left_frames == 18 or self.roll_right_frames == 18:
            self.invincibility_frames = 10

        if self.roll_left_frames > 0:
            self.roll_left_frames -= 1

        if self.roll_right_frames > 0:
            self.roll_right_frames -= 1

    def airdodge(self, left_key, right_key, up_key, down_key, shield_key):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[shield_key] and not self.on_ground and not self.in_lag and self.airdodge_capable:
            self.airdodge_capable = False
            if pressed_keys[left_key]:
                self.airdodge_left_frames = len(self.airdodge_left)
                self.num_lag = len(self.airdodge_left)
                self.direction = False
                if pressed_keys[up_key]:
                    self.set_velocity = "Up-Left"
                elif pressed_keys[down_key]:
                    self.set_velocity = "Down-Left"
                else:
                    self.set_velocity = "Left"

            elif pressed_keys[right_key]:
                self.airdodge_right_frames = len(self.airdodge_right)
                self.num_lag = len(self.airdodge_right)
                self.direction = True
                if pressed_keys[up_key]:
                    self.set_velocity = "Up-Right"
                elif pressed_keys[down_key]:
                    self.set_velocity = "Down-Right"
                else:
                    self.set_velocity = "Right"

            elif pressed_keys[up_key]:
                self.set_velocity = "Up"
                self.num_lag = len(self.airdodge_left)
                if self.direction:
                    self.airdodge_right_frames = len(self.airdodge_right)
                else:
                    self.airdodge_left_frames = len(self.airdodge_left)

            elif pressed_keys[down_key]:
                self.set_velocity = "Down"
                self.num_lag = len(self.airdodge_left)
                if self.direction:
                    self.airdodge_right_frames = len(self.airdodge_right)
                else:
                    self.airdodge_left_frames = len(self.airdodge_left)

            else:
                self.set_velocity = "Neutral"
                self.num_lag = len(self.airdodge_left)
                if self.direction:
                    self.airdodge_right_frames = len(self.airdodge_right)
                else:
                    self.airdodge_left_frames = len(self.airdodge_left)

        if self.airdodge_left_frames > 0:
            self.airdodge_left_frames -= 1

            if self.on_ground:
                self.num_lag = 5
                self.airdodge_left_frames = 0

        if self.airdodge_right_frames > 0:
            self.airdodge_right_frames -= 1

            if self.on_ground:
                self.num_lag = 5
                self.airdodge_right_frames = 0

        if self.airdodge_left_frames == 18 or self.airdodge_right_frames == 18:
            self.invincibility_frames = 10

    def get_angle(self, attack_attributes):
        # ATTACK ATTRIBUTES (or ATTACK_ANGLE_P_1) FORMAT: (X_COMPONENT (1), Y_COMPONENT(1), X_COMPONENT(2),
        # Y_COMPONENT(2), MIN HITSTUN, ATTACK_DAMAGE, BASE_KNOCKBACK, KNOCKBACK_SCALING)
        if self.num_active > 0:
            if self.direction:
                if self.jab_1:
                    attack_attributes = (
                        self.jab_1_x, self.jab_1_y, 0, 0, self.jab_1_hitstun, self.jab_1_dmg, self.jab_1_base,
                        self.jab_1_scale)
                elif self.jab_2:
                    attack_attributes = (
                        self.jab_2_x, self.jab_2_y, 0, 0, self.jab_2_hitstun, self.jab_2_dmg, self.jab_2_base,
                        self.jab_2_scale)
            else:
                if self.jab_1:
                    attack_attributes = (
                        -1 * self.jab_1_x, self.jab_1_y, 0, 0, self.jab_1_hitstun, self.jab_1_dmg, self.jab_1_base,
                        self.jab_1_scale)
                elif self.jab_2:
                    attack_attributes = (
                        -1 * self.jab_2_x, self.jab_2_y, 0, 0, self.jab_2_hitstun, self.jab_2_dmg, self.jab_2_base,
                        self.jab_2_scale)

        elif self.num_active_f > 0:
            if self.on_ground:
                if self.direction:
                    attack_attributes = (
                        self.f_tilt_x, self.f_tilt_y, 0, 0, self.f_tilt_hitstun, self.f_tilt_dmg, self.f_tilt_base,
                        self.f_tilt_scale)
                else:
                    attack_attributes = (
                        -1 * self.f_tilt_x, self.f_tilt_y, 0, 0, self.f_tilt_hitstun, self.f_tilt_dmg,
                        self.f_tilt_base,
                        self.f_tilt_scale)
            else:
                if self.direction:
                    attack_attributes = (
                        self.f_air_x, self.f_air_y, 0, 0, self.f_air_hitstun, self.f_air_dmg, self.f_air_base,
                        self.f_air_scale)

                else:
                    attack_attributes = (
                        -1 * self.f_air_x, self.f_air_y, 0, 0, self.f_air_hitstun, self.f_air_dmg, self.f_air_base,
                        self.f_air_scale)

        elif self.num_active_b > 0:
            if self.direction:
                attack_attributes = (
                    -1 * self.back_air_x, self.back_air_y, 0, 0, self.back_air_hitstun, self.back_air_dmg,
                    self.back_air_base,
                    self.back_air_scale)

            else:
                attack_attributes = (
                    self.back_air_x, self.back_air_y, 0, 0, self.back_air_hitstun, self.back_air_dmg,
                    self.back_air_base,
                    self.back_air_scale)

        elif self.num_active_u > 0:
            if self.on_ground:
                attack_attributes = (
                    self.up_tilt2_x, self.up_tilt2_y, 0, 0, self.up_tilt2_hitstun, self.up_tilt2_dmg,
                    self.up_tilt2_base,
                    self.up_tilt2_scale)
            else:
                if self.direction:
                    attack_attributes = (
                        self.up_air_x, self.up_air_y, 0, 0, self.up_air_hitstun, self.up_air_dmg, self.up_air_base,
                        self.up_air_scale)
                else:
                    attack_attributes = (
                        -1 * self.up_air_x, self.up_air_y, 0, 0, self.up_air_hitstun, self.up_air_dmg,
                        self.up_air_base,
                        self.up_air_scale)

        elif self.num_active_u2 > 0:
            if self.on_ground:
                attack_attributes = (
                    -1 * self.up_tilt1_x, self.up_tilt1_y, self.up_tilt1_x,
                    self.up_tilt1_y, self.up_tilt1_hitstun, self.up_tilt1_dmg, self.up_tilt1_base,
                    self.up_tilt1_scale)

        elif self.num_active_d > 0:
            if self.on_ground:
                if self.direction:
                    attack_attributes = (
                        self.down_tilt_x, self.down_tilt_y, 0, 0, self.down_tilt_hitstun, self.down_tilt_dmg,
                        self.down_tilt_base,
                        self.down_tilt_scale)
                else:
                    attack_attributes = (
                        -1 * self.down_tilt_x, self.down_tilt_y, 0, 0, self.down_tilt_hitstun, self.down_tilt_dmg,
                        self.down_tilt_base,
                        self.down_tilt_scale)
            else:
                attack_attributes = (
                    self.down_air_x, self.down_air_y, 0, 0, self.down_air_hitstun, self.down_air_dmg,
                    self.down_air_base,
                    self.down_air_scale)

        elif self.num_active_n13 > 0:
            attack_attributes = (self.neutral_air_13_x, self.neutral_air_13_y, 0, 0, self.neutral_air_13_hitstun,
                                 self.neutral_air_13_dmg, self.neutral_air_13_base, self.neutral_air_13_scale)

        elif self.num_active_n4 > 0:
            if self.direction:
                attack_attributes = (self.neutral_air_4_x, self.neutral_air_4_y, 0, 0, self.neutral_air_4_hitstun,
                                     self.neutral_air_4_dmg, self.neutral_air_4_base, self.neutral_air_4_scale)
            else:
                attack_attributes = (
                    -1 * self.neutral_air_4_x, self.neutral_air_4_y, 0, 0, self.neutral_air_4_hitstun,
                    self.neutral_air_4_dmg, self.neutral_air_4_base, self.neutral_air_4_scale)

        elif self.num_active_us > 0:
            if self.direction:
                attack_attributes = (self.up_strong_x, self.up_strong_y, 0, 0, self.up_strong_hitstun,
                                     self.up_strong_dmg, self.up_strong_base,
                                     self.up_strong_scale + (self.charge_boost_us * self.num_rotations))
            else:
                attack_attributes = (-1 * self.up_strong_x, self.up_strong_y, 0, 0, self.up_strong_hitstun,
                                     self.up_strong_dmg, self.up_strong_base,
                                     self.up_strong_scale + (self.charge_boost_us * self.num_rotations))

        elif self.num_active_ds > 0:
            attack_attributes = (
                self.down_strong_x, self.down_strong_y, -1 * self.down_strong_x, self.down_strong_y,
                self.down_strong_hitstun, self.down_strong_dmg, self.down_strong_base,
                self.down_strong_scale + (self.charge_boost_ds * self.num_rotations))

        elif self.num_active_fs > 0:
            if self.direction:
                attack_attributes = (
                    self.f_strong_x, self.f_strong_y, 0, 0, self.f_strong_hitstun, self.f_strong_dmg,
                    self.f_strong_base,
                    self.f_strong_scale + (self.charge_boost_fs * self.num_rotations))
            else:
                attack_attributes = (
                    -1 * self.f_strong_x, self.f_strong_y, 0, 0, self.f_strong_hitstun, self.f_strong_dmg,
                    self.f_strong_base,
                    self.f_strong_scale + (self.charge_boost_fs * self.num_rotations))

        elif self.num_active_flash > 0:
            attack_attributes = (
                self.flash_x, self.flash_y, -1 * self.flash_x,
                self.flash_y, self.flash_hitstun, self.flash_dmg, self.flash_base,
                self.flash_scale)

        elif self.projectile_active > 0:
            attack_attributes = (
                self.neutral_b_x, self.neutral_b_y, 0, 0, self.neutral_b_hitstun, self.neutral_b_dmg,
                self.neutral_b_base, self.neutral_b_scale)
        elif self.projectile_active_left > 0:
            attack_attributes = (
                -1 * self.neutral_b_x, self.neutral_b_y, 0, 0, self.neutral_b_hitstun, self.neutral_b_dmg,
                self.neutral_b_base, self.neutral_b_scale)
        elif self.num_active_ss > 0:
            if self.direction:
                attack_attributes = (
                    self.side_special_x, self.side_special_y, 0, 0, self.side_special_hitstun, self.side_special_dmg,
                    self.side_special_base, self.side_special_scale)
            else:
                attack_attributes = (
                    -1 * self.side_special_x, self.side_special_y, 0, 0, self.side_special_hitstun,
                    self.side_special_dmg,
                    self.side_special_base, self.side_special_scale)

        elif self.num_active_ub1 > 0:
            if self.direction:
                attack_attributes = (
                    self.up_special_x1, self.up_special_y1, 0, 0, self.up_special_hitstun1,
                    self.up_special_dmg1,
                    self.up_special_base1, self.up_special_scale1)
            else:
                attack_attributes = (
                    -1 * self.up_special_x1, self.up_special_y1, 0, 0, self.up_special_hitstun1,
                    self.up_special_dmg1,
                    self.up_special_base1, self.up_special_scale1)

        elif self.num_active_ub2 > 0:
            if self.direction:
                attack_attributes = (
                    self.up_special_x2, self.up_special_y2, 0, 0, self.up_special_hitstun2,
                    self.up_special_dmg2,
                    self.up_special_base2, self.up_special_scale2)
            else:
                attack_attributes = (
                    -1 * self.up_special_x2, self.up_special_y2, 0, 0, self.up_special_hitstun2,
                    self.up_special_dmg2,
                    self.up_special_base2, self.up_special_scale2)

        elif self.num_active_dsg > 0:
            if self.direction:
                attack_attributes = (
                    self.down_special_ground_x, self.down_special_ground_y, 0, 0, self.down_special_ground_hitstun,
                    self.down_special_ground_dmg,
                    self.down_special_ground_base, self.down_special_ground_scale)
            else:
                attack_attributes = (
                    -1 * self.down_special_ground_x, self.down_special_ground_y, 0, 0, self.down_special_ground_hitstun,
                    self.down_special_ground_dmg,
                    self.down_special_ground_base, self.down_special_ground_scale)

        elif self.num_active_dsa > 0:
            if self.direction:
                attack_attributes = (
                    self.down_special_air_x, self.down_special_air_y, 0, 0, self.down_special_air_hitstun,
                    self.down_special_air_dmg,
                    self.down_special_air_base, self.down_special_air_scale)
            else:
                attack_attributes = (
                    -1 * self.down_special_air_x, self.down_special_air_y, 0, 0, self.down_special_air_hitstun,
                    self.down_special_air_dmg,
                    self.down_special_air_base, self.down_special_air_scale)

        return attack_attributes

    def getHit(self, player, other_player, player_shield, other_player_2, other_player_proj, hitstop=0):
        hits = pygame.sprite.spritecollide(player, other_player, False)
        hits2 = pygame.sprite.spritecollide(player_shield, other_player, False)
        hits3 = pygame.sprite.spritecollide(player, other_player_2, False)
        hits4 = pygame.sprite.spritecollide(player_shield, other_player_2, False)
        hits5 = pygame.sprite.spritecollide(player, other_player_proj, False)
        hits6 = pygame.sprite.spritecollide(player_shield, other_player_proj, False)
        if (hits or hits3 or hits5) and not (hits2 or hits4 or hits6) and self.invincibility_frames <= 0:
            self.take_knockback = True
            if hits:
                self.hitbox_1 = True
                self.hitbox_2 = False
            elif hits3:
                self.hitbox_1 = False
                self.hitbox_2 = True
            else:
                self.hitbox_1 = False
                self.hitbox_2 = False
        else:
            self.take_knockback = False

        if hits2 or hits4:
            self.shieldstun = hitstop

    def hit_opponent(self, opponent, opponent_shield, hitbox_1, hitbox_2, opponent_invincibility, hitbox_proj):
        hits = pygame.sprite.spritecollide(opponent, hitbox_1, False)
        hits2 = pygame.sprite.spritecollide(opponent, hitbox_2, False)
        hits5 = pygame.sprite.spritecollide(opponent, hitbox_proj, False)
        hits3 = pygame.sprite.spritecollide(opponent_shield, hitbox_1, False)
        hits4 = pygame.sprite.spritecollide(opponent_shield, hitbox_2, False)
        hits6 = pygame.sprite.spritecollide(opponent_shield, hitbox_proj, False)

        if (hits or hits2 or hits5) and not (hits3 or hits4 or hits6) and opponent_invincibility == 0:
            # HIT (Not shield) (Do Hitstop, hitstop)
            self.hitstop_counter += 1

            if self.num_active_ub1 > 0:
                self.up_special_hit = 30

            if self.projectile_active > 0:
                self.projectile_active = 0
                self.proj_image = None
            elif self.projectile_active_left > 0:
                self.projectile_active_left = 0
                self.proj_image = None

            if self.hitstop_counter == 1:
                self.prev_vel_x = self.vel.x
                self.prev_vel_y = self.vel.y
                self.sfxObj.stop()
                self.sfxObj.play()
                if self.flash_percent <= 100 - self.current_attack_attributes:
                    self.flash_percent += self.current_attack_attributes
                else:
                    self.flash_percent = 100
            if self.in_hitstop > 0:
                self.vel.x = 0
                self.vel.y = 0
            else:
                self.vel.x = self.prev_vel_x
                self.vel.y = self.prev_vel_y

            self.hit = True

        elif hits3 or hits4 or hits6:
            self.shieldSFX.play()

            if self.projectile_active > 0:
                self.projectile_active = 0
                self.proj_image = None
            elif self.projectile_active_left > 0:
                self.projectile_active_left = 0
                self.proj_image = None

            self.hitstop_counter += 1
            if self.hitstop_counter == 1:
                self.in_hitstop = 5
                if self.flash_percent <= 100 - self.current_attack_attributes * 0.5:
                    self.flash_percent += self.current_attack_attributes * 0.5
                else:
                    self.flash_percent = 100
            self.hit = True

        elif not (self.take_knockback or self.knockback_frames > 0):
            self.hitstop_counter = 0
            self.hit = False
