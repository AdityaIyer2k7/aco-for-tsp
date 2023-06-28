from typing import Iterable
import pygame as pg
import numpy as np
import random
import math



BGCOLOR = (255,255,255)
CCOLOR = (240,0,0)
ACOLOR = (0,240,0)
BLACK = (0,0,0)
NCITIES = 15
NANTS = 150
SEED = 0
DECAY = 0.5/NCITIES

def distBtw(a, b):
    dx = a.x-b.x
    dy = a.y-b.y
    return math.sqrt(dx*dx+dy*dy)



class City:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight

class Colony:
    def __init__(self, rand:random.Random, cities:Iterable[City], ants:Iterable, decay:float, max_iter:int, pherWeight:float, idistWeight:float, *_):
        self.r = rand
        self.cities = cities
        self.n_cities = len(cities)
        self.ants = ants
        self.n_ants = len(ants)
        self.mat_pheromone = np.zeros((self.n_cities, self.n_cities))
        self.mat_invdist = np.zeros((self.n_cities, self.n_cities))
        for i, city_a in enumerate(cities):
            for j, city_b in enumerate(cities):
                self.mat_invdist[i,j] = 0 if i==j else 1/distBtw(city_a, city_b)
        self.pherWeight = pherWeight
        self.idistWeight = idistWeight
        self.decay = decay
        self.max_iter = max_iter
        self.tickCount = 0
        self.bestPath = []
        self.bestPLen = -1
        self.bestTick = -1
        self.lupdate = 0
    def tick(self):
        if self.tickCount >= self.max_iter: return True
        self.mat_pheromone *= (1-self.decay)
        self.tickCount += 1
        # print(f"{self.tickCount} ticks elapsed")
        for ant in self.ants:
            c = ant.tick()
            if c:
                if round(ant.pLen, 3) < self.bestPLen or self.bestPLen==-1:
                    # print(ant.path, round(ant.pLen, 3), self.tickCount)
                    self.bestPath = ant.path
                    self.bestPLen = round(ant.pLen, 3)
                    self.bestTick = self.tickCount
                    self.lupdate = self.tickCount
                    for idx in range(len(self.bestPath)):
                        c1 = self.bestPath[idx-1]
                        c2 = self.bestPath[idx]
                        self.mat_pheromone[c1,c2] += 1/self.bestPLen
                ant.idx = ant.rootidx
                ant.path = [ant.idx]
                ant.pLen = 200*self.n_cities
        return False

class Ant:
    def __init__(self, rand:random.Random, cities:Iterable[City]):
        self.rand = rand
        self.idx = rand.randint(0, len(cities)-1)
        self.rootidx = self.idx
        self.cities = cities
        self.n_cities = len(cities)
        self.path = [self.idx]
        self.pLen = 200*NCITIES
    def setColony(self, colony:Colony):
        self.colony = colony
        self.pherWeight = colony.pherWeight
        self.idistWeight = colony.idistWeight
    def tick(self) -> bool:
        usable = [i for i in range(0, len(self.cities)) if i not in self.path]
        if len(usable)==0:
            self.pLen += distBtw(self.cities[self.idx], self.cities[self.rootidx])
            self.idx = self.rootidx
            return True
        # Pheromones
        pher = [self.colony.mat_pheromone[self.idx][i]*(0.5+self.rand.random()) for i in usable]
        pher = np.multiply(pher, self.pherWeight/sum(pher) if sum(pher)!=0 else 0)
        # Inv. dists
        invd = [self.colony.mat_invdist[self.idx][i]*(0.5+self.rand.random()) for i in usable]
        invd = np.multiply(invd, self.idistWeight/sum(invd) if sum(invd)!=0 else 0)
        # Final weights and decision
        w = np.add(pher, invd)
        newidx = self.rand.choices(usable, w)[0]
        self.pLen += distBtw(self.cities[self.idx], self.cities[newidx])
        self.idx = newidx
        self.path.append(self.idx)
        return False



def init():
    global font, rand, cities, ants, colony
    font = pg.font.Font('freesansbold.ttf', 20)
    rand = random.Random(SEED)
    cities = [City(5*rand.randint(1, 99), 5*rand.randint(1, 99), 1) for _ in range(NCITIES)]
    ants = [Ant(rand, cities) for _ in range(NANTS)]
    colony = Colony(rand, cities, ants, DECAY, 5000, 0.4, 0.5)
    for ant in ants: ant.setColony(colony)

if __name__ == '__main__':
    pg.init()
    win = pg.display.set_mode((500,500))
    def draw():
        win.fill(BGCOLOR)
        seedTxt = font.render(str(SEED), True, BLACK, BGCOLOR)
        seedRect = seedTxt.get_rect()
        win.blit(seedTxt, seedRect)
        for idx, city in enumerate(cities):
            c = (255*(idx/NCITIES), 255*(1-idx/NCITIES), 0)
            pg.draw.circle(win, c, (city.x, city.y), 5)
            t = font.render(str(idx), True, BLACK, BGCOLOR)
            r = t.get_rect()
            r.center = (city.x+10, city.y+10)
            win.blit(t, r)
        # for ant in ants: pg.draw.circle(win, ACOLOR, (cities[ant.idx].x, cities[ant.idx].y), 2)
        for idx in range(len(colony.bestPath)):
            c0 = cities[colony.bestPath[idx-1]]
            c1 = cities[colony.bestPath[idx]]
            pg.draw.line(win, BLACK, (c0.x, c0.y), (c1.x, c1.y))
        # for i in range(NCITIES):
        #     for j in range(NCITIES):
        #         c = 255-255*colony.mat_pheromone[i,j]*colony.pherWeight
        #         c = (c,c,c) if c>0 else (0,0,0)
        #         pg.draw.line(win, c, (cities[i].x-2, cities[i].y-2), (cities[j].x-2, cities[j].y-2))
    running = True
    lupdate = 0
    init()
    while running:
        colony.tick()
        if lupdate!=colony.lupdate:
            draw()
            lupdate = colony.lupdate
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if pg.key.name(event.key)=='space':
                    colony.tick()
                if pg.key.name(event.key)=='r':
                    init()
                if pg.key.name(event.key)=='up':
                    SEED += 1
                if pg.key.name(event.key)=='down':
                    SEED -= 1

    pg.quit()
