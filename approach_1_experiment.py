import random, math, collections, copy, time
from fractions import Fraction
from decimal import Decimal
from collections import defaultdict
import random_graphs, st_sampler, mtt, db
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
# take 5 samples
# discard outliers
# take average of last 3
def approx_term_2(g, u, v, num_samples):
    num_runs = 10
    num_discard = 2

    runs = []
    for run in range(num_runs):
        runs.append(approx_term_1(g, u, v, num_samples))

    runs = sorted(runs)[num_discard : -num_discard]
    return sum(runs) / len(runs)

def approx_count(g, num_samples):
    g_i = get_initial_st(g)
    remaining_edges = get_remaining_edges(g, g_i)
    # the initial graph has only 1 st
    result = 1
    for new_edge in remaining_edges:
        # add the remaining edges until we get back the original graph
        u, v = new_edge
        g_i[u].append(v)
        g_i[v].append(u)
        # denominator is the number of samples that are also st for g without the new edge
        # term = math.log(approx_term_1(g_i, u, v, num_samples), math.e)
        term = approx_term_1(g_i, u, v, num_samples)
        print(f'len(g) = {len(g)}, term = {float(term)}')
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

def approx_count_log_modified(g, num_samples):
    g_i = get_initial_st(g)
    remaining_edges = get_remaining_edges(g, g_i)
    result = Decimal(0) # the initial graph has only 1 st
    for new_edge in remaining_edges:
        # add the remaining edges until we get back the original graph
        u, v = new_edge
        g_i[u].append(v)
        g_i[v].append(u)
        # denominator is the number of samples that are also st for g without the new edge
        term = approx_term_2(g_i, u, v, num_samples)
        termdec = Decimal(term.numerator) / Decimal(term.denominator)
        logterm = termdec.ln()
        print(f'len(g) = {len(g)}, term = {logterm}')
        result += logterm
    return result

def make_row(n, density, num_samples):
    g = random_graphs.get_random_connected_graph(n, density)

    t0 = time.time()
    est = approx_count_log(g, num_samples)
    t1 = time.time()

    act = mtt.MTT(g, log=True)
    error = mult_error_log(float(est), act)
    print(f'actual = {act}, est = {est}, error = {error}')

    row = [n, density, act, float(est), error, t1 - t0]
    return row

def make_row_modified(n, density, num_samples):
    g = random_graphs.get_random_connected_graph(n, density)

    t0 = time.time()
    est = approx_count_log_modified(g, num_samples) # uses a different way of approx each term
    t1 = time.time()

    act = mtt.MTT(g, log=True)
    error = mult_error_log(float(est), act)
    print(f'actual = {act}, est = {est}, error = {error}')

    row = [n, density, act, float(est), error, t1 - t0]
    return row


fjson = 'rows2_10n_modified.json' # filename for saving generated data
fcsv = 'rows2_10n_modified.csv'
def gen():
    ns = list(range(30, 420, 20))
    rows = db.load_data(fjson)
    for n in ns:
        den = 10 / n
        num_samples = int(n)
        r = make_row_modified(n, den, num_samples)
        rows.append(r)
        db.save_data(rows, fjson)

def save_csv():
    rows = db.load_data(fjson)
    cols = ['n', 'density', 'log act', 'log est', 'error', 'time']
    df = pd.DataFrame(rows, columns=cols)
    print(df)
    df.to_csv(fcsv)

def get_pts():
    df = pd.read_csv(fcsv)
    ex = 'Unnamed: 0'
    del df[ex]
    coords = list(zip(df['n'], df['error']))
    for c in sorted(coords):
        print(c)

if __name__ == "__main__":
    get_pts()
