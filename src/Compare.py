from GraphAlgo import GraphAlgo
import timeit

if __name__ == '__main__':

    algo = GraphAlgo()
    algo.load_from_json("../Graphs_on_circle/G_30000_240000_1.json")
    keys = list(algo.get_graph().get_all_v().keys())
    last_node = len(keys) - 1

    laps = 100
    start = timeit.default_timer()
    for i in range(laps):
        algo.connected_components()

    total_time = timeit.default_timer() - start
    print(algo.connected_components())
    print(total_time / laps)
