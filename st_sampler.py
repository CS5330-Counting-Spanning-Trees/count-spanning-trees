import random
import time
from graph import Graph
from random_graphs import get_random_connected_graph
from collections import defaultdict


# class to sample random spanning trees
class STSampler:
    def __init__(self, g):
        self.g = g

    # returns a ST uniformly distributed
    # uses the random walk algorithm
    # returns the edges used to construct the ST
    def sample(self):
        g_vertices = self.g.get_vertices()
        v = g_vertices[0]
        tree_vertices = set([v]) # initially only the root is in the tree
        tree_edges = []

        while len(tree_vertices) < len(g_vertices):
            edges = self.g.get_edge_indices(v)
            edge = random.choice(edges)
            neighbor = self.g.neighbor(v, edge)
            if neighbor not in tree_vertices:
                tree_edges.append(edge)
                tree_vertices.add(neighbor)
            v = neighbor

        return tree_edges

# Testing functions

def to_adj_list(g, edges):
    adj_list = defaultdict(list)
    for edge_idx in edges:
        u, v = g.edges[edge_idx]
        adj_list[u].append(v)
        adj_list[v].append(u)
    return adj_list

def is_st(g, edges):
    adj_list = to_adj_list(g, edges)
    g_vertices = g.get_vertices()
    v = g_vertices[0]
    stack = [v]
    visited = set([v])
    while len(stack) > 0:
        v = stack.pop()
        for nbr in adj_list[v]:
            if nbr in visited:
                continue
            visited.add(nbr)
            stack.append(nbr)

    for v in g_vertices:
        if v not in visited:
            print("error: st is not connected")
            return False

    if len(edges) != len(g_vertices) - 1:
        print("error: wrong number of edges")

    # if the graph is connected and it has n - 1 edges,
    # then it is an st
    return True

def test_st_sampler():
    adj_list = {}
    adj_list[1] = [2, 4]
    adj_list[2] = [1, 3, 4]
    adj_list[3] = [2, 4, 6]
    adj_list[4] = [1, 2, 3, 5]
    adj_list[5] = [4, 6]
    adj_list[6] = [3, 5]
    g = Graph(adj_list)
    sampler = STSampler(g)
    st = sampler.sample()
    assert (is_st(g, st))

def test_performance():
    g = Graph(get_random_connected_graph(100, 0.1, 0))
    sampler = STSampler(g)
    start = time.time_ns()
    for _ in range(1000):
        sampler.sample()
    end = time.time_ns()
    elapsed = end - start
    print(f"STSampler took {elapsed} ns for 1000 samples")


if __name__ == "__main__":
    test_st_sampler()
    test_performance()
