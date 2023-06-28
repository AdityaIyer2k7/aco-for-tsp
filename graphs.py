import matplotlib.pyplot as plt
import numpy as np
import json

fn1 = "data/data orig.txt"
fn2 = "data/data popl.txt"
fn3 = "data/data greed.txt"
fn4 = "data/data iner.txt"
fn5 = "data/data all.txt"

with open(fn1) as fl: d1 = np.array(json.load(fl), dtype=object)
with open(fn2) as fl: d2 = np.array(json.load(fl), dtype=object)
with open(fn3) as fl: d3 = np.array(json.load(fl), dtype=object)
with open(fn4) as fl: d4 = np.array(json.load(fl), dtype=object)
with open(fn5) as fl: d5 = np.array(json.load(fl), dtype=object)

t1 = [d1[d1[:,0]==i,1] for i in range(21)]
t2 = [d2[d2[:,0]==i,1] for i in range(21)]
t3 = [d3[d3[:,0]==i,1] for i in range(21)]
t4 = [d4[d4[:,0]==i,1] for i in range(21)]
t5 = [d5[d5[:,0]==i,1] for i in range(21)]

t1bar = [sum(t1[i])/5 for i in range(21)]
t2bar = [sum(t2[i])/5 for i in range(21)]
t3bar = [sum(t3[i])/5 for i in range(21)]
t4bar = [sum(t4[i])/5 for i in range(21)]
t5bar = [sum(t5[i])/5 for i in range(21)]

t1bar2 = np.average(t1bar)
t2bar2 = np.average(t2bar)
t3bar2 = np.average(t3bar)
t4bar2 = np.average(t4bar)
t5bar2 = np.average(t5bar)

emin = [
    t1bar2 - min(t1bar),
    t2bar2 - min(t2bar),
    t3bar2 - min(t3bar),
    t4bar2 - min(t4bar),
    t5bar2 - min(t5bar)
]
emax = [
    max(t1bar) - t1bar2,
    max(t2bar) - t2bar2,
    max(t3bar) - t3bar2,
    max(t4bar) - t4bar2,
    max(t5bar) - t5bar2
]

colors = [
    (230,25,25),
    (25,25,230),
    (25,230,25),
    (230,230,25),
    (25,230,230)
]

tbar2 = [t1bar2, t2bar2, t3bar2, t4bar2, t5bar2]
print([tbar2[i]-emin[i] for i in range(5)])
print(tbar2)
print([emax[i]+tbar2[i] for i in range(5)])

# plt.figure()
# barcon = plt.bar(["Original", "Popularity", "Greed", "Inertia", "All"], [t1bar2, t2bar2, t3bar2, t4bar2, t5bar2])
# for bar, color in zip(barcon, colors):
#     bar.set_facecolor((color[0]/255, color[1]/255, color[2]/255))
# errcon = plt.errorbar(
#     ["Original", "Popularity", "Greed", "Inertia", "All"],
#     [t1bar2, t2bar2, t3bar2, t4bar2, t5bar2],
#     (emin, emax),
#     ecolor=(0,0,0),
#     elinewidth=0.5,
#     fmt=',')
# plt.show()