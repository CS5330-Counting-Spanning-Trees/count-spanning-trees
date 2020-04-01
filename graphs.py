import random
from collections import defaultdict

def make_complete_graph(n):
    return make_random_graph(n, 1)

def make_random_graph(n, density):
    g = defaultdict(list)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if random.random() < density:
                g[i].append(j)
    return g
