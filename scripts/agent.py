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
        self.target_tile=None
        self.energy = random.randint(config.MAX_ENERGY-50,config.MAX_ENERGY)
        self.isalive = True
        self.ishungry = False
        self.hunger = 1 - (self.energy/config.MAX_ENERGY)
        self.smell_radius = config.SMELL_RADIUS
        self.metabolism = 1+random.random()
        self.want_to_fuck = random.random()
                
    def update(self,tile):
        self.energy-= self.metabolism
        self.row,self.col = tile
        if self.energy<=0:
            self.isalive=False
            
    def move_to_target():
        return (0,0)
    
    def pick_target(self,foods):
        visible_foods=[]
        self.hunger = 1-(self.energy/config.MAX_ENERGY)
        if not self.ishungry:
            self.ishungry = random.random()+config.SURVIVAL_FACTOR < self.hunger
        if self.ishungry:
            for food in foods:
                dist = math.sqrt((food.row-self.row)**2+(food.col-self.col)**2)
                if dist < self.smell_radius:
                    visible_foods.append((dist,food))
            
            if visible_foods:
                nearest_food = min(visible_foods,key=lambda a:a[0])[1]
                self.target_tile = (nearest_food.row,nearest_food.col)

            else :
                new_x = random.randint(0,config.GRID_COLS-1)
                new_y =random.randint(0,config.GRID_ROWS-1)
                self.target_tile = (new_x,new_y)
        
        else:
            new_x = random.randint(0,config.GRID_COLS-1)
            new_y =random.randint(0,config.GRID_ROWS-1)
            self.target_tile = (new_x,new_y)
        
        
        
            
    def propose_move(self,foods):
        
        if self.target_tile == None or (self.row == self.target_tile[0] and self.col == self.target_tile[1]):
            self.pick_target(foods)
         
        if self.row==self.target_tile[0]:
            dx=0
        elif self.row < self.target_tile[0] :
            dx =1
        else:
            dx = -1
            
        if self.col==self.target_tile[1]:
            dy = 0
        elif self.col < self.target_tile[1] :
            dy = 1
        else:
            dy = -1
        
        return (self.row+dx,self.col+dy)                
    
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
