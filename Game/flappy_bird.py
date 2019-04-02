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


