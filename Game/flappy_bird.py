import numpy as np
import sys
import random
import pygame
from Game import utils
import pygame.surfarray as surfarray
from pygame.locals import *
from itertools import cycle

#constants for game screen layout
frame_per_second = 30
screen_width = 288
screen_height = 512

#initilazion of game screen
pygame.init()
#create an object to help track time
fps_clock = pygame.time.Clock()
#Game screen specifications are given.
GAME_SCREEN = pygame.display.set_mode((screen_width, screen_height))
#Setting game window title
pygame.display.set_caption('Flappy_Bird-AI-Course')

#Loading the utils of the game.
IMAGES, GAME_SOUND, HITMASKS = utils.load()
#Setting Pipe Space Between Upper And Lower part of Pipe
pipe_space_size = 100
base_y = screen_height * 0.79

player_width = IMAGES['player'][0].get_width()
player_height = IMAGES['player'][0].get_height()
pipe_width = IMAGES['pipe'][0].get_width()
pipe_height = IMAGES['pipe'][0].get_height()
background_width = IMAGES['background'].get_width()

player_index_generation = cycle([0, 1, 2, 1])


class state_game:
    def __init__(self):
        self.score = self.playerIndex = self.loopIter = 0
        self.playerX = int(screen_width)
        self.playerY = int((screen_height - player_height) / 2)
        self.baseX = 0
        #to shift the base during the game.
        self.baseShift = IMAGES['base'].get_width() - background_width

        newPipe1 = generateRandomPipe()
        newPipe2 = generateRandomPipe()

        self.upperPipes = [
            {'x': screen_width, 'y': newPipe1[0]['y']},
            {'x': screen_width + (screen_width / 2), 'y': newPipe2[0]['y']},
        ]
        self.lowerPipes = [
            {'x': screen_width, 'y': newPipe1[1]['y']},
            {'x': screen_width + (screen_width / 2), 'y': newPipe2[1]['y']},
        ]

        self.pipe_velocity_x = -4
        self.player_velocity_y = 0  # player's velocity along Y, default same as playerFlapped
        self.player_max_velocity_y = 10  # max vel along Y, max descend speed
        self.player_min_velocity_y = -8  # min vel along Y, max ascend speed
        self.player_acc_y = 1  # players downward accleration asagi yonlu hizlanma
        self.player_acc_flap= -9  # players speed on flapping
        self.player_flapped = False  # True when player flaps

   


def generateRandomPipe():
    #With this class, it will produce a random pipe and returns the necessary places.
    #Y is the empty space between upper and lower pipe
    #I produce this spaces as a list.

    pipe_gaps = [20, 30 , 40 , 50 , 60 , 70 , 80, 90]
    #this will produce a random index to select one of the Y.
    lengh_y = len(pipe_gaps)
    index = random.randint(0, pipe_gaps-1)
    pipe_gap= pipe_gaps[index]

    pipe_gap = pipe_gap + int(base_y * 0.2)
    pipeX = screen_width + 10

    return [
        {'x': pipeX, 'y': pipe_gap - pipe_height}, {'x': pipeX, 'y': pipe_gap + pipe_space_size},
        # upper pipe,  # lower pipe
    ]

def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (screen_width - totalWidth) / 2

    for digit in scoreDigits:
        GAME_SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, screen_height * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()

def checkCrash(player, upperPipes, lowerPipes):
    #returns True if player colliders with base or pipes.
    player_index = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= base_y - 1:
        return True
    else:
        #pygame object for storing rectangular coordinates
        player_rect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])

        for upper_pipe, lower_pipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(upper_pipe['x'], upper_pipe['y'], pipe_width, pipe_height)
            lPipeRect = pygame.Rect(lower_pipe['x'], lower_pipe['y'], pipe_width, pipe_height)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][player_index]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upper pipe or lower pipe
            upper_collide = pixel_collision(player_rect, uPipeRect, pHitMask, uHitmask)
            lower_collide = pixel_collision(player_rect, lPipeRect, pHitMask, lHitmask)

            if upper_collide or lower_collide:
                return True

    return False

def pixel_collision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    #think this is rectangle
    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False