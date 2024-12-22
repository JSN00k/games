#! /usr/bin/python3

import sys
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
my_shape = Shape([Coordinate(0, 0), Coordinate(0, 1), Coordinate(1, 1)], my_grid, True, True, (0, 0, 200))

running = True

my_grid.clear()
my_shape.add_shape_to_grid()
my_grid.draw()
pygame.display.flip() #update the display

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get all currently pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        my_shape.move(Direction.UP)
    if keys[pygame.K_DOWN]:
        my_shape.move(Direction.DOWN)
    if keys[pygame.K_LEFT]:
        my_shape.move(Direction.LEFT)
    if keys[pygame.K_RIGHT]:
        my_shape.move(Direction.RIGHT)

    my_grid.clear()
    my_shape.add_shape_to_grid()

    my_grid.draw()
    pygame.display.flip() #update the display

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
