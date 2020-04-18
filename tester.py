#!/usr/bin/env python3

# contains functions to run tests 
import math, sys
import graphs, mtt, approx_count_st, st_sampler, mc_sampler


# use num_vertices, density, seed to generate a graph deterministically
# use the sampler and num_samples params to approximate the number of spanning tress
# use mtt to compute the correct answer
# return the error (approx - actual) / actual
def get_error(num_vertices, density, seed, num_samples, sampler_type, use_log = False):
    g = graphs.get_random_connected_graph(num_vertices, density) # todo: add seed here
    actual = mtt.MTT(g)  # todo: add use_log
    sampler = None
    if (sampler_type == "st"):
        sampler = st_sampler.STSampler(g)
    elif (sampler_type == "mc"):
        sampler = mc_sampler.MCSampler(g)
    else:
        print("invalid sampler")
        return None
    estimated = approx_count_st.approx_count_st_testing_ver(g, sampler, num_samples, use_log)
    error = abs(actual - estimated) / actual # note that if use_log = True, the error will be log-error also
    return error

def unit_test():
    n = 30
    p = 0.3
    seed = 1
    num_samples = 30
    stsampler = "st"
    mcsampler = "mc" # currently, mc does not yet work, because need supply the number of rounds.
    use_log = False
    for n in range(30, 80, 10):
        error = get_error(n, p, seed, num_samples, stsampler, use_log)
        print(error)
    # for n in range(30, 80, 10):
    #     error = get_error(n, p, seed, num_samples, mcsampler, use_log)
    #     print(error)
    

# unit_test()

# usage:
# python3 tester.py n density seed num_samples sampler_type use_log
# e.g.
# python3 tester.py 30 0.5 123 100 st False
if __name__ == "__main__":
    _, n, density, seed, num_samples, sampler_type, use_log = sys.argv
    n = int(n)
    density = float(density)
    seed = int(seed)
    num_samples = int(num_samples)
    error = get_error(n, density, seed, num_samples, sampler_type, use_log == "True")
    print(f"error = {error}")