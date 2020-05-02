import random, math, collections
from fractions import Fraction
from collections import defaultdict
from mc_sampler import MCSampler
import graphs, st_sampler, mtt

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

def approx_count_st(g, rounds, samples):
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
        denominator = 0
        for _ in range(samples):
            sampler = MCSampler(g_i)
            sample = sampler.sample(rounds)
            if u not in sample[v]:
                denominator += 1
        result *= Fraction(samples, denominator)
    return float(result)

# approximates the number of spanning trees of the graph
# uses the given sampler, and draws num_samples to approximate the increase in number of st each time we add an edge
def approx_count_st_testing_ver(g, sampler, num_samples, use_log):
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
        denominator = 0
        for _ in range(num_samples):
            sampler.set_graph(g_i)
            sample = sampler.sample()
            if u not in sample[v]:
                denominator += 1
        result *= Fraction(num_samples, denominator)

    base = math.e # todo: what is the base of the log
    if (use_log):
        return math.log(result, base)
    else:
        return float(result)

# some helper fns for approx_count_st_generic

# adds a list of edges to the graph
# edge_list is a list of 2-tuple (u, v)
# note: does not check whether the edges already exist in graph!
def add_edges(graph, edge_list):
    for u, v in edge_list:
        graph[u].append(v) # add edge to graph
        graph[v].append(u)

# check if graph contains edges in edge_list
# assumes graph is undirected
def contains_any_edges(graph, edge_list):
    for u, v in edge_list:
        if v in graph[u]:
            return True
    return False

# more generic vesion of approx_count
# vary the number of samples and number of edges to add 
# both functions take in the number of vertices in g, and number of edges in g, and returns a integer
# warning: depending on the functions you give, can becomes extremely slow, so test first!
def approx_count_st_generic(g, sampler, num_samples_fn, num_edges_each_time_fn, use_log):
    n = len(g)
    e = n-1 # tracks the number of edges currently in g_i
    g_i = get_initial_st(g)
    # assert(graphs.is_connected(g_i))
    remaining_edges = get_remaining_edges(g, g_i)
    
    result = 1 # the initial graph has only 1 st
    iterations = 1 # track number of iterations for debug
    num_samples_record = [] # tracks num_samples at each iteration
    while len(remaining_edges) > 0:
        num_add = min(num_edges_each_time_fn(n, e), len(remaining_edges))
        edges_to_add = remaining_edges[-num_add : ] # get the last few edges
        remaining_edges = remaining_edges[ : -num_add] # exclude last few edges
            
        add_edges(g_i, edges_to_add)
        e += num_add

        # approximate the increase in number of spanning trees
        denominator = 0 # denominator is the number of samples that are also st for g without the new edges
        num_samples = num_samples_fn(n, e)
        for _ in range(num_samples):
            #print(f'iteration = {iterations}, sample = {_}')
            sampler.set_graph(g_i)
            sample = sampler.sample()
            if not contains_any_edges(sample, edges_to_add):
                denominator += 1
        num_samples_record.append(num_samples)

        if denominator == 0: # we cannot proceed unless we take more samples, so repeat until denom not zero
            print("entering sampling loop")
            while(denominator == 0):
                num_samples_record[-1] += 1
                sampler.set_graph(g_i)
                sample = sampler.sample()
                if not contains_any_edges(sample, edges_to_add):
                    denominator += 1

        result *= Fraction(num_samples_record[-1], denominator)
        #print(Fraction(num_samples, denominator))
        iterations += 1

    # print(num_samples_record)
    base = math.e # todo: what is the base of the log
    if (use_log):
        return math.log(result, base)
    else:
        return float(result)


def unit_test_1():
    n = 10
    p = 0.3
    seed = 1
    g = graphs.get_random_connected_graph(n, p) # todo: add seed
    num_samples = 100

    sampler = st_sampler.STSampler({}) # empty sampler, it will be initialized within fn later
    use_log = False
    
    nst = approx_count_st_testing_ver(g, sampler, num_samples, use_log)
    print(nst)

def unit_test_2():
    n = 30
    p = 0.3
    seed = 1
    g = graphs.get_random_connected_graph(n, p) # todo: add seed
    
    sampler = st_sampler.STSampler({}) # empty sampler, it will be initialized within fn later
    num_edges_each_time_fn_1 = lambda x, y: 1 # one edge each time
    num_samples_fn_1 = lambda x, y: 200 # 100 samples each time
    num_edges_each_time_fn_2 = lambda x, y: 3 # 3 edges each time
    num_samples_fn_2 = lambda x, y: 100 + 30*y # 100 samples as base, and for every edge, add 10 samples
    use_log = False
    
    nst = approx_count_st_generic(g, sampler, num_samples_fn_2, num_edges_each_time_fn_2, use_log)
    actual = mtt.MTT(g)
    print('error =', abs(nst - actual) / actual)


def get_expansion_factor(c):
    T = sum(c.values())
    exp = 0
    for di in c:
        exp += c[di] * pow(2, di)
    return Fraction(exp, T)
    

# approx counts the number of st of g
# will modify g
def approx_count(g, M1, M2):
    if (graphs.num_edges(g) == len(g) - 1):
        return 1
    # pick first edge of g
    #u = next(iter(g.keys()))
    #v = g[u][0] # possible because g connected
    # get random edge
    u, v = graphs.get_random_edge(g)

    # draw M1 samples to decide which case
    sampler = st_sampler.STSampler(g)
    has_e = 0
    
    for i in range(M1):
        sample = sampler.sample()
        if v in sample[u]:
            has_e += 1
        
    print(f'has_e = {has_e}')
    # decide if proportion of has_e > 0.5
    if (2 * has_e > M1):
        both_nbrs = set(g[v]).intersection(set(g[u])) # a vertex is a double if it is in this set
        # contract g
        graphs.contract(g, (u, v))

        # we need to do some extra estimation, because st of the contracted g can be expanded in many ways
        sampler = st_sampler.STSampler(g)
        counter = collections.Counter() # counts freq of doubles
        for i in range(M2):
            sample = sampler.sample()
            num_doubles = len(set(sample[u]).intersection(both_nbrs)) # u is now the node (u+v)
            counter[num_doubles] += 1
        exp = get_expansion_factor(counter)
        print(f'exp factor = {exp}')

        nst = mtt.MTT(g)
        rec = approx_count(g, M1, M2)
        est = rec
        error = abs(est - nst) / nst * 100
        print(f'actual = {nst}, estimated = {est}, error = {error}')

        return rec * exp * M1 / has_e
    else:
        # delete e and recurse
        g[u].remove(v)
        g[v].remove(u)
        nst = mtt.MTT(g)
        rec = approx_count(g, M1, M2)
        est = rec
        error = abs(est - nst) / nst * 100
        print(f'actual = {nst}, estimated = {est}, error = {error}')

        return rec * M1 / (M1 - has_e)

# approx counts the number of st of g
# will modify g
def approx_count_iter(g, M1, M2):
    est = 1 # accumulates the multiplers here

    while (graphs.num_edges(g) > len(g) - 1): # while we dont have a spanning tree
        u, v = graphs.get_random_edge(g)
        # draw M1 samples to decide which how to reduce the graph
        sampler = st_sampler.STSampler(g)
        has_e = 0

        for i in range(M1):
            sample = sampler.sample()
            if v in sample[u]:
                has_e += 1
        print(f'has_e / M1 = {has_e}/{M1}')

        # decide which of the 2 reductions to use
        if (2 * has_e > M1): # has_e > 0.5
            both_nbrs = set(g[v]).intersection(set(g[u])) # a vertex is a double if it is in this set
            graphs.contract(g, (u, v))

            #we need to do some extra estimation, because st of the contracted g can be expanded in many ways
            sampler = st_sampler.STSampler(g)
            counter = collections.Counter() # counts freq of doubles
            for i in range(M2):
                sample = sampler.sample()
                num_doubles = len(set(sample[u]).intersection(both_nbrs)) # u is now the node (u+v)
                counter[num_doubles] += 1
            exp = get_expansion_factor(counter)

            print('num_bad =', len(both_nbrs))
            print(counter)
            print(f'exp_factor = {exp.numerator / exp.denominator}')
            if (exp > 1):
                print('*' * 50)

            # some debug info
            est *= Fraction(M1, has_e) * exp
        else:
            # delete e and recurse
            g[u].remove(v)
            g[v].remove(u)
            est *= Fraction(M1, M1 - has_e)
    return round(est)

def test():
    g = graphs.get_random_connected_graph(20, 0.6)
    nst = mtt.MTT(g)
    est = approx_count_iter(g, 300, 300)
    error = abs(est - nst) / nst * 100
    print(f'Final: actual = {nst}, estimated = {est}, error = {error}')

if __name__ == "__main__":   
    test()