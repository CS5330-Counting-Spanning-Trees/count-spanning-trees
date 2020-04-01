import random
from collections import defaultdict


class RootedArborescence():
    def __init__(self, root, parents):
        self.root = root
        self.parents = parents

    @staticmethod
    def random_ra_from_graph_dfs(g, v, visited, parents):
        visited.add(v)
        neighbors = g[v][:]
        random.shuffle(neighbors)
        for neighbor in neighbors:
            if neighbor not in visited:
                parents[neighbor] = v
                RootedArborescence.random_ra_from_graph_dfs(
                    g, neighbor, visited, parents)

    @staticmethod
    def random_ra_from_graph(g):
        root = random.sample(g.keys(), 1)[0]
        visited = set()
        parents = {}
        RootedArborescence.random_ra_from_graph_dfs(g, root, visited, parents)
        ra = RootedArborescence(root, parents)
        return ra

    def __repr__(self):
        return f"({self.root}, {self.parents})"


class MCSampler():
    def __init__(self, g):
        self.g = g

    def markov_step(self, ra):
        r = random.random()
        if r < 0.5:
            return self
        neighbors = self.g[ra.root][:]
        neighbor = random.sample(neighbors, 1)[0]
        del ra.parents[neighbor]
        ra.parents[ra.root] = neighbor
        ra.root = neighbor

    def sample(self, rounds):
        ra = RootedArborescence.random_ra_from_graph(self.g)
        for _ in range(rounds):
            self.markov_step(ra)
        st = defaultdict(list)
        for v, p in ra.parents.items():
            st[v].append(p)
            st[p].append(v)
        return st
