#! /usr/bin/python3
# A class for drawing a grid with a default colour and
# being able to fill in grid blocks with a different colour
# based on their coordinates.

import pygame

class Grid:
    def __init__(self, SCREEN_WINDOW, columns, rows, tileSize, background = (0, 0, 0), boarder = (200, 200, 200), highlighted = (0xff, 0xff, 0x0)):
        self.onOffArray = [[False for x in range(columns)] for y in range(rows)]
        self.onOffArray[5][2] = True
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
                rect = pygame.Rect(col * self.tileSize, row * self.tileSize, self.tileSize, self.tileSize)

                if self.onOffArray[row][col]:
                    pygame.draw.rect(self.SCREEN_WINDOW, self.highlighted, rect, 0)
                else:
                    pygame.draw.rect(self.SCREEN_WINDOW, self.background, rect, 0)
                    
                pygame.draw.rect(self.SCREEN_WINDOW, self.boarder, rect, 1)
    

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
