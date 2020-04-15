import random
from collections import defaultdict

def make_complete_graph(n):
    g = defaultdict(list)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            g[i].append(j)
            g[j].append(i)
    return g

def make_random_graph(n, density):
    # we want the graph to be connected, so we start with a spanning tree
    g = make_random_st(n)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if j in g[i]:
                continue
            if random.random() < density:
                g[i].append(j)
                g[j].append(i)
    return g

def make_random_st_dfs(n, v, visited, st):
    visited.add(v)
    # consider all other vertices except v as neighbors
    neighbors = [x if x < v else x + 1 for x in range(n - 1)]
    random.shuffle(neighbors)
    for neighbor in neighbors:
        if neighbor not in visited:
            st[v].append(neighbor)
            st[neighbor].append(v)
            make_random_st_dfs(n, neighbor, visited, st)


def make_random_st(n):
    root = random.randint(0, n - 1)
    visited = set()
    st = defaultdict(list)
    make_random_st_dfs(n, root, visited, st)
    return st
