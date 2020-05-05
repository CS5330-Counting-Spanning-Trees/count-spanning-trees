import random
import random_graphs

def random_walk(g):
    steps = 0
    vertices = g.keys()
    v = random.sample(vertices, 1)[0]
    visited = set([v])
    while len(visited) < len(vertices):
        neighbors = g[v]
        neighbor = random.sample(neighbors, 1)[0]
        visited.add(neighbor)
        v = neighbor
        steps += 1
    return steps

def test(n):
    sum = 0
    for _ in range(100):
        g = random_graphs.get_random_connected_graph(n, 0.1, max_degree=5)
        sum += random_walk(g)
    return sum / 100


if __name__ == "__main__":
    for n in [10, 100, 1000]:
        steps = test(n)
        print(f"n: {n}, steps: {steps}")
