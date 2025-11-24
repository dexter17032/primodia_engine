import config
import pygame
import random

class Food:
    def __init__(self,tile):
        self.row,self.col = tile
        self.size = config.CELL_SIZE
        food_pallete = [(255,50,50),(40,100,255),(140,255,140)]
        self.color = food_pallete[0]
    def draw(self, surface):
        x = self.col * self.size
        y = self.row * self.size

        cx = x + self.size // 2
        cy = y + self.size // 2

        base_radius = int(self.size * 0.25)

    # Glow
        pygame.draw.circle(surface, (self.color[0], self.color[1], self.color[2],), (cx, cy), base_radius + 3, width=2)
    
    # Core
        pygame.draw.circle(surface, self.color, (cx, cy), base_radius)
