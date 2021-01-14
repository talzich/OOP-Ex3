from GraphAlgo import GraphAlgo
import timeit


def compare_scc(algo: GraphAlgo, laps):

    times = []
    sum_times = 0

    for i in range(laps):
        start = timeit.default_timer()
        algo.connected_component(5)
        time = timeit.default_timer() - start
        sum_times += time
        times.append(time)

    min_time = min(times)
    max_time = max(times)
    avg = sum_times/laps
    return "{:.4f}".format(min_time), "{:.4f}".format(max_time), "{:.4f}".format(avg)






if __name__ == '__main__':

    algo = GraphAlgo()
    algo.load_from_json("../Graphs_on_circle/G_10000_80000s_1.json")

    print(compare_scc(algo, 10))

    # keys = list(algo.get_graph().get_all_v().keys())
    # last_node = keys[len(keys) - 1]
    #
    # laps = 100
    # start = timeit.default_timer()
    # for i in range(laps):
    #     algo.connected_components()
    #
    # total_time = timeit.default_timer() - start
    # print(algo.connected_components())
    # print(total_time / laps)
