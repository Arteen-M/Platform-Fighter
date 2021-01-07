import pygame
import math
# import time
# import os

vec = pygame.math.Vector2
pygame.mixer.init()

HEIGHT = 600  # STAGE HEIGHT
WIDTH = 800  # STAGE WIDTH
ACC = 0.5  # ACCELERATION (REMOVE MAYBE?)
FRIC = -0.12  # FRICTION (DECELERATION)


class PlayerStickman(pygame.sprite.Sprite):
    def __init__(self, colour, numPlayer, show_hitbox=False, stockNum=3):
        super().__init__()
        self.colour = colour  # HURTBOX COLOUR (TESTING ONLY)
        self.surf = pygame.image.load(  # FIRST INSTANCE OF PLAYER IMAGE
            "Stickman Character/Walk cycle/stick_char_run_60fps-1.png")
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
        self.fall_speed = 3.2  # Fall Speed
        self.fast_fall = 5.12  # 60% Increase
        self.groundACC = 0.6  # GROUNDED ACCELERATION
        self.airACC = 0.45  # AIR ACCELERATION
        self.show_hitbox = show_hitbox

        # SET PLAYER JUMPSQUAT
        self.jumpsquat_right = [
            "../PlatformFighter/Stickman Character/Jump Squat Frames/stick_char_jump-1.png",
            "../PlatformFighter/Stickman Character/Jump Squat Frames/stick_char_jump-2.png",
            "../PlatformFighter/Stickman Character/Jump Squat Frames/stick_char_jump-3.png"]
        self.jumpsquat_left = [
            "../PlatformFighter/Stickman Character/Jump Squat Frames/stick_char_jump_reverse-1.png",
            "../PlatformFighter/Stickman Character/Jump Squat Frames/stick_char_jump_reverse-2.png",
            "../PlatformFighter/Stickman Character/Jump Squat Frames/stick_char_jump_reverse-3.png"]
        self.in_jumpsquat = 0

        self.hitstunLeft = "../PlatformFighter/Stickman Character/Hitstun/stick_char_hitstun-1.png"
        self.hitstunRight = "../PlatformFighter/Stickman Character/Hitstun/stick_char_hitstun_clone-1.png"

        # AERIAL DRIFT ANIMATION
        self.jump_left = "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-4.png"
        self.jump_right = "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-18.png"
        self.drift_cycle = 0

        # SET PLAYER IDLE CYCLE
        self.idle_cycle = [
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png"]
        self.in_idle_cycle = 0

        self.idle_cycle_left = [
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-7.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-4.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png",
            "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel_clone-1.png"]
        self.in_idle_cycle_left = 0

        # SET PLAYER WALK CYCLE
        self.walk_cycle_right = [
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-1.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-1.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-1.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-1.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-6.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-6.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-6.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-6.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-11.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-11.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-11.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-11.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-18.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-18.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-18.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_60fps-18.png"]
        self.in_walk_cycle_right = 0

        self.walk_cycle_left = [
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-1.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-1.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-1.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-1.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-2.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-2.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-2.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-2.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-3.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-3.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-3.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-3.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-4.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-4.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-4.png",
            "../PlatformFighter/Stickman Character/Walk cycle/stick_char_run_clone-4.png"]
        self.in_walk_cycle_left = 0

        # SET PLAYER CROUCH CYCLE
        self.crouch_right = [
            "../PlatformFighter/Stickman Character/Crouch/stick_char_crouch-1.png",
            "../PlatformFighter/Stickman Character/Crouch/stick_char_crouch-2.png"]
        self.crouch_left = [
            "../PlatformFighter/Stickman Character/Crouch/stick_char_crouch_clone-2.png",
            "../PlatformFighter/Stickman Character/Crouch/stick_char_crouch_clone-3.png"]
        self.crouch_frames = 0

        # SETS PLAYER JAB CYCLE AND ATTRIBUTES
        self.jab_right = [
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-1.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-1.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-1.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-2.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-2.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-2.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-3.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-3.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-3.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-4.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-4.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-4.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-5.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-5.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-5.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-6.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-6.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-6.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-7.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-7.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-7.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-8.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-8.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-8.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-9.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-9.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-9.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-10.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-10.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab-10.png"]
        self.jab_left = [
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-1.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-1.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-1.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-2.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-2.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-2.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-3.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-3.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-3.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-4.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-4.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-4.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-5.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-5.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-5.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-6.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-6.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-6.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-7.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-7.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-7.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-8.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-8.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-8.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-9.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-9.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-9.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-10.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-10.png",
            "../PlatformFighter/Stickman Character/Jab/stick_char_jab_clone-10.png"]
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
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-1.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-1.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-2.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-2.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-3.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-3.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-4.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-4.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-5.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-5.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-6.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-6.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-7.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-7.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-8.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-8.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-9.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-9.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-10.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-10.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-11.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-11.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-12.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-12.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-13.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-13.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-14.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt-14.png"]
        self.in_f_tilt = 0

        # SET PLAYER F-TILT CYCLE (LEFT) + ATTRIBUTES
        self.f_tilt_left = [
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-1.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-1.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-2.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-2.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-3.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-3.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-4.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-4.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-5.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-5.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-6.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-6.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-7.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-7.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-8.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-8.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-9.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-9.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-10.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-10.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-11.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-11.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-12.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-12.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-13.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-13.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-14.png",
            "../PlatformFighter/Stickman Character/Forward Tilt/stick_char_ftilt_clone-14.png"]
        self.in_f_tilt_left = 0

        self.f_tilt_x = math.sin(math.radians(65))
        self.f_tilt_y = math.sin(math.radians(25))
        self.f_tilt_dmg = 12
        self.f_tilt_base = 1.05
        self.f_tilt_scale = 0.14
        self.f_tilt_hitstun = 7

        # SET PLAYER DOWN-TILT CYCLE (RIGHT) + ATTRIBUTES
        self.down_tilt_right = [
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-1.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-1.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-2.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-2.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-3.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-3.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-4.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-4.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-5.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-5.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-6.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt-6.png"]
        self.in_down_tilt_right = 0

        # SET PLAYER DOWN TILT CYCLE (LEFT) + ATTRIBUTES
        self.down_tilt_left = [
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt_reverse-1.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt_reverse-1.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt_reverse-2.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt_reverse-2.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt_reverse-3.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt_reverse-3.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt_reverse-4.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt_reverse-4.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt_reverse-5.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt_reverse-5.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt_reverse-6.png",
            "../PlatformFighter/Stickman Character/Down Tilt/stick_char_dtilt_reverse-6.png"]
        self.in_down_tilt_left = 0

        self.down_tilt_x = math.sin(math.radians(20))
        self.down_tilt_y = math.sin(math.radians(70))
        self.down_tilt_dmg = 3
        self.down_tilt_base = 3
        self.down_tilt_scale = 0.03
        self.down_tilt_hitstun = 7

        # SET PLAYER UP-TILT CYCLE
        self.up_tilt_right = [
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-1.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-1.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-2.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-2.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-3.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-3.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-4.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-4.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-5.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-5.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-6.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-6.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-7.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-7.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-8.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-8.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-9.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-9.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-10.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-10.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-11.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-11.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-12.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-12.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-13.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-13.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-14.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-14.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-15.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-15.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-16.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-16.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-17.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-17.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-18.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt-18.png"]
        self.up_tilt_left = [
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-1.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-1.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-2.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-2.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-3.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-3.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-4.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-4.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-5.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-5.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-6.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-6.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-7.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-7.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-8.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-8.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-9.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-9.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-10.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-10.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-11.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-11.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-12.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-12.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-13.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-13.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-14.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-14.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-15.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-15.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-16.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-16.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-17.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-17.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-18.png",
            "../PlatformFighter/Stickman Character/Up Tilt/stick_char_uptilt_clone-18.png"]
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
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-1.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-2.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-3.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-4.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-5.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-6.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-7.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-8.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-9.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-10.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-11.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-12.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-13.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-14.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-15.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-16.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-17.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair_clone-18.png"]
        self.f_air_left = [
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-1.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-2.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-3.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-4.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-5.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-6.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-7.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-8.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-9.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-10.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-11.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-12.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-13.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-14.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-15.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-16.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-17.png",
            "C:/Users/matee/PycharmProjects/PlatformFighter/Stickman Character/Forward Air/stick_char_fair-18.png"]
        self.in_f_air_right = 0
        self.in_f_air_left = 0

        self.f_air_x = math.sin(math.radians(60))
        self.f_air_y = math.sin(math.radians(30))
        self.f_air_dmg = 9
        self.f_air_base = 2.5
        self.f_air_scale = 0.12
        self.f_air_hitstun = 6

        # SET PLAYER DOWN AIR CYCLE AND ATTRIBUTES
        self.down_air_right = ["../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-1.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-1.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-2.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-2.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-3.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-3.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-4.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-4.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-5.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-5.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-6.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-6.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-7.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-7.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-8.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-8.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-9.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-9.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-10.png",
                               "../PlatformFighter/Stickman Character/Down Air/stick_char_dair_clone-10.png"]
        self.down_air_left = ["../PlatformFighter/Stickman Character/Down Air/stick_char_dair-1.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-1.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-2.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-2.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-3.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-3.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-4.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-4.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-5.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-5.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-6.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-6.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-7.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-7.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-8.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-8.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-9.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-9.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-10.png",
                              "../PlatformFighter/Stickman Character/Down Air/stick_char_dair-10.png"]
        self.in_down_air = 0

        self.down_air_x = 0
        self.down_air_y = -1
        self.down_air_dmg = 15
        self.down_air_base = 3
        self.down_air_scale = 0.17
        self.down_air_hitstun = 5

        # SET PLAYER UP AIR CYCLE AND ATTRIBUTES
        self.up_air_right = ["../PlatformFighter/Stickman Character/Up Air/stick_char_upair-1.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-1.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-2.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-2.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-3.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-3.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-4.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-4.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-5.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-5.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-6.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-6.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-7.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-7.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-8.png",
                             "../PlatformFighter/Stickman Character/Up Air/stick_char_upair-8.png"]
        self.up_air_left = ["../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-1.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-1.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-2.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-2.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-3.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-3.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-4.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-4.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-5.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-5.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-6.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-6.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-7.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-7.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-8.png",
                            "../PlatformFighter/Stickman Character/Up Air/stick_char_upair_clone-8.png"]
        self.in_up_air_right = 0
        self.in_up_air_left = 0

        self.up_air_x = math.sin(math.radians(10))
        self.up_air_y = math.sin(math.radians(80))
        self.up_air_dmg = 8
        self.up_air_base = 0.7
        self.up_air_scale = 0.12
        self.up_air_hitstun = 6

        # SET PLAYER BACK AIR ATTRIBUTES
        self.back_air_left = ["../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-1.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-1.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-2.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-2.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-3.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-3.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-4.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-4.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-5.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-5.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-6.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-6.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-7.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-7.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-8.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-8.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-9.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-9.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-10.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-10.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-11.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-11.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-12.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-12.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-13.png",
                              "../PlatformFighter/Stickman Character/Back Air/stick_char_bair_clone-13.png"]
        self.back_air_right = ["../PlatformFighter/Stickman Character/Back Air/stick_char_bair-1.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-1.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-2.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-2.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-3.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-3.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-4.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-4.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-5.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-5.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-6.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-6.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-7.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-7.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-8.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-8.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-9.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-9.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-10.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-10.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-11.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-11.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-12.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-12.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-13.png",
                               "../PlatformFighter/Stickman Character/Back Air/stick_char_bair-13.png"]
        self.in_back_air_right = 0
        self.in_back_air_left = 0

        self.back_air_x = math.sin(math.radians(75))
        self.back_air_y = math.sin(math.radians(15))
        self.back_air_dmg = 10
        self.back_air_base = 1
        self.back_air_scale = 0.2
        self.back_air_hitstun = 6

        self.num_lag = 0  # SETS LAG (TYPE: STARTUP/ENDLAG)
        self.in_lag = False  # SETS LAG (TYPE: ALL)
        self.num_active = 0  # HITBOX FRAMES (JAB 1/2)
        self.num_active_b = 0
        self.jab_1 = False  # JAB 1 IDENTIFIER
        self.jab_2 = False  # JAB 2 IDENTIFIER
        self.num_active_f = 0  # HITBOX FRAMES (F-TILT LEFT and RIGHt) and (FAIR and BAIR)
        self.num_active_d = 0  # HITBOX FRAMES (DOWN-TILT)
        self.num_active_u = 0  # HITBOX FRAMES (UP-TILT, 1)
        self.num_active_u2 = 0  # HITBOX FRAMES (UP-TILT, 2)
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
        self.opponent_jumps = 0  # SETS NUMBER OF OPPONENT JUMPS (FOR KNOCKBACK ONLY)
        self.is_shielding = False  # SETS SHIELDING VARIABLE
        self.invincibility_frames = 0  # SETS INVINCIBILITY FRAMES

        # SETS ON STAGE VARIABLES
        self.on_stage = False
        self.on_platform = False
        self.on_ground = False

        self.pressing_right = False  # IF PRESSING RIGHT KEY
        self.press_right_frames = 0  # SETS FRAMES AFTER RIGHT PRESS (FOR DASHING ONLY)
        self.pressing_left = False  # IF PRESSING LEFT KEY
        self.press_left_frames = 0  # SAME, BUT FOR LEFT
        self.press_down_frames = 0  # SAME, BUT FOR DOWN
        self.going_down = False  # SETS FAST-FALLING (GOING THROUGH PLATFORMS)

        self.hurt_pos_x = 0  # HURTBOX POSITION (X)
        self.hurt_pos_y = 0  # HURTBOX POSITION (Y)
        # SETS DEFAULT IMAGE
        self.image = "../PlatformFighter/Stickman Character/Idle cycle/stick_char_idel-1.png"
        # SETS IMAGE POSITION
        self.size = (30, 50)

        self.hitbox_1 = False  # HITBOX (1) VARIABLE
        self.hitbox_2 = False  # HITBOX (2) VARIABLE

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
    def shield_size(self, l, h, x, y):
        self.shield_length = l
        self.shield_height = h
        self.shield_pos_x = x
        self.shield_pos_y = y

    def knockback_formula(self, angle):
        velocity = angle * (((((self.percentage / 10) + ((self.percentage * (self.opponent_damage / 2)) / 20)) * (
                (200 / (self.weight + 100)) * 1.4) + 18) * self.knockback_scale) + self.base_knockback)
        return velocity

    # GETTING HIT FUNCTION
    def call_hit(self, component_x, component_y):
        velocityX = self.knockback_formula(component_x)
        velocityY = self.knockback_formula(component_y)
        velocity = math.sqrt(velocityX ** 2 + velocityY ** 2)
        self.numHitstun = round(velocity / (2 * self.gravity) - (2 * velocity) + (0.1 * self.percentage)) + self.minHitstun
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

    # WHEN TO DASH/ WHAT HAPPENS
    def dash(self, press_frames):
        if self.pressing_right:
            neg = 1
        else:
            neg = -1
        if 0 < press_frames <= 6 and not (self.take_momentum or self.in_lag):
            self.vel.x = neg * 11
            press_frames = 7
        else:
            press_frames = 7

        return press_frames

    # WHEN YOU ARE IN ABSOLUTE LAG
    def inLag(self):
        if self.num_lag > 0 or self.numHitstun > 0 or self.platform_hitstun > 0 or self.in_jumpsquat > 0:
            self.in_lag = True
        else:
            self.in_lag = False

    # DI COMPONENT
    def momentumChange(self):
        if self.pressing_left or self.pressing_right:
            if self.numHitstun == 0 and self.take_momentum:
                self.in_momentum += self.groundACC
            else:
                self.in_momentum = 0

    # PUSHBACK ON SHIELD
    def shieldPush(self, shield_dir, opponent_pos):
        if shield_dir == "Right":
            self.vel.x += 0.5
        elif shield_dir == "Left":
            self.vel.x -= 0.5
        elif shield_dir == "Up" or shield_dir == "Down":
            if self.pos.x >= opponent_pos:
                self.vel.x += 0.5
            else:
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

    def findBuffer(self, press_left_key, press_right_key, press_up_key, press_down_key, attack_key, shield_key):
        pressed_keys = pygame.key.get_pressed()
        if self.in_lag:
            if pressed_keys[attack_key]:
                print("Attack")
            elif pressed_keys[shield_key]:
                print("Shield")
            elif pressed_keys[press_left_key]:
                print("Left")
            elif pressed_keys[press_right_key]:
                print("Right")
            elif pressed_keys[press_up_key] and self.in_jumpsquat <= 0:
                print("Up")
            elif pressed_keys[press_down_key]:
                print("Down")
        # else:
        #    print("0")

    # MOVING/ MOVEMENT FUNCTION (PLACE ALL MOVEMENT RELATED THINGS HERE)
    def move(self, player_key_left, player_key_right, player_key_down):
        self.acc = vec(0, self.gravity)  # GRAVITY
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[
            player_key_left] and self.on_ground and self.platform_hitstun == 0 and not self.is_shielding and self.num_lag <= 0 and self.crouch_frames == 0 and self.in_jumpsquat == 0:
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

                self.press_left_frames = self.dash(self.press_left_frames)  # AWAITS DASH COMMAND

        elif pressed_keys[player_key_left] and not self.on_ground and self.platform_hitstun == 0:  # AIRBORNE MOVEMENT

            self.acc.x -= self.airACC  # AIR MOVEMENT

            self.in_walk_cycle_left = 0  # ENDS WALK CYCLE

            self.pressing_left = True  # PRESSING LEFT IS ALWAYS TRUE HERE

            self.press_left_frames = self.dash(self.press_left_frames)  # AWAITS DASH COMMAND

        else:
            self.pressing_left = False  # IF YOU'RE NOT PRESSING LEFT
            self.in_walk_cycle_left = 0  # END WALK CYCLE (MAYBE START IDLE CYCLE? IDLE CYCLE DEPENDANT ON PRESS OR ON ANIMATION)
            # LOWERS PRESS FRAMES
            if self.press_left_frames > 0:
                self.press_left_frames -= 1

        if pressed_keys[
            player_key_right] and self.on_ground and self.platform_hitstun == 0 and not self.is_shielding and self.num_lag == 0 and self.crouch_frames == 0 and self.in_jumpsquat == 0:
            # WHEN YOU CAN MOVE RIGHT
            # self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))

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

                self.press_right_frames = self.dash(self.press_right_frames)  # AWAITS DASH COMMAND

        elif pressed_keys[player_key_right] and not self.on_ground and self.platform_hitstun == 0:  # AIRBORNE MOVEMENT
            self.acc.x += self.airACC  # AIR MOVEMENT
            self.in_walk_cycle_right = 0  # ENDS WALK CYCLE WHEN AIRBORNE

            self.pressing_right = True  # PRESSING RIGHT IS ALWAYS TRUE HERE

            self.press_right_frames = self.dash(self.press_right_frames)  # AWAITS DASH COMMAND

        else:
            self.pressing_right = False  # IF YOU'RE NOT PRESSING LEFT
            self.in_walk_cycle_right = 0  # END WALK CYCLE
            # LOWERS PRESS FRAMES
            if self.press_right_frames > 0:
                self.press_right_frames -= 1

        if pressed_keys[
            player_key_down] and self.numHitstun == 0 and self.platform_hitstun == 0 and (
                self.num_lag == 0 or not self.on_ground) and self.in_jumpsquat == 0:
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
        self.acc.x += self.vel.x * FRIC
        self.vel.x += self.acc.x
        if self.vel.y <= self.fall_speed:
            self.vel.y += self.acc.y
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

    def jump(self):
        self.going_down = False
        self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))

        if not (self.in_lag or self.is_shielding) and self.crouch_frames == 0:  # CANNOT JUMP IN THESE TWO CASES
            self.take_momentum = False
            if self.on_ground:
                self.in_jumpsquat = len(self.jumpsquat_left)  # START JUMPSQUAT
            elif self.jumps > 0:  # OTHERWISE, FRAME 1 JUMP (CHANGE WHEN AERIAL JUMPS HAVE ANIMATIONS)
                self.vel.y = -4.8
                self.jumps -= 1

    def update(self, player, attack_angle_p_1, tops_1, sides_left_1, sides_right_1, platforms, under_platforms, jumps,
               shield_dir, other_shield, opponent_pos):
        hitsGround = pygame.sprite.spritecollide(player, tops_1, False)
        hitsSideLeft = pygame.sprite.spritecollide(player, sides_left_1, False)
        hitsSideRight = pygame.sprite.spritecollide(player, sides_right_1, False)
        hitsPlatform = pygame.sprite.spritecollide(player, platforms, False)
        hitsUnderPlat = pygame.sprite.spritecollide(player, under_platforms, False)
        hitsShield = pygame.sprite.spritecollide(player, other_shield, False)

        self.call_respawn()
        self.inLag()
        self.momentumChange()
        self.groundCheck()
        self.invincibleState()
        self.platformHitstun()
        self.hitstunState()
        self.determineEnd()
        self.lowerNumLag()
        self.opponent_jumps = jumps

        if hitsGround:
            self.on_stage = True
            self.pos.y = hitsGround[0].rect.top + 1
            self.vel.y = 0
            self.take_momentum = False
            self.knockback_frames = 0
            self.jumps = 5
            self.going_down = False
        else:
            self.on_stage = False

        if hitsSideLeft and not hitsGround:
            self.pos.x = hitsSideLeft[0].rect.left - 15
            self.vel.x = 0

        if hitsSideRight and not hitsGround:
            self.pos.x = hitsSideRight[0].rect.right + 15
            self.vel.x = 0

        if hitsPlatform and self.vel.y >= 0 and not self.going_down and not hitsUnderPlat:
            self.on_platform = True
            self.pos.y = hitsPlatform[0].rect.top + 1
            self.vel.y = 0
            self.jumps = 5
            self.take_momentum = False
            self.knockback_frames = 0
        else:
            self.on_platform = False

        if hitsShield:
            self.shieldPush(shield_dir, opponent_pos)

        # JUMPSQUAT ANIMATION PLAY
        if self.in_jumpsquat > 0:
            self.in_jumpsquat -= 1

            if self.in_jumpsquat == 0:
                self.on_ground = False
                self.vel.y = -4.8

        # ATTACKING ANIMATIONS PLAY
        if self.in_f_tilt > 0 or self.in_f_tilt_left > 0:

            if self.in_f_tilt > 0:  # ACTIVATE F-TILT RIGHT
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

            self.in_up_tilt -= 1  # LOWER ANIMATION FRAMES

            if self.in_up_tilt == 17:  # HITBOX FLAG 1
                self.num_active_u = 10  # TOTAL ACTIVE FRAMES (1)

            if self.in_up_tilt == 25:  # HITBOX FLAG 2
                self.num_active_u2 = 4  # TOTAL ACTIVE FRAMES (2)

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
                self.in_jab_right -= 1

                if self.in_jab_right == 20:
                    self.num_active = 6
                    self.jab_1 = True
                elif self.in_jab_right == 9:
                    self.num_active = 6
                    self.jab_2 = True
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
                self.in_jab_left -= 1

                if self.in_jab_left == 20:
                    self.num_active = 6
                    self.jab_1 = True
                elif self.in_jab_left == 9:
                    self.num_active = 6
                    self.jab_2 = True
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
            if self.in_f_air_right > 0:
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
                    # self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))

            elif self.in_f_air_left > 0:
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
                    # self.hurtbox_size_alteration((30, 50), (self.pos.x, self.pos.y - 27))

        elif self.in_down_air > 0:
            if self.direction:
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
            if self.in_up_air_right > 0:
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
            if self.in_back_air_right > 0:
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

            if self.take_knockback:
                self.call_hit(component_x, -1 * component_y)
                self.take_knockback = False

            if self.knockback_frames == self.total_knockback:
                self.knockback_num_x = self.knockback_formula(component_x)
                self.knockback_num_y = self.knockback_formula((-1 * component_y))

            if self.knockback_frames == (self.total_knockback - 1):
                self.percentage += self.opponent_damage

            self.vel.x = self.knockback_num_x
            self.vel.y = self.knockback_num_y  # + (self.gravity * (self.total_knockback - self.knockback_frames))

            self.hitbox_alteration(1, 0, 0, 0, 0)
            self.hitbox_alteration(2, 0, 0, 0, 0)

            self.knockback_frames -= 1
            self.take_momentum = True

        if self.take_momentum and self.knockback_frames == 0:
            # self.vel.x = self.knockback_num_x
            if self.vel.x < 0:
                self.vel.x -= 0.2
            elif self.vel.x > 0:
                self.vel.x += 0.2

            if abs(self.in_momentum) >= abs(self.vel.x) / 2:
                self.take_momentum = False

        # END OF KNOCKBACK SYSTEM

        # ANIMATION PRIORITY
        # HITSTUN
        if self.numHitstun > 0:
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
        # SPECIAL ATTACKS
        # SMASH ATTACKS
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

        # if self.crouch_frames > 0 and not self.in_lag:
        #   if self.direction:
        #      self.hurtbox_alteration(self.crouch_right[(len(self.crouch_right) - 1) - self.crouch_frames],
        #                             (self.pos.x, self.pos.y - 50))
        # else:
        #   self.hurtbox_alteration(self.crouch_left[(len(self.crouch_left) - 1) - self.crouch_frames],
        #                          (self.pos.x, self.pos.y - 50))
        # self.hurtbox_size_alteration((30, 40), (self.pos.x, self.pos.y - 22))

        # self.hurtbox_alteration(self.image, (self.pos.x, self.pos.y - 50))
        # self.hurtbox_size_alteration(self.size, (self.pos.x, self.pos.y - 27 + ((50 - self.size[1]) / 2)))

    def attack(self, attack_key, left_key, right_key, up_key, down_key):
        pressed_keys = pygame.key.get_pressed()
        pressed_keys_2 = pygame.key.get_pressed()

        if pressed_keys[attack_key] and (pressed_keys_2[left_key] or pressed_keys_2[right_key]) and not (
                self.in_lag or self.is_shielding):
            if pressed_keys_2[right_key]:
                if self.on_ground:
                    self.num_lag = len(self.f_tilt_right)
                    self.in_f_tilt = len(self.f_tilt_right)
                elif not self.on_ground and self.direction:
                    self.num_lag = len(self.f_air_right)
                    self.in_f_air_right = len(self.f_air_right)
                elif not self.on_ground and not self.direction:
                    self.num_lag = len(self.back_air_left)
                    self.in_back_air_left = len(self.back_air_left)
            elif pressed_keys_2[left_key]:
                if self.on_ground:
                    self.num_lag = len(self.f_tilt_left)
                    self.in_f_tilt_left = len(self.f_tilt_left)
                elif not self.on_ground and not self.direction:
                    self.num_lag = len(self.f_air_left)
                    self.in_f_air_left = len(self.f_air_left)
                elif not self.on_ground and self.direction:
                    self.num_lag = len(self.back_air_right)
                    self.in_back_air_right = len(self.back_air_right)
        elif pressed_keys[attack_key] and pressed_keys_2[up_key] and not (self.in_lag or self.is_shielding):
            if self.on_ground:
                self.num_lag = len(self.up_tilt_right)
                self.in_up_tilt = len(self.up_tilt_right)
            else:
                self.num_lag = len(self.up_air_right)
                if self.direction:
                    self.in_up_air_right = len(self.up_air_right)
                else:
                    self.in_up_air_left = len(self.up_air_left)
        elif pressed_keys[attack_key] and pressed_keys_2[down_key] and not (self.in_lag or self.is_shielding):
            if self.on_ground:
                self.num_lag = len(self.down_tilt_right) + 1
                if self.direction:
                    self.in_down_tilt_right = len(self.down_tilt_right)
                else:
                    self.in_down_tilt_left = len(self.down_tilt_left)
            elif not self.on_ground:
                self.num_lag = len(self.down_air_right)
                self.in_down_air = len(self.down_air_right)

        elif pressed_keys[attack_key] and not (self.in_lag or self.is_shielding):
            if self.on_ground:
                self.num_lag = len(self.jab_right)
                if self.direction:
                    self.in_jab_right = len(self.jab_right)
                else:
                    self.in_jab_left = len(self.jab_left)
            # else:
            # NEUTRAL AIR ACTIVATION

    def shielding(self, shield_key, left_key, right_key, up_key, down_key):
        pressed_keys = pygame.key.get_pressed()
        pressed_keys_2 = pygame.key.get_pressed()
        shield_direction = None

        if pressed_keys[
            shield_key] and self.on_ground and self.numHitstun == 0 and self.num_active == 0 and self.num_active_f == 0 and self.num_active_d == 0 and self.num_active_u == 0:
            self.is_shielding = True
            if pressed_keys_2[left_key]:
                self.shield_size(15, 65, self.pos.x - 25, self.pos.y - 30)
                self.vel.x = 0
                self.direction = False
                shield_direction = "Left"
            elif pressed_keys_2[right_key]:
                self.shield_size(15, 65, self.pos.x + 25, self.pos.y - 30)
                self.vel.x = 0
                self.direction = True
                shield_direction = "Right"
            elif pressed_keys_2[up_key]:
                self.shield_size(65, 15, self.pos.x, self.pos.y - 60)
                self.vel.x = 0
                shield_direction = "Up"
            elif pressed_keys_2[down_key]:
                self.shield_size(65, 15, self.pos.x, self.pos.y + 15)
                self.vel.x = 0
                shield_direction = "Down"
            else:
                if self.direction:
                    self.shield_size(15, 65, self.pos.x + 25, self.pos.y - 30)
                    self.vel.x = 0
                    shield_direction = "Right"
                else:
                    self.shield_size(15, 65, self.pos.x - 25, self.pos.y - 30)
                    self.vel.x = 0
                    shield_direction = "Left"
        else:
            self.is_shielding = False
            self.shield_length = 0
            self.shield_height = 0
            self.shield_pos_x = 0
            self.shield_pos_y = 0

        return shield_direction

    def createHit(self, activity_11, activity_22):
        if self.num_active > 0 or self.num_active_d > 0 or self.num_active_f > 0 or self.num_active_u > 0 or self.num_active_u2 > 0 or self.num_active_b > 0:
            if self.numPlayer == 1:
                activity_11 = True
                return activity_11
            elif self.numPlayer == 2:
                activity_22 = True
                return activity_22
        else:
            activity_11 = False
            activity_22 = False

        if self.numPlayer == 1:
            return activity_11
        elif self.numPlayer == 2:
            return activity_22

    def get_angle(self, attack_attributes_1, attack_attributes_2):
        # ATTACK ATTRIBUTES (or ATTACK_ANGLE_P_1) FORMAT:
        # (X_COMPONENT (1), Y_COMPONENT(1), X_COMPONENT(2), Y_COMPONENT(2), ATTACK_DAMAGE, BASE_KNOCKBACK, KNOCKBACK_SCALING)
        if self.num_active > 0:
            if self.numPlayer == 1:
                if self.direction:
                    if self.jab_1:
                        attack_attributes_1 = (
                            self.jab_1_x, self.jab_1_y, 0, 0, self.jab_1_hitstun, self.jab_1_dmg, self.jab_1_base, self.jab_1_scale)
                    elif self.jab_2:
                        attack_attributes_1 = (
                            self.jab_2_x, self.jab_2_y, 0, 0, self.jab_2_hitstun, self.jab_2_dmg, self.jab_2_base, self.jab_2_scale)
                else:
                    if self.jab_1:
                        attack_attributes_1 = (
                            -1 * self.jab_1_x, self.jab_1_y, 0, 0, self.jab_1_hitstun, self.jab_1_dmg, self.jab_1_base, self.jab_1_scale)
                    elif self.jab_2:
                        attack_attributes_1 = (
                            -1 * self.jab_2_x, self.jab_2_y, 0, 0, self.jab_2_hitstun, self.jab_2_dmg, self.jab_2_base, self.jab_2_scale)
            else:
                if self.direction:
                    if self.jab_1:
                        attack_attributes_2 = (
                            self.jab_1_x, self.jab_1_y, 0, 0, self.jab_1_hitstun, self.jab_1_dmg, self.jab_1_base, self.jab_1_scale)
                    elif self.jab_2:
                        attack_attributes_2 = (
                            self.jab_2_x, self.jab_2_y, 0, 0, self.jab_2_hitstun, self.jab_2_dmg, self.jab_2_base, self.jab_2_scale)
                else:
                    if self.jab_1:
                        attack_attributes_2 = (
                            -1 * self.jab_1_x, self.jab_1_y, 0, 0, self.jab_1_hitstun, self.jab_1_dmg, self.jab_1_base, self.jab_1_scale)
                    elif self.jab_2:
                        attack_attributes_2 = (
                            -1 * self.jab_2_x, self.jab_2_y, 0, 0, self.jab_2_hitstun, self.jab_2_dmg, self.jab_2_base, self.jab_2_scale)
        elif self.num_active_f > 0:
            if self.on_ground:
                if self.direction:
                    if self.numPlayer == 1:
                        attack_attributes_1 = (
                            self.f_tilt_x, self.f_tilt_y, 0, 0, self.f_tilt_hitstun, self.f_tilt_dmg, self.f_tilt_base, self.f_tilt_scale)
                    else:
                        attack_attributes_2 = (
                            self.f_tilt_x, self.f_tilt_y, 0, 0, self.f_tilt_hitstun, self.f_tilt_dmg, self.f_tilt_base, self.f_tilt_scale)
                else:
                    if self.numPlayer == 1:
                        attack_attributes_1 = (
                            -1 * self.f_tilt_x, self.f_tilt_y, 0, 0, self.f_tilt_hitstun, self.f_tilt_dmg, self.f_tilt_base,
                            self.f_tilt_scale)
                    else:
                        attack_attributes_2 = (
                            -1 * self.f_tilt_x, self.f_tilt_y, 0, 0, self.f_tilt_hitstun, self.f_tilt_dmg, self.f_tilt_base,
                            self.f_tilt_scale)
            else:
                if self.direction:
                    if self.numPlayer == 1:
                        attack_attributes_1 = (
                            self.f_air_x, self.f_air_y, 0, 0, self.f_air_hitstun, self.f_air_dmg, self.f_air_base, self.f_air_scale)
                    else:
                        attack_attributes_2 = (
                            self.f_air_x, self.f_air_y, 0, 0, self.f_air_hitstun, self.f_air_dmg, self.f_air_base, self.f_air_scale)
                else:
                    if self.numPlayer == 1:
                        attack_attributes_1 = (
                            -1 * self.f_air_x, self.f_air_y, 0, 0, self.f_air_hitstun, self.f_air_dmg, self.f_air_base, self.f_air_scale)
                    else:
                        attack_attributes_2 = (
                            -1 * self.f_air_x, self.f_air_y, 0, 0, self.f_air_hitstun, self.f_air_dmg, self.f_air_base, self.f_air_scale)
        elif self.num_active_b > 0:
            if self.direction:
                if self.numPlayer == 1:
                    attack_attributes_1 = (
                        -1 * self.back_air_x, self.back_air_y, 0, 0, self.back_air_hitstun, self.back_air_dmg, self.back_air_base,
                        self.back_air_scale)
                else:
                    attack_attributes_2 = (
                        -1 * self.back_air_x, self.back_air_y, 0, 0, self.back_air_hitstun, self.back_air_dmg, self.back_air_base,
                        self.back_air_scale)
            else:
                if self.numPlayer == 1:
                    attack_attributes_1 = (
                        self.back_air_x, self.back_air_y, 0, 0, self.back_air_hitstun, self.back_air_dmg, self.back_air_base,
                        self.back_air_scale)
                else:
                    attack_attributes_2 = (
                        self.back_air_x, self.back_air_y, 0, 0, self.back_air_hitstun, self.back_air_dmg, self.back_air_base,
                        self.back_air_scale)
        elif self.num_active_u > 0:
            if self.on_ground:
                if self.numPlayer == 1:
                    attack_attributes_1 = (
                        self.up_tilt2_x, self.up_tilt2_y, 0, 0, self.up_tilt2_hitstun, self.up_tilt2_dmg, self.up_tilt2_base,
                        self.up_tilt2_scale)
                else:
                    attack_attributes_2 = (
                        self.up_tilt2_x, self.up_tilt2_y, 0, 0, self.up_tilt2_hitstun, self.up_tilt2_dmg, self.up_tilt2_base,
                        self.up_tilt2_scale)
            else:
                if self.direction:
                    if self.numPlayer == 1:
                        attack_attributes_1 = (
                            self.up_air_x, self.up_air_y, 0, 0, self.up_air_hitstun, self.up_air_dmg, self.up_air_base, self.up_air_scale)
                    else:
                        attack_attributes_2 = (
                            self.up_air_x, self.up_air_y, 0, 0, self.up_air_hitstun, self.up_air_dmg, self.up_air_base, self.up_air_scale)
                else:
                    if self.numPlayer == 1:
                        attack_attributes_1 = (
                            -1 * self.up_air_x, self.up_air_y, 0, 0, self.up_air_hitstun, self.up_air_dmg, self.up_air_base,
                            self.up_air_scale)
                    else:
                        attack_attributes_2 = (
                            -1 * self.up_air_x, self.up_air_y, 0, 0, self.up_air_hitstun, self.up_air_dmg, self.up_air_base,
                            self.up_air_scale)

        elif self.num_active_u2 > 0:
            if self.on_ground:
                if self.numPlayer == 1:
                    attack_attributes_1 = (
                        -1 * self.up_tilt1_x, self.up_tilt1_y, self.up_tilt1_x,
                        self.up_tilt1_y, self.up_tilt1_hitstun, self.up_tilt1_dmg, self.up_tilt1_base, self.up_tilt1_scale)
                else:
                    attack_attributes_2 = (
                        -1 * self.up_tilt1_x, self.up_tilt1_y, self.up_tilt1_x,
                        self.up_tilt1_y, self.up_tilt1_hitstun, self.up_tilt1_dmg, self.up_tilt1_base, self.up_tilt1_scale)

        elif self.num_active_d > 0:
            if self.on_ground:
                if self.numPlayer == 1:
                    if self.direction:
                        attack_attributes_1 = (
                            self.down_tilt_x, self.down_tilt_y, 0, 0, self.down_tilt_hitstun, self.down_tilt_dmg, self.down_tilt_base,
                            self.down_tilt_scale)
                    else:
                        attack_attributes_1 = (
                            -1 * self.down_tilt_x, self.down_tilt_y, 0, 0, self.down_tilt_hitstun, self.down_tilt_dmg, self.down_tilt_base,
                            self.down_tilt_scale)
                else:
                    if self.direction:
                        attack_attributes_2 = (
                            self.down_tilt_x, self.down_tilt_y, 0, 0, self.down_tilt_hitstun, self.down_tilt_dmg, self.down_tilt_base,
                            self.down_tilt_scale)
                    else:
                        attack_attributes_2 = (
                            -1 * self.down_tilt_x, self.down_tilt_y, 0, 0, self.down_tilt_hitstun, self.down_tilt_dmg, self.down_tilt_base,
                            self.down_tilt_scale)
            else:
                if self.numPlayer == 1:
                    attack_attributes_1 = (
                        self.down_air_x, self.down_air_y, 0, 0, self.down_air_hitstun, self.down_air_dmg, self.down_air_base,
                        self.down_air_scale)
                else:
                    attack_attributes_2 = (
                        self.down_air_x, self.down_air_y, 0, 0, self.down_air_hitstun, self.down_air_dmg, self.down_air_base,
                        self.down_air_scale)

        if self.numPlayer == 1:
            return attack_attributes_1
        else:
            return attack_attributes_2

    def getHit(self, player, other_player, activity_11, activity_22, player_shield, other_player_2):
        hits = pygame.sprite.spritecollide(player, other_player, False)
        hits2 = pygame.sprite.spritecollide(player_shield, other_player, False)
        hits3 = pygame.sprite.spritecollide(player, other_player_2, False)
        if activity_11 and (hits or hits3) and self.numPlayer == 2 and not hits2 and self.invincibility_frames <= 0:
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

        elif activity_22 and (hits or hits3) and self.numPlayer == 1 and not hits2 and self.invincibility_frames <= 0:
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

