import functools as ft
import pygame as pg
import random as r
import math
import time
import sys

win = pg.display.set_mode((500,500))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)

NCITIES = 10
NANTS = 100
DT = 0

running = True

@ft.cache
def dist(a, b):
    dx = a[0]-b[0]
    dy = a[1]-b[1]
    return math.sqrt(dx*dx+dy*dy)



cities = []
ants = []

trails = {}

phers = {}

lastBestPath = NCITIES*200
lastBestRoute = cities.copy()



class City:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight

class Ant:
    def __init__(self, rootCity, cities, distPower, pherPower):
        self.rc = rootCity
        self.c = rootCity
        self.cities = cities
        self.distPower = distPower
        self.pherPower = pherPower
        self.visited = [rootCity]
        self.done = False
        self.pLen = 0
    @property
    def x(self): return self.c.x
    @property
    def y(self): return self.c.y
    def tick(self):
        if len(self.visited)==NCITIES:
            # trails[(self.c, self.rc)] = 0.5
            self.c = self.rc
            self.done = True
            return 
        cities = [c for c in self.cities if c not in self.visited]
        dists = [dist((self.x, self.y), (c.x, c.y)) for c in cities]
        weights = []
        for i in range(len(cities)):
            weight = (1/dists[i])**self.distPower if dists[i]!=0 else 0
            if (self.c, cities[i]) in phers.keys():
                weight += phers[(self.c, cities[i])]**self.pherPower
                sys.stdout.flush()
            weights.append(weight)
        nextCity = r.choices(cities, weights)[0]
        # trails[(self.c, nextCity)] = 0.5
        self.pLen += dist((self.c.x, self.c.y), (nextCity.x, nextCity.y))
        self.c = nextCity
        self.visited.append(self.c)
    def reset(self):
        self.c = self.rc
        self.visited = [self.rc]
        self.done = False
        self.pLen = 0



def reset():
    for ant in ants:
        ant.reset()

def pherGen():
    global trails, lastBestRoute, lastBestPath
    trails = {}
    bestRoute = lastBestRoute
    bestPath = lastBestPath
    for ant in ants:
        if bestPath == -1 or ant.pLen < bestPath:
            bestRoute = ant.visited
            bestPath = ant.pLen
    if bestPath != lastBestPath: print("New best:", bestPath)
    lastBestPath = bestPath
    lastBestRoute = bestRoute
    for idx in range(len(bestRoute)):
        trails[(bestRoute[idx-1], bestRoute[idx])] = 1
        # if (bestRoute[idx-1], bestRoute[idx]) in phers.keys():
        #     phers[(bestRoute[idx-1], bestRoute[idx])] += 0.1
        # else:
        phers[(bestRoute[idx-1], bestRoute[idx])] = 1/bestPath # Tab this in if the if-else is uncommented

def tick():
    if ants[0].done:
        pherGen()
        reset()
        return
    for ant in ants:
        ant.tick()
        
def reload():
    print('-'*25+'RESET'+'-'*25)
    global ants, cities, lastBestPath, lastBestRoute
    cities = [City(r.randint(1, 100), r.randint(1, 100), 5) for _ in range(NCITIES)]
    ants = [Ant(r.choice(cities), cities, 0.5, 0.5) for _ in range(NANTS)]
    lastBestPath = NCITIES*200
    lastBestRoute = cities.copy()
    
def draw():
    win.fill(WHITE)
    for city in cities:
        pg.draw.circle(win, BLACK, (5*city.x, 5*city.y), 5)
    for ant in ants:
        pg.draw.rect(win, RED, pg.rect.Rect(5*ant.x-2, 5*ant.y-2, 4, 4))
    for tpl, weight in trails.items():
        pg.draw.line(win, (255-255*weight, 255-255*weight, 255-255*weight), (5*tpl[0].x, 5*tpl[0].y), (5*tpl[1].x, 5*tpl[1].y))

reload()

prev = time.time()

while running:
    if DT==0: tick()
    elif time.time()-prev >= DT:
        tick()
        prev = time.time()
    draw()
    pg.display.flip()
    for e in pg.event.get():
        if e.type == pg.KEYDOWN:
            if pg.key.name(e.key) == 'q':
                for a in ants: a.distPower += 0.05
                print("DistPower is now", ants[0].distPower)
            if pg.key.name(e.key) == 'a':
                for a in ants: a.distPower -= 0.05
                print("DistPower is now", ants[0].distPower)
            if pg.key.name(e.key) == 'w':
                for a in ants: a.pherPower += 0.05
                print("PherPower is now", ants[0].pherPower)
            if pg.key.name(e.key) == 's':
                for a in ants: a.pherPower -= 0.05
                print("PherPower is now", ants[0].pherPower)
            if pg.key.name(e.key) == 'r':
                reload()
            # if pg.key.name(e.key) == 'space':
            #     tick()
        if e.type == pg.QUIT: running = False

pg.quit()
