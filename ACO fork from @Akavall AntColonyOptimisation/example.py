import math
import numpy as np
import random

import pygame as pg

from ant_colony import AntColony

rand = random.Random(0)

NCITIES = 15
cities = [(5*rand.randint(1, 99), 5*rand.randint(1, 99)) for _ in range(NCITIES)]

def distBtw(a, b):
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    return math.sqrt(dx*dx+dy*dy)

distances = np.zeros((NCITIES, NCITIES))
for i, city_a in enumerate(cities):
    for j, city_b in enumerate(cities):
        distances[i,j] = np.inf if i==j else distBtw(city_a, city_b)


ant_colony = AntColony(distances, 100, 1, 100, 0.95, alpha=1, beta=1)
shortest_path = ant_colony.run()
print ("shorted_path: {}".format(shortest_path))



win = pg.display.set_mode((500,500))

def draw():
    win.fill((255,255,255))
    for city in cities:
        pg.draw.circle(win, (240,0,0), (city[0], city[1]), 5)

running = True
while running: 
    draw()
    pg.display.flip()
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running = False

pg.quit()