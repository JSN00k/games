#! /usr/bin/python3

from grid import Coordinate
from enum import Enum
from pprint import pprint

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

def create_coordinate(orig, newVal, updateX):
    if updateX:
        return Coordinate(newVal, orig.y)
    else:
        return Coordinate(orig.x, newVal)
    
class Shape():
    def __init__(self, shape_coords, grid, allow_wrap, can_only_move_to_clear_squares, colour):
        self.allow_wrap = allow_wrap
        self.shape_coords = shape_coords
        self.can_only_move_to_clear_squares = can_only_move_to_clear_squares
        self.colour = colour
        self.grid = grid

    def move_by(self, move_val, moveHoriz):
        newLocations = None
        accessor = 0 # choose the horizontal component
        end_val = self.grid.columns
        
        if not moveHoriz:
            # set up for moving vertically
            accessor = 1
            end_val = self.grid.rows
            
        if not self.allow_wrap:
            # check we can move, return false if we can't
            newLocations = [create_coordinate(x, x[accessor] + move_val, moveHoriz) for x in self.shape_coords]
            # The rule is that shapes cannot go off the grid, however if they
            # were off the grid they can move onto it.
            true_false_list = map(lambda x : x[accessor] >= end_val - 1 and move_val > 0 or x[accessor] <= 0 and move_val < 0, self.shape_coords)
            if any(true_false_list):
                # one of my coordinates is off the grid and moving away from the grid
                return False

        else:
            # use modular arithmetic to work out the new locations, however, if a location
            # was already off screen do not do the modular arigthmetic 
            newLocations = [create_coordinate(x, ((((x[accessor] + move_val) % end_val) + end_val)) % self.grid.columns, moveHoriz) for x in self.shape_coords if x[accessor] >= 0 and x[accessor] < end_val]
            # The previous loop does not increment the values that were off the sceen.
            newLocations = [create_coordinate(x, x[accessor] + move_val, moveHoriz) for x in newLocations if x[accessor] < 0 or x[accessor] >= end_val]

        self.grid.clear_locations(self.shape_coords)
        # we have now constructed the new locations.
        if self.can_only_move_to_clear_squares:
            # check all new locations are the background colour
            true_false_array = map(lambda x: self.grid.block_at_location_is_clear(x), newLocations)
            if not all(true_false_array):
                self.add_shape_to_grid()
                return False

        self.shape_coords = newLocations
        self.add_shape_to_grid()
        
    def move(self, move_direction):
        pprint(self.shape_coords)
        match move_direction:
            case Direction.UP:
                self.move_by(-1, False)
                return
            case Direction.RIGHT:
                self.move_by(1, True)
                return
            case Direction.DOWN:
                self.move_by(1, False)
                return
            case Direction.LEFT:
                self.move_by(-1, True)
                return
            
    def add_shape_to_grid(self):
        for coord in self.shape_coords:
            if coord.x < 0 or coord.y < 0 or coord.x >= self.grid.columns or coord.y >= self.grid.rows:
                continue

            self.grid.set_colour_at_location(coord, self.colour)
