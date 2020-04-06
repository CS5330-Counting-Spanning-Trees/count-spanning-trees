# Experiments for approximating the term NST(G_i) / NST(G_{i-1})
import pprint
import copy
import random
from graphs import make_random_graph
from mtt import MTT
from st_sampler import STSampler

def printGraph(g):
    pp = pprint.PrettyPrinter()
    pp.pprint(g)

def num_edges(g): # assumes undirected
    total = 0
    for k, v in g.items():
        total += len(v)
    return total // 2

def randomEdge(g): # chooses a random edge from g
    random_u = random.choice(list(g.keys()))
    random_v = random.choice(g[random_u]) # g[u] is not empty, assuming g is connected
    return (random_u, random_v)

g1 = make_random_graph(15, 0.5)
NST1 = MTT(g1)
g2 = copy.deepcopy(g1)
u, v = randomEdge(g2)
g2[u].remove(v)
NST2 = MTT(g2)
r = NST1 / NST2

sampler = STSampler(g1)
num_samples = 1000
good = 0
for i in range(num_samples):
    print(i)
    t = sampler.sample()
    if not (v in t[u]): # doesnt contains bad edge
        good += 1
r_est = num_samples / good

printGraph(g1)
printGraph(g2)

print('actual = {}; estimated = {}, ratio = {}'.format(r, r_est, r / r_est))

printGraph(g1)
printGraph(g2)

