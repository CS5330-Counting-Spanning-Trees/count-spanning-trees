from graph import Graph
from random_graphs import get_random_connected_graph
from approx_count_st_mtt import approx_count_st
from mtt import MTT
import time

def count_mtt(adj_list):
    mtt_start = time.time_ns()
    mtt = MTT(adj_list, use_log=True)
    mtt_end = time.time_ns()
    mtt_time = mtt_end - mtt_start
    print(f"{mtt} ({mtt_time} ns)")


def count_approx(adj_list):
    g = Graph(adj_list)
    count_start = time.time_ns()
    count = approx_count_st(g)
    count_end = time.time_ns()
    count_time = count_end - count_start
    print(f"{count} ({count_time} ns)")

def run_compare():
    adj_list = get_random_connected_graph(50000, 0.1, 0, max_degree=5)
    # count_mtt(adj_list)
    count_approx(adj_list)

if __name__ == "__main__":
    run_compare()
