import config
import pygame
import random
import math
class Agent:
    def __init__(self,x,y,color):
        
        #position params
        self.col = x
        self.row = y
        self.size = config.CELL_SIZE
        self.color=color
        self.directions=[(0,1),(0,-1),(1,0),(-1,0)]
        self.target_tile=None
        
        #eating and energy params
        self.energy = random.randint(config.MAX_ENERGY-50,config.MAX_ENERGY)
        self.isalive = True
        self.ishungry = False
        self.hunger = 1 - (self.energy/config.MAX_ENERGY)
        
        #fucking params        
        self.horniness = random.random()
        self.gender = random.choice(["M","F"])
        self.mating_cooldown = 0
        self.target_partner  = None
        
        #mutation params
        self.smell_radius = random.randint(15,config.SMELL_RADIUS)
        self.metabolism = random.uniform(0.6,1)*config.METABOLISM_RATE_GLOBAL
        #self.laziness = random.uniform(0,0.5)
            
            
    def update(self,tile):
        self.energy-= self.metabolism
        self.horniness+= random.random()*config.WORLD_HORNINESS
        self.row,self.col = tile
        
        if(self.mating_cooldown>0):
            self.mating_cooldown-=1
        
        if self.energy<=0:
            self.isalive=False
            
    def ready_to_mate(self):
        if self.horniness>config.HORNINESS_THRESHOLD and self.energy > config.MAX_ENERGY*0.80 and self.mating_cooldown==0:
            return True
            
    def inherit(self,mother,father):
        self.metabolism = (mother.metabolism+father.metabolism)/2
        self.smell_radius = (mother.smell_radius+father.smell_radius)/2
        
        if random.random() < config.MUTATION_RATE:
            self.metabolism *= random.uniform(1-config.MUTATION_LIMIT,1+config.MUTATION_LIMIT)
            
        if random.random() < config.MUTATION_RATE:
            self.smell_radius *= random.uniform(1-config.MUTATION_LIMIT,1+config.MUTATION_LIMIT)
           
    
    def pick_target(self,foods):
        visible_foods=[]
        self.hunger = 1-(self.energy/config.MAX_ENERGY)
        if not self.ishungry:
            self.ishungry = random.random()+config.SURVIVAL_FACTOR < self.hunger
        
        if self.target_partner:
            partner = self.target_partner
            self.target_tile = (partner.row,partner.col)    
        
        elif self.ishungry:
            for food in foods:
                dist = math.sqrt((food.row-self.row)**2+(food.col-self.col)**2)
                if dist < self.smell_radius:
                    visible_foods.append((dist,food))
            
            if visible_foods:
                nearest_food = min(visible_foods,key=lambda a:a[0])[1]
                self.target_tile = (nearest_food.row,nearest_food.col)

            else :
                new_col = random.randint(0,config.GRID_COLS-1)
                new_row =random.randint(0,config.GRID_ROWS-1)
                self.target_tile = (new_row,new_col)
                 
        else:
            new_col = random.randint(0,config.GRID_COLS-1)
            new_row =random.randint(0,config.GRID_ROWS-1)
            self.target_tile = (new_row,new_col)
            
        new_row = max(0,min(config.GRID_ROWS-1,self.target_tile[0]))
        new_col = max(0,min(config.GRID_COLS-1,self.target_tile[1]))
        self.target_tile = (new_row,new_col)
        
        
        
            
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
        color = (255, 240, 150) if self.gender == "M" else (255, 80, 180)

        pygame.draw.rect(surface,color,(
            x+padding,
            y+padding,
            self.size-padding*2,
            self.size-padding*2
            )
        )
