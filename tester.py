# contains functions to run tests 
import math
import graphs, mtt, approx_count_st, st_sampler, mc_sampler


# use num_vertices, density, seed to generate a graph deterministically
# use the sampler and num_samples params to approximate the number of spanning tress
# use mtt to compute the correct answer
# return the error (approx - actual) / actual
def get_error(num_vertices, density, seed, num_samples, sampler_name, use_log = False):
    g = graphs.get_random_connected_graph(num_vertices, density) # todo: add seed here
    actual = mtt.MTT(g)  # todo: add use_log
    sampler = None
    if (sampler_name == "st"):
        sampler = st_sampler.STSampler(g)
    elif (sampler_name == "mc"):
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

