import scipy.stats as ss
import numpy as np

import graphs, st_sampler, mc_sampler, mtt

# tests if a sampler gives a uniform sample
# the sampler must be initialized, this fn just calls sampler.sample()
# g must be connected
def test_for_uniform_dist(g, sampler):
    st_counter = graphs.ST_counter() # for counting the number of spanning trees. Inefficient, so mtt(g) must be reasonably small, like < 100

    nst = mtt.MTT(g)
    print(f"nst = {nst}")
    for i in range(100 * nst): # if distr is uniform, we will have about 100 of each spanning tree
        tree = sampler.sample()
        st_counter.add_tree(tree)
    
    print("observed counts:", st_counter.counts)
    t = ss.chisquare(st_counter.counts)
    print(f"Test result: chi statistic = {t[0]}, p-value = {t[1]}")
    if (t[1] < 0.05):
        print("Distribution is probably not uniform")
    else:
        print("Distribution is probably uniform")

def unit_test():
    n = 8
    d = 0.3
    g = graphs.get_random_connected_graph(n, d)
    sampler = st_sampler.STSampler(g)
    test_for_uniform_dist(g, sampler)

if __name__ == "__main__":
    unit_test()