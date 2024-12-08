#! /usr/bin/python3
# A class for drawing a grid with a default colour and
# being able to fill in grid blocks with a different colour
# based on their coordinates. 

import pygame

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range. Use 0 for x and 1 for y.")

    def __repr__(self):
        return f"Coordinate(x={self.x}, y={self.y})"

class Grid:
    def __init__(self, SCREEN_WINDOW, columns, rows, tileSize, background = (0, 0, 0), boarder = (200, 200, 200), highlighted = (0xff, 0xff, 0x0)):
        self.blockColourArray = [[background for x in range(columns)] for y in range(rows)]
        self.blockColourArray[5][2] = (255, 0, 0)
        self.columns = columns
        self.rows = rows
        self.tileSize = tileSize
        self.background = background
        self.boarder = boarder
        self.highlighted = highlighted
        self.SCREEN_WINDOW = SCREEN_WINDOW

    def draw(self):
        for col in range(self.columns):
            for row in range(self.rows):
                rect = pygame.Rect(20 + col * self.tileSize, 20 + row * self.tileSize, self.tileSize, self.tileSize)

                pygame.draw.rect(self.SCREEN_WINDOW, self.blockColourArray[row][col], rect, 0)                    
                pygame.draw.rect(self.SCREEN_WINDOW, self.boarder, rect, 1)

    def get_background_colour(self):
        return self.background

    def find_full_rows(self):
        # iterate the rows and check that all the blocks are not the background color
        # if they are all not the background colour add the index to teh result array.
        # the map function creates an array of trues and falses and the all function
        # checks for all true
        res = [ind for ind, x in enumerate(self.rows) if all(map(lambda y: y != self.background, x))]
        return res

    def colour_at_location(self, location):
        return self.blockColourArray[location.y][location.x]

    def location_is_in_grid(self, location):
        return location.x >= 0 and location.x < self.columns and location.y >= 0 and location.y < self.rows  
    
    def block_at_location_is_clear(self, location):
        return not self.location_is_in_grid(location) or self.blockColourArray[location.y][location.x] == self.background

    def set_colour_at_location(self, location, colour):
        self.blockColourArray[location.y][location.x] = colour

    def clear_locations(self, locations):
        for location in locations:
            self.blockColourArray[location.y][location.x] = self.background

    def clear(self):
        self.blockColourArray = [[self.background for x in range(self.columns)] for y in range(self.rows)]

if __name__ == "__main__":
    global SCREEN, CLOCK, BLACK, WHITE
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    BLUE = (0, 0, 200)
    WINDOW_HEIGHT = 400
    WINDOW_WIDTH = 400
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLUE)
    
    grid = Grid(SCREEN, 5, 10, 20, BLACK, WHITE)
    grid.draw()
    pygame.display.flip() #update the display
    while True:
        print("running")
        pygame.time.delay(2000)
