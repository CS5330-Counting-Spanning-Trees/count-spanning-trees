from graph import Graph
from random_graphs import get_random_connected_graph
from approx_count_st import approx_count_st
from mtt import MTT

if __name__ == "__main__":
    adj_list = get_random_connected_graph(100, 0.1, 0, max_degree=3)
    g = Graph(adj_list)
    mtt = MTT(adj_list)
    print(mtt)
    count = int(approx_count_st(g))
    print(count)
