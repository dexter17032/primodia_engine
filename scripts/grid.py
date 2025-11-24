import config
import pygame

class Grid:
    def __init__(self):
        self.rows  = config.GRID_ROWS
        self.cols = config.GRID_COLS
        self.size = config.CELL_SIZE
    
    def draw(self,surface):
        for row in range(0,self.rows):
            for column in range(0,self.cols):
                color = (0, 0, 0)

                x = column*self.size
                y = row*self.size
                pygame.draw.rect(surface, color, (x,y,self.size,self.size),width=0)