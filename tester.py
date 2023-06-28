from versions.v4 import City, Ant, Colony
import threading
import random
import sys

NCITIES = 15
NANTS = 100
SEED = 0
DECAY = 0.5/NCITIES

MINSEED = int(sys.argv[-3])
MAXSEED = int(sys.argv[-2])
ITERS = int(sys.argv[-1])

pherWeight = float(sys.argv[-8])
idistWeight = float(sys.argv[-7])
poplWeight = float(sys.argv[-6])
greedWeight = float(sys.argv[-5])
inertiaWeight = float(sys.argv[-4])

lock = threading.Lock()
data = []

def onThread(seed, id):
    rand = random.Random(seed)
    cities = [City(5*rand.randint(1, 99), 5*rand.randint(1, 99), 1) for _ in range(NCITIES)]
    ants = [Ant(random.Random(), cities) for _ in range(NANTS)]
    colony = Colony(random.Random(), cities, ants, DECAY, 5000,
                    pherWeight, idistWeight, poplWeight, greedWeight, inertiaWeight)
    for ant in ants: ant.setColony(colony)
    pathComplete = False
    while not pathComplete:
        pathComplete = colony.tick()
    with lock:
        data.append((seed, colony.bestTick, colony.bestPLen, colony.bestPath))
        print(f"Chunk {seed},{id} complete")

threads = []
for seed in range(MINSEED, MAXSEED+1):
    for i in range(ITERS):
        thread = threading.Thread(target=onThread, args=(seed,i))
        thread.setDaemon(True)
        threads.append(thread)
        thread.start()

for thread in threads:
    thread.join()

with open(f"data {sys.argv[-9]}.txt", mode='w') as fl:
    for item in data:
        fl.write(f"[{str(item)}],")
