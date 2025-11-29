from grid  import Grid
from agent import Agent
import random
import math
import config
from food import Food

class World:
    def __init__(self):
        self.grid = Grid()
        self.agents=[]
        self.foods=[]
        self.energy_wastage = 0
        self.ready_males=[]
        self.ready_females = []
        self.mating_in_progress = []
        self.babies_born = []
        
        self.no_of_babies=0

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
    
    
    def get_stats(self):
        if len(self.agents) > 0:
            avg_energy = sum(a.energy for a in self.agents) / len(self.agents)
            avg_horniness = sum(a.horniness for a in self.agents) / len(self.agents)
        else:
            avg_energy = 0
            avg_horniness = 0

        return {
        "agents": len(self.agents),
        "babies": self.no_of_babies,
        "foods": len(self.foods),
        "avg_energy": int(avg_energy),
        "avg_horniness": int(avg_horniness),
        "mating": len(self.mating_in_progress),
        }

        
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
                if is_food_tile:
                    winner = max(agent_list,key=lambda a:a.hunger)
                else:
                    winner = random.choice(agent_list)
                
                approved[winner] = tile

        return approved

            
    def agent_eats(self,foods_to_remove):
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
                    agent.ishungry = False        
    
    
    def add_food_to_world(self):
        if len(self.foods) < config.FOOD_CAP:
            if random.random() <= config.FOOD_SPAWN_CHANCE:
                r = random.randint(0,self.grid.rows-1)
                c = random.randint(0,self.grid.cols-1)
                self.foods.append(Food((r,c)))
    
    def male_score(self,male,female):
        horniness_n = male.horniness
        energy_n = male.energy/config.MAX_ENERGY
        distance  = math.dist((female.row,female.col),(male.row,male.col))
        distance_n = 1- distance/math.dist((0,0),(config.GRID_ROWS-1,config.GRID_COLS-1))
        if distance_n<0 : distance_n=0
        
        return horniness_n*config.HORNINESS_WEIGHT + energy_n*config.ENERGY_WEIGHT + distance_n*config.DISTANCE_WEIGHT
    
    def choose_partner(self):             
        for female in self.ready_females:
            if self.ready_males:
                best_male = max(self.ready_males,key= lambda m : self.male_score(m , female))
                self.ready_males.remove(best_male)
                female.target_partner = best_male
                best_male.target_partner  = female
                self.mating_in_progress.append(female)
                
        self.ready_females = [f for f in self.ready_females if f.target_partner is None]    
    
    
    def mate_if_possible(self):
        for female in self.mating_in_progress[:]:
            if female.target_partner  in self.agents:
                if abs(female.row - female.target_partner.row)<=1 and abs(female.col - female.target_partner.col)<=1:
                    self.babies_born.append((
                        female.row,
                        female.col,
                        female,
                        female.target_partner
                    ))
                    
                    male = female.target_partner
                    
                    male.horniness = 0
                    male.target_tile = None
                    male.mating_cooldown = config.MATING_COOLDOWN
                    male.target_partner = None
                    
                    female.horniness = 0
                    female.target_tile = None
                    female.mating_cooldown = config.MATING_COOLDOWN
                    female.target_partner = None
                    
                    self.mating_in_progress.remove(female)
                    
            else :
                female.target_partner = None
                self.mating_in_progress.remove(female)
                    
    def spawn_babies(self):
        new_pending = []

        for (row, col, female, male) in self.babies_born:

            spawn_tile = None

        # 1. Try original tile
            if (row, col) not in self.occupied:
                spawn_tile = (row, col)
            else:
            # 2. Try 8 neighbors
                neighbors = [
                    (row + dr, col + dc)
                    for dr in (-1, 0, 1)
                    for dc in (-1, 0, 1)
                    if not (dr == 0 and dc == 0)
                ]

                for (r, c) in neighbors:
                    if 0 <= r < config.GRID_ROWS and 0 <= c < config.GRID_COLS:
                        if (r, c) not in self.occupied:
                            spawn_tile = (r, c)
                            break

            if spawn_tile:
                r, c = spawn_tile

                # Create baby
                baby = Agent(c, r, (
                    random.randint(50, 255),
                    random.randint(50, 255),
                    random.randint(50, 255)
                ))
                self.no_of_babies+=1

            # Optional: inherit some traits
                baby.energy = config.MAX_ENERGY * 0.5
                baby.metabolism = (female.metabolism + male.metabolism) / 2

                self.agents.append(baby)
                self.occupied.add((r, c))

            else:
            # No room → try again next tick
                new_pending.append((row, col, female, male))

        self.babies_born = new_pending

        
        
           
    def update(self):
        
        self.spawn_babies()
        self.occupied=set()
        self.proposals={}
        foods_to_remove=set()
        self.ready_males =[]
        self.ready_females=[]

            
        for agent in self.agents:
            self.occupied.add((agent.row,agent.col))
            self.proposals[agent] = agent.propose_move(self.foods)
        approved = self.conflict_resolution(self.proposals)
        for agent,tile in approved.items():
            agent.update(tile)
            
        self.agent_eats(foods_to_remove)

                        
        for f in foods_to_remove:self.foods.remove(f)
                
        alive_agents = [a for a in self.agents if a.isalive]

        self.agents=alive_agents

        for agent in self.agents:
            if agent.ready_to_mate():
                if agent.gender=="M":
                    self.ready_males.append(agent)
                else:
                    self.ready_females.append(agent)
        
        self.choose_partner()
        
        self.mate_if_possible()
        
        self.add_food_to_world()  

    def draw(self, surface):
        self.grid.draw(surface=surface)
        
        for food in self.foods:
            food.draw(surface)
        for agent in self.agents:
            agent.draw(surface)
