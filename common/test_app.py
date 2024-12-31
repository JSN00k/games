#! /usr/bin/python3

import sys
from grid import Grid
from grid import Coordinate
from shape import Shape
from shape import Direction
import pygame

def direction_for_key(pygame_key):
    if pygame_key == pygame.K_w:
        return Direction.UP
    if pygame_key == pygame.K_s:
        return Direction.DOWN
    if pygame_key == pygame.K_a:
        return Direction.LEFT
    if pygame_key == pygame.K_d:
        return Direction.RIGHT
    
    return None

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLUE = (0, 0, 200)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
SCREEN.fill(BLUE)

my_grid = Grid(SCREEN, 5, 10, 20, BLACK, WHITE)
my_shape = Shape([Coordinate(-2, 0), Coordinate(-2, 1), Coordinate(-1, 0), Coordinate(-1, 1)], my_grid, True, True, (0, 0, 200))

running = True

my_grid.clear()
my_grid.set_colour_at_location(Coordinate(3, 4), (200, 0, 0))
my_shape.add_shape_to_grid()
my_grid.draw()
pygame.display.flip() #update the display

persistent_key = None

while running:
    directionReceived = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not persistent_key:
            direction = direction_for_key(event.key)
            if direction:
                persistent_key = event.key
                if not directionReceived:
                    my_shape.move(direction)
                    directionReceived = True
        elif persistent_key and event.type == pygame.KEYUP and persistent_key == event.key:
            persistent_key = None

    if persistent_key and not directionReceived:
        my_shape.move(direction_for_key(persistent_key))

    my_shape.add_shape_to_grid()

    my_grid.draw()
    pygame.display.flip() #update the display

    pygame.time.Clock().tick(5)



pygame.quit()
sys.exit()

