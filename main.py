import random, math, collections, copy, time
from fractions import Fraction
from decimal import Decimal
from collections import defaultdict
import graphs, st_sampler, mtt, db
import pandas as pd

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
    # root = random.sample(g.keys(), 1)[0]
    # visited = set()
    # st = defaultdict(list)
    # get_initial_st_dfs(g, root, visited, st)
    sampler = st_sampler.STSampler(g)
    return sampler.sample()

def get_remaining_edges(g, st):
    edges = []
    for v, neighbors in g.items():
        for neighbor in neighbors:
            if v > neighbor or neighbor in st[v]: # prevent double counting
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
    while denominator < min_denom: # while denom is too small, take more samples
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
        print(f'len(g) = {len(g)}, term = {float(term)}')
        # actual = nst1 / nst2
        # print('term error:', mult_error(term, actual))
        result *= term
    return result

def approx_count_log(g, num_samples):
    g_i = get_initial_st(g)
    remaining_edges = get_remaining_edges(g, g_i)
    result = Decimal(0) # the initial graph has only 1 st
    for new_edge in remaining_edges:
        # add the remaining edges until we get back the original graph
        u, v = new_edge
        g_i[u].append(v)
        g_i[v].append(u)
        # denominator is the number of samples that are also st for g without the new edge
        term = approx_term_1(g_i, u, v, num_samples)
        termdec = Decimal(term.numerator) / Decimal(term.denominator)
        logterm = termdec.ln()
        print(f'len(g) = {len(g)}, term = {logterm}')
        result += logterm
    return result

# the guess is that O(V) samples is enough
def make_row(n, density, num_samples):
    g = graphs.get_random_connected_graph(n, density)
    
    t0 = time.time()
    est = approx_count_log(g, num_samples)
    t1 = time.time()

    act = mtt.MTT(g, log=True)
    error = mult_error_log(float(est), act)
    print(f'actual = {act}, est = {est}, error = {error}')
    
    row = [n, density, act, float(est), error, t1 - t0]
    return row
    # g = graphs.get_random_connected_graph(50, 0.1)
    # g2 = copy.deepcopy(g)
    # u, v = graphs.pop_random_edge(g2)
    # est = approx_term_2(g, u, v, 300)
    # nst1 = mtt.MTT(g)
    # nst2 = mtt.MTT(g2)
    # act = nst1 / nst2
    # error = mult_error(est, act)
    # print(f'error = {error}')

def gen():
    ns = list(range(30, 420, 20))
    rows = db.load_data('rows2_n.json')
    for n in ns:
        den = 10 / n
        num_samples = int(n)
        r = make_row(n, den, num_samples)
        rows.append(r)
        db.save_data(rows, 'rows2_n.json')

def save_csv():
    rows = db.load_data('rows2_n.json')
    cols = ['n', 'density', 'log act', 'log est', 'error', 'time']
    df = pd.DataFrame(rows, columns=cols)
    print(df)
    df.to_csv('rows2_n.csv')

def get_pts():
    df = pd.read_csv('rows2_10n.csv')
    ex = 'Unnamed: 0'
    del df[ex]
    coords = list(zip(df['n'], df['time']))
    for c in sorted(coords):
        print(c)

if __name__ == "__main__":
    # db.save_data([], 'rows2_nn') # create file
    #gen()
    #save_csv()
    get_pts()
