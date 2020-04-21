import random
from graph import Graph
from collections import defaultdict

# class to sample random spanning trees
class STSampler:
    def __init__(self, g):
        self.graph = g

    # erase loops in a walk
    def erase_loops(self, walk):
        res = []
        seen = {}
        for step in walk:
            v, _ = step
            if v not in seen:
                seen[v] = len(res)
                res.append(step)
                continue
            # we have come across v before, so there is a loop
            res, to_remove = res[: seen[v] + 1], res[seen[v] + 1:]
            for u, _ in to_remove:
                del seen[u]
        return res

    # starting from u, do a random walk until we meet the tree
    # assumes that u is not already part of the tree
    def walk_to_tree(self, u, tree_get_vertices):
        walk = [(u, None)]
        while True:
            v, _ = walk[-1]
            if v in tree_get_vertices:
                # walk has reached the tree
                break
            edge_idx = random.choice(self.graph.get_edge_indices(v))
            neighbor = self.graph.neighbor(v, edge_idx)
            # record each step in the path as (vertex, idx of edge taken to reach vertex)
            step = (neighbor, edge_idx)
            walk.append(step)
        return walk

    # adds the found path to the tree
    def add_to_tree(self, tree_get_vertices, tree_edges, path):
        for step in path:
            v, edge_idx = step
            tree_get_vertices.add(v)
            if edge_idx is not None:
                # the first step in the path does not have an edge taken
                tree_edges.append(edge_idx)

    # returns a ST uniformly distributed
    # implements Wilson's algorithm
    # returns the edges used to construct the ST
    def sample(self):
        unused = set(self.graph.get_vertices())
        root = unused.pop() # choose last elem to be the root, choice of root does not matter
        tree_get_vertices = set([root]) # initially only the root is in the tree
        tree_edges = []

        while len(unused) > 0:
            u = random.sample(unused, 1)[0]
            walk = self.walk_to_tree(u, tree_get_vertices)
            path = self.erase_loops(walk)
            self.add_to_tree(tree_get_vertices, tree_edges, path)
            unused = unused - tree_get_vertices

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
    assert(is_st(g, st))


if __name__ == "__main__":
    test_st_sampler()
