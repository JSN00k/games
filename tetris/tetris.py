import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__)).split()[0]
print(dir_path)

sys.path.append(dir_path + "/../common")

from grid import Grid
from grid import Coordinate
from shape import Shape
from shape import Direction

import pygame

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLUE = (0, 0, 200)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
SCREEN.fill(BLUE)

my_grid = Grid(SCREEN, 5, 10, 20, BLACK, WHITE)

pygame.display.flip() #update the display