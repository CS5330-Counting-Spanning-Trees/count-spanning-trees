from collections import defaultdict

class Graph:
    def construct_graph(self, adj_list):
        edge_idx = 0
        self.g = defaultdict(list)
        self.edges = {}
        for u in adj_list:
            for v in adj_list[u]:
                if u > v:
                    continue
                # labelled edge in form (neighbor, edge_idx)
                self.g[u].append(edge_idx)
                self.g[v].append(edge_idx)
                self.edges[edge_idx] = (u, v)
                edge_idx += 1

    def __init__(self, adj_list):
        self.construct_graph(adj_list)

    def get_vertices(self):
        return list(self.g.keys())

    def neighbor(self, v, edge_idx):
        (x, y) = self.edges[edge_idx]
        if x != v:
            return x
        return y

    def get_all_edge_indcies(self):
        return list(self.edges.keys())

    def get_edge_indices(self, v):
        return self.g[v]

    def get_edge(self, edge_idx):
        return self.edges[edge_idx]

    def get_edge_between_vertices(self, u, v):
        for edge_idx in self.g[u]:
            if self.neighbor(u, edge_idx) == v:
                return edge_idx
        return None

    def contract(self, edge_idx):
        u, v = self.edges[edge_idx]
        # remove all new self loops
        filtered_u_neighbors = [idx for idx in self.g[u] if self.neighbor(u, idx) != v]
        filtered_v_neighbors = [idx for idx in self.g[v] if self.neighbor(v, idx) != u]
        for idx in self.g[u]:
            if self.neighbor(u, idx) == v:
                del self.edges[idx]

        # collapse v into u
        del self.g[v]
        self.g[u] = filtered_u_neighbors + filtered_v_neighbors
        # update edges for neighbors of v to point to u instead
        for edge_idx in filtered_v_neighbors:
            n = self.neighbor(v, edge_idx)
            self.edges[edge_idx] = (min(u, n), max(u, n))

    def remove_edge(self, edge_idx):
        u, v = self.edges[edge_idx]
        self.g[u].remove(edge_idx)
        self.g[v].remove(edge_idx)
        del self.edges[edge_idx]

    def pprint(self):
        for v in self.g:
            neighbors = []
            for edge_idx in self.g[v]:
                neighbors.append(self.neighbor(v, edge_idx))
            neighbors.sort()
            print(f"{v}: {neighbors}")
        print(f"edges: {self.edges}")

def test_graph():
    adj_list = {1: [2, 3], 2: [1, 3], 3: [1, 2, 4], 4: [3]}
    g = Graph(adj_list)
    print("---initial graph---")
    g.pprint()
    e = g.get_edge_between_vertices(2, 3)
    g.contract(e)
    print("---contract vertex 2 and 3---")
    g.pprint()
    e = g.get_edge_between_vertices(1, 2)
    g.remove_edge(e)
    print("---remove one of the edges between vertex 1 and 2---")
    g.pprint()

if __name__ == "__main__":
    test_graph()
