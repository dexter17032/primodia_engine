import pygame
from world import World
from grid import Grid
import config
import matplotlib.pyplot as plt
import numpy as np

energy_wastage_list=[]
agent_count_list = []
food_count_list = []

pygame.init()
canvas = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

clock = pygame.time.Clock()
world = World()


running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    world.update()
    energy_wastage_list.append(world.energy_wastage)
    food_count_list.append(len(world.foods))
    agent_count_list.append(len(world.agents))
    canvas.fill((255,255,255))
    world.draw(canvas)
    pygame.display.update()
    clock.tick(config.FPS)
    
    


ew = np.array(energy_wastage_list)
ag = np.array(agent_count_list)
fd = np.array(food_count_list)

ew_norm = ew / ew.max()
ag_norm = ag / ag.max()
fd_norm = fd / fd.max()

plt.plot(ew_norm, color='black', label='Energy Wastage')
plt.plot(ag_norm, color='green', label='Agent Count')
plt.plot(fd_norm, color='blue', label='Food Count')
plt.legend()
plt.show()

