import graphs
import approx_count_st

if __name__ == "__main__":
    g = graphs.get_random_connected_graph(20, 0.5)
    count = approx_count_st.approx_count_st(g, 1000, 1000)
    print(count)
