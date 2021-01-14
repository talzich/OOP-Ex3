from GraphAlgo import GraphAlgo
import timeit


def compare_scc(g_algo: GraphAlgo, laps):
    times = []
    sum_times = 0

    for i in range(laps):
        start = timeit.default_timer()
        s = g_algo.connected_component(5)
        time = timeit.default_timer() - start
        sum_times += time
        times.append(time)

    min_time = min(times)
    max_time = max(times)
    avg = sum_times/laps
    print("SCC of vertex 0 is:", s)
    return "Min Time: " + "{:.6f}".format(min_time) + " Max Time: " + "{:.6f}".format(max_time) + " Avg Time: " + \
           "{:.6f}".format(avg)


def compare_sccs(g_algo: GraphAlgo, laps):

    times = []
    sum_times = 0

    for i in range(laps):
        start = timeit.default_timer()
        s = g_algo.connected_components()
        time = timeit.default_timer() - start
        sum_times += time
        times.append(time)

    min_time = min(times)
    max_time = max(times)
    avg = sum_times/laps
    print("All Scc's in the Graph:", s)
    return "Min Time: " + "{:.6f}".format(min_time) + " Max Time: " + "{:.6f}".format(max_time) + " Avg Time: " + \
           "{:.6f}".format(avg)


def compare_shortest_path(g_algo: GraphAlgo, laps):

    curr_graph = g_algo.get_graph()
    keys = list(curr_graph.get_all_v().keys())
    min_node = min(keys)
    max_node = max(keys)

    times = []
    sum_times = 0

    for i in range(laps):
        start = timeit.default_timer()
        s = g_algo.shortest_path(min_node, max_node)
        time = timeit.default_timer() - start
        sum_times += time
        times.append(time)

    min_time = min(times)
    max_time = max(times)
    avg = sum_times/laps
    print("Shortest Path between src:", min_node, "and dest:", max_node, "is:" + str(s))
    return "Min Time: " + "{:.6f}".format(min_time) + " Max Time: " + "{:.6f}".format(max_time) + " Avg Time: " + \
           "{:.6f}".format(avg)


if __name__ == '__main__':

    graph = "../Graphs_on_circle/G_10000_80000_1.json"
    algo = GraphAlgo()
    algo1 = GraphAlgo()
    algo2 = GraphAlgo()

    # algo.load_from_json(graph)
    # print("\n********** Start of Testing SCC **********\n")
    # print('\n', compare_scc(algo, 10), '\n')
    # print("********** End of Testing SCC **********\n\n")
    #
    # algo1.load_from_json(graph)
    # print("********** Start of Testing SCC's **********\n")
    # print('\n', compare_sccs(algo1, 10), '\n')
    # print("********** End of Testing SCC's **********\n\n")

    algo2.load_from_json(graph)
    print("********** Start of Testing Shortest Path **********\n")
    print('\n', compare_shortest_path(algo2, 10), '\n')
    print("********** End of Testing Shortest Path **********\n\n")



