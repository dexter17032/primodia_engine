import config
import pygame
import random
import math
class Agent:
    def __init__(self,x,y,color):
        self.col = x
        self.row = y
        self.size = config.CELL_SIZE
        self.color=color
        self.directions=[(0,1),(0,-1),(1,0),(-1,0)]
        self.energy = random.randint(config.MAX_ENERGY-50,config.MAX_ENERGY)
        self.isalive = True
        self.hunger = 1 - (self.energy/config.MAX_ENERGY)
    def update(self,tile):
        self.energy-=1
        self.row,self.col = tile
        if self.energy<=0:
            self.isalive=False
            
    def propose_move(self,foods):
        visible_foods=[]
        self.hunger = 1-(self.energy/config.MAX_ENERGY)
        
        if random.random()+config.SURVIVAL_FACTOR < self.hunger:
            
            for food in foods:
                dist = math.sqrt((food.row-self.row)**2+(food.col-self.col)**2)
                if dist < config.SMELL_RADIUS:
                    visible_foods.append((dist,food))
                
            if len(visible_foods)==0:
                return random.choice([
                    (self.row, self.col),          # stay
                    (self.row + 1, self.col),
                    (self.row - 1, self.col),
                    (self.row, self.col + 1),
                    (self.row, self.col - 1)
                ])
                
            nearest = min(visible_foods,key=lambda x:x[0])[1]
            dx = 1 if nearest.row > self.row else -1 if nearest.row < self.row else 0
            dy = 1 if nearest.col > self.col else -1 if nearest.col < self.col else 0    

            new_row = self.row+dx
            new_col = self.col+dy
            if 0 <=new_row<config.GRID_ROWS and 0<= new_col<config.GRID_COLS:
                return (new_row,new_col)
            return(self.row,self.col)
        else :
            return random.choice([
                    (self.row, self.col),          # stay
                    (self.row + 1, self.col),
                    (self.row - 1, self.col),
                    (self.row, self.col + 1),
                    (self.row, self.col - 1)
                ])
            
        
    
    def draw(self,surface):
        x = self.col*self.size
        y = self.row*self.size
        padding = config.PADDING
        hunger_color = (int(255*self.hunger),int(255*(1-self.hunger)),0)
        pygame.draw.rect(surface,hunger_color,(
            x+padding,
            y+padding,
            self.size-padding*2,
            self.size-padding*2
            )
        )
