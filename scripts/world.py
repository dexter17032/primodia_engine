from grid  import Grid
from agent import Agent
import random
import config
from food import Food

class World:
    def __init__(self):
        self.grid = Grid()
        self.agents=[]
        self.foods=[]
        self.energy_wastage = 0

        for _ in range(config.NO_OF_AGENTS):
            row = random.randint(0, self.grid.rows - 1)
            col = random.randint(0, self.grid.cols - 1)

            color = (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            )
            self.agents.append(Agent(col, row, color))
            
        for _ in range(config.BASE_AVAILABLE_FOODS):
            r = random.randint(0,self.grid.rows-1)
            c = random.randint(0,self.grid.cols-1)
            self.foods.append(Food((r,c)))
                
            
        
        self.occupied=set()
        self.proposals = {}
        
        
    def group_proposals(self,proposals):
        grouped_proposals = {}
        for agent,tile in proposals.items():
            if tile not in grouped_proposals:
                grouped_proposals[tile] = []
            grouped_proposals[tile].append (agent)
            
        return grouped_proposals
    
    def conflict_resolution(self, proposals):
        grouped = self.group_proposals(proposals)
        approved = {}

        for tile, agent_list in grouped.items():

            # 1️⃣ Check for staying agents
            staying_agents = []
            for a in agent_list:
                if proposals[a] == (a.row, a.col):
                    staying_agents.append(a)

            if staying_agents:
                # Tile stays locked for the staying agent
                approved[staying_agents[0]] = tile
                continue  # skip the rest of the logic
            r,c = tile
            is_food_tile  = False
            for f in self.foods:
                if f.col==c and f.row==r:
                    is_food_tile = True
                    break
            # 2️⃣ Tile has no staying occupant → free to compete
            if len(agent_list) == 1:
                approved[agent_list[0]] = tile
            else:
                #if is_food_tile:
                winner = max(agent_list,key=lambda a:a.hunger)
                #else:
                    #winner = random.choice(agent_list)
                
                approved[winner] = tile

        return approved

    
    
    def update(self):
        self.occupied=set()
        self.proposals={}
        foods_to_remove=set()
            
        for agent in self.agents:
            self.occupied.add((agent.row,agent.col))
            self.proposals[agent] = agent.propose_move(self.foods)
                
        approved = self.conflict_resolution(self.proposals)
        for agent,tile in approved.items():
            agent.update(tile)
            
        
        
        for agent in self.agents:
            for food in self.foods:
                if agent.row==food.row and agent.col==food.col:
                    energy_req_agent = config.MAX_ENERGY-agent.energy
                    if food.energy>energy_req_agent:
                        agent.energy=config.MAX_ENERGY
                        food.energy-=energy_req_agent
                    else:
                        agent.energy+=food.energy 
                        food.energy=0
                    
                    if food.energy<=0:
                        foods_to_remove.add(food)
                        
        for f in foods_to_remove:self.foods.remove(f)
                
        alive_agents = [a for a in self.agents if a.isalive]
        self.agents=alive_agents
        if len(self.foods) < config.FOOD_CAP:
            if random.random() <= config.FOOD_SPAWN_CHANCE:
                r = random.randint(0,self.grid.rows-1)
                c = random.randint(0,self.grid.cols-1)
                self.foods.append(Food((r,c)))
                    

        print("currently alive agents : "+ str(len(self.agents))+" food available : " + str(len(self.foods))) 
            

    def draw(self, surface):
        self.grid.draw(surface=surface)
        
        for food in self.foods:
            food.draw(surface)
        for agent in self.agents:
            agent.draw(surface)
