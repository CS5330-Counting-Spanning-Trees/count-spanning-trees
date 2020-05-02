import random, math, collections
from fractions import Fraction
from collections import defaultdict
import graphs, st_sampler, mtt

def mult_error(est, actual):    
    return (est - actual) / actual

def mult_error_log(log_est, log_actual):
    return pow(math.e, log_est - log_actual) - 1

def get_initial_st_dfs(g, v, visited, st):
    visited.add(v)
    neighbors = g[v][:]
    random.shuffle(neighbors)
    for neighbor in neighbors:
        if neighbor not in visited:
            st[neighbor].append(v)
            st[v].append(neighbor)
            get_initial_st_dfs(g, neighbor, visited, st)

def get_initial_st(g):
    root = random.sample(g.keys(), 1)[0]
    visited = set()
    st = defaultdict(list)
    get_initial_st_dfs(g, root, visited, st)
    return st

def get_remaining_edges(g, st):
    edges = []
    for v, neighbors in g.items():
        for neighbor in neighbors:
            if v > neighbor:
                # every edge is represented twice in g
                # to avoid double counting, we only consider edges for v < neighbor
                continue
            if neighbor in st[v]:
                # don't include edges in the st
                continue
            edge = (v, neighbor)
            edges.append(edge)
    random.shuffle(edges)
    return edges

def approx_term_1(g, u, v, num_samples):
    min_denom = 5
    sampler = st_sampler.STSampler(g)
    denominator = 0
    for _ in range(num_samples):
        sample = sampler.sample()
        if u not in sample[v]:
            denominator += 1
    while denominator < min_denom: # while denom is too small
        sample = sampler.sample()
        if u not in sample[v]:
            denominator += 1
        num_samples += 1
    return Fraction(num_samples, denominator)

# a more complex approximation of each term
# take 10 samples
# discard outliers
# take average
def approx_term_2(g, u, v, num_samples):
    num_runs = 5
    num_discard = 1
    runs = []
    sampler = st_sampler.STSampler({})
    denominator = 0

    for r in range(num_runs):
        denominator = 0
        for _ in range(num_samples):
            sampler.set_graph(g)
            sample = sampler.sample()
            if u not in sample[v]:
                denominator += 1
        while denominator < 5: # while denom is too small
            sampler.set_graph(g)
            sample = sampler.sample()
            if u not in sample[v]:
                denominator += 1
        runs.append(Fraction(num_samples, denominator))

    runs = sorted(runs)[num_discard : -num_discard]
    return sum(runs) / (num_runs - 2 * num_discard)

def approx_count(g, num_samples):
    g_i = get_initial_st(g)
    remaining_edges = get_remaining_edges(g, g_i)
    sampler = st_sampler.STSampler({})
    # the initial graph has only 1 st
    result = 1
    for new_edge in remaining_edges:
        #nst2 = mtt.MTT(g_i)
        # add the remaining edges until we get back the original graph
        u, v = new_edge
        g_i[u].append(v)
        g_i[v].append(u)
        #nst1 = mtt.MTT(g_i)
        # denominator is the number of samples that are also st for g without the new edge
        # term = math.log(approx_term_1(g_i, u, v, num_samples), math.e)
        term = approx_term_1(g_i, u, v, num_samples)
        print(f'len(g) = {len(g)}, term = {term}')
        # actual = nst1 / nst2
        # print('term error:', mult_error(term, actual))
        result *= term
    return result

# the guess is that O(V) samples is enough
def test():
    filename = 'overnight2.json'

    ns = [50]
    for n in ns:
        den = 0.2
        g = graphs.get_random_connected_graph(n, den)

        est = int(approx_count(g, 200))
        act = mtt.MTT(g, log=False)

        error = mult_error(est, act)
        print(f'actual = {act}, est = {est}, error = {error}')



if __name__ == "__main__":
    test()
