import numpy as np
import graphs
import random
import mtt

def analyze_graph(n, density, seed):
    g = graphs.get_random_connected_graph(n, density, seed)
    degrees = get_degrees(g)
    min_degree = min(degrees)
    max_degree = max(degrees)
    degree_var = np.var(degrees)
    hit_rate = get_hit_rate(g, 10, n)
    num_st = mtt.MTT(g)
    pretty_print(n, density, seed, min_degree, max_degree, degree_var, hit_rate, num_st)

def pretty_print(n, density, seed, min_degree, max_degree, degree_var, hit_rate, num_st):
    print(f"n: {n}, density: {density}, seed: {seed}, min_degree: {min_degree}, max_degree: {max_degree}, degree_var: {degree_var}, hit_rate: {hit_rate}, num_st: {num_st}")

def get_degrees(g):
    d = []
    for neighbors in g.values():
        degree = len(neighbors)
        d.append(degree)
    return d

# do a random walk on the graph and see what percentage of the graph we hit
# this is our attempt at a cheap heuristic to determine the cover time
def get_hit_rate(g, iterations, steps):
    hit_rates = []
    for _ in range(iterations):
        hit = set()
        v = random.sample(g.keys(), 1)[0]
        hit.add(v)
        for _ in range(steps):
            v = random.sample(g[v], 1)[0]
            hit.add(v)
        hit_rate = len(hit) / len(g)
        hit_rates.append(hit_rate)
    return np.mean(hit_rates)

if __name__ == "__main__":
    analyze_graph(10, 0.5, 1)
