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
    def __init__(self, g, mix_time):
        self.g = g
        self.ra = RootedArborescence.random_ra_from_graph(self.g)
        self.mix(mix_time)

    def markov_step(self):
        r = random.random()
        if r < 0.5:
            return
        neighbors = self.g[self.ra.root][:]
        neighbor = random.sample(neighbors, 1)[0]
        del self.ra.parents[neighbor]
        self.ra.parents[self.ra.root] = neighbor
        self.ra.root = neighbor

    def mix(self, mix_time):
        for _ in range(mix_time):
            self.markov_step()

    def ra_to_st(self):
        st = defaultdict(list)
        for v, p in self.ra.parents.items():
            st[v].append(p)
            st[p].append(v)
        return st

    def sample(self):
        self.markov_step()
        return self.ra_to_st()
