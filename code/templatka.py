#!/usr/bin/python
# -*- coding: utf-8 -*-

from psychopy import visual, event, core
import multiprocessing as mp
import pandas as pd
import filterlib as flt
import blink as blk
import pygame
import sys
import random


from pyOpenBCI import OpenBCIGanglion

def blinks_detector(
    quit_program,
    blink_det,
    blinks_num,
    blink,
    ):

    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)

        brt.blink_detect(smp_flted, -38000)
        if brt.new_blink:
            if brt.blinks_num == 1:

                # connected.set()

                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()

####################################################

    SYMULACJA_SYGNALU = True

####################################################

    mac_adress = 'd2:b4:11:81:48:ad'

####################################################

    clock = pygame.time.Clock()
    frt = flt.FltRealTime()
    brt = blk.BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv('dane_do_symulacji/data.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)


if __name__ == '__main__':

    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)

    # connected = mp.Event()

    quit_program = mp.Event()

    proc_blink_det = mp.Process(name='proc_', target=blinks_detector,
                                args=(quit_program, blink_det,
                                blinks_num, blink))

    proc_blink_det.start()
    print('subprocess started')

    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()

    screen_width = 1300
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption('First Game')
    pygame.mixer.music.load('pigula.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    font1 = pygame.font.SysFont('comicsansms', 180)
    clock = pygame.time.Clock()
    walk_right = [pygame.image.load('karoR.png')]
    walk_left = [pygame.image.load('karoL.png')]
    walk_up = [pygame.image.load('karoU.png')]
    walk_down = [pygame.image.load('karoD.png')]
    background = pygame.image.load('bgca.jpg')
    char = pygame.image.load('karoR.png')


    class Hero:

        def __init__(self):
            self.x = 300
            self.y = 500
            self.object_width = 100
            self.object_height = 167
            self.vel_x = 0
            self.vel_y = 0
            self.left = False
            self.right = False
            self.up = False
            self.down = False
            self.score = 0
            self.direction = 0
            self.blink = 0
            self.end = 0

        def draw_hero(self, screen):
            screen.blit(background, (0, 0))
            text = font.render('Score: ' + str(self.score), 1, (0, 255, 0))
            screen.blit(text, (screen_width - 120, 10))

            if self.left:
                screen.blit(walk_left[0], (self.x, self.y))
            elif self.right:

                screen.blit(walk_right[0], (self.x, self.y))
            elif self.up:

                screen.blit(walk_up[0], (self.x, self.y))
            elif self.down:

                screen.blit(walk_down[0], (self.x, self.y))

            pygame.display.update()


    class Point:

        def __init__(self, screen):
            self.screen = screen
            self.width = 15
            self.height = 15
            self.x = random.randint(0, screen_width - 3 * self.width)
            self.y = random.randint(0, screen_height - 3 * self.height)
            self.hitbox = (self.x, self.y, self.width, self.height)

        def draw_point(self):
            pygame.draw_hero.circle(self.screen, (255, 255, 10),
                                    (self.x, self.y), self.width,
                                    self.height)
            pygame.display.update()

    class Super_Point:

        def __init__(self, screen):
            self.screen = screen
            self.width = 20
            self.height = 20
            self.x = random.randint(0, screen_width - 3 * self.width)
            self.y = random.randint(0, screen_height - 3 * self.height)
            self.hitbox = (self.x, self.y, self.width, self.height)

        def draw_super_point(self):
            pygame.draw_hero.circle(self.screen, (255, 0, 0), (self.x,
                                    self.y), self.width, self.height)
            pygame.display.update()


    class End:

        def __init__(self, screen):
            self.screen = screen
            self.text = font1.render('GAME OVER', True, (255, 255, 255))

        def draw_end_screen(self):
            screen.blit(self.text, (270, 200))
            pygame.display.update()


    # main loop

    run = True
    font = pygame.font.SysFont('comicsans', 30, True)
    point = Point(screen)
    super_point = Super_Point(screen)
    character = Hero()
    chance = random.random()
    end = End(screen)

    while run:
        clock.tick(32)

        if chance > 0.8:
            super_point.draw_super_point()
            if character.x < super_point.x and character.x \
                >= super_point.x - character.object_width \
                and character.y < super_point.y and character.y \
                >= super_point.y - character.object_height:
                character.score += 3
                chance = random.random()
                super_point.x = random.randint(0, screen_width
                        - super_point.width - 20)
                super_point.y = random.randint(0, screen_height
                        - super_point.height - 20)
        else:

            point.draw_point()
            if character.x < point.x and character.x >= point.x \
                - character.object_width and character.y < point.y \
                and character.y >= point.y - character.object_height:
                character.score += 1
                chance = random.random()
                point.x = random.randint(0, screen_width - point.width
                        - 20)
                point.y = random.randint(0, screen_height
                        - point.height - 20)

        # End Game

        if character.x < 0 - character.object_width + 40:
            character.vel_y = 0
            character.vel_x = 0
            character.end = 1
            end.draw_end_screen()

        elif character.x > screen_width - character.object_width + 40:
            character.vel_y = 0
            character.vel_x = 0
            character.end = 1
            end.draw_end_screen()

        elif character.y < 0 - character.object_height + 40:
            character.vel_y = 0
            character.vel_x = 0
            character.end = 1
            end.draw_end_screen()

        elif character.y > screen_height - character.object_height + 40:
            character.vel_y = 0
            character.vel_x = 0
            character.end = 1
            end.draw_end_screen()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or blink.value == 1:
            character.blink = 1
            blink.value = 0
            if character.blink == 1:
                character.direction += 1
                if character.direction == 5:
                    character.direction = 1
                    character.blink = 0

                if character.direction == 1:
                    character.right = True
                    character.down = False
                    character.left = False
                    character.up = False
                    character.blink = 0

                elif character.direction == 2:
                    character.right = False
                    character.down = True
                    character.left = False
                    character.up = False
                    character.blink = 0

                elif character.direction == 3:
                    character.right = False
                    character.down = False
                    character.left = True
                    character.up = False
                    character.blink = 0

                elif character.direction == 4:
                    character.right = False
                    character.down = False
                    character.left = False
                    character.up = True
                    character.blink = 0

        if character.end == 0:
            if character.right:
                character.object_width = 100
                character.object_height = 167
                character.vel_x = 10
                character.vel_y = 0

            elif character.down:
                character.object_width = 167
                character.object_height = 100
                character.vel_y = 10
                character.vel_x = 0

            elif character.left:
                character.object_width = 100
                character.object_height = 167
                character.vel_x = -10
                character.vel_y = 0

            elif character.up:
                character.object_width = 167
                character.object_height = 100
                character.vel_y = -10
                character.vel_x = 0
        else:
            character.vel_x = 0
            character.vel_y = 0

        if character.vel_x > 0:
            character.x += character.vel_x + character.score
        if character.vel_y > 0:
            character.y += character.vel_y + character.score
        if character.vel_x < 0:
            character.x += character.vel_x - character.score
        if character.vel_y < 0:
            character.y += character.vel_y - character.score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key \
                == pygame.K_ESCAPE:
                sys.exit(0)

        character.draw_hero(screen)

    proc_blink_det.join()
