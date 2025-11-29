import pygame
from world import World
from grid import Grid
import config
import matplotlib.pyplot as plt
import numpy as np

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
    canvas.fill((255,255,255))
    world.draw(canvas)
    pygame.display.update()
    clock.tick(config.FPS)
    
    



