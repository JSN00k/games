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

    def all_coords_on_grid(self):
        return all(map(lambda x : x.x >= 0 and x.x < self.grid.columns and x.y >= 0 and x.y < self.grid.rows, self.shape_coords))

    def move_by(self, move_val, moveHoriz):
        newLocations = None
        accessor = 0 # choose the horizontal component
        end_val = self.grid.columns

        # Don't allow wrapping until all parts of the shape are already on the grid.
        actually_allow_wrap = self.allow_wrap and self.all_coords_on_grid()
        
        if not moveHoriz:
            # set up for moving vertically
            accessor = 1
            end_val = self.grid.rows
            
        if not actually_allow_wrap:
            # check we can move, return false if we can't
            newLocations = [create_coordinate(x, x[accessor] + move_val, moveHoriz) for x in self.shape_coords]
            # The rule is that shapes cannot go off the grid or further off the grid
            # so if a coord in the shape is at the edge of this axis or further and moving toward the edge the
            # move is not allowed.
            true_false_list = map(lambda x : x[accessor] >= end_val - 1 and move_val > 0 or x[accessor] <= 0 and move_val < 0, self.shape_coords)
            if any(true_false_list):
                # one of my coordinates is off the grid and moving away from the grid
                return False

        else:
            # We can't get here unless all locations were already on the grid
                newLocations = [create_coordinate(x, ((((x[accessor] + move_val) % end_val) + end_val)) % end_val, moveHoriz) for x in self.shape_coords]

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
