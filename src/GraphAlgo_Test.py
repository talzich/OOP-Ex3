from DiGraph import DiGraph
from GraphAlgo import GraphAlgo

graph = DiGraph()

graph.add_node(0)
graph.add_node(1)
graph.add_node(2)
graph.add_node(3)
graph.add_node(4)
graph.add_node(5)
graph.add_node(6)
graph.add_node(7)
graph.add_node(8)

graph.add_edge(0, 1, 4)
graph.add_edge(1, 0, 4)
graph.add_edge(0, 7, 8)
graph.add_edge(7, 0, 8)
graph.add_edge(1, 7, 11)
graph.add_edge(7, 1, 11)
graph.add_edge(1, 2, 8)
graph.add_edge(2, 1, 8)
graph.add_edge(2, 3, 7)
graph.add_edge(3, 2, 7)
graph.add_edge(2, 5, 4)
graph.add_edge(5, 2, 4)
graph.add_edge(3, 4, 9)
graph.add_edge(4, 3, 9)
graph.add_edge(2, 8, 2)
graph.add_edge(8, 2, 2)
graph.add_edge(7, 8, 7)
graph.add_edge(8, 7, 7)
graph.add_edge(6, 8, 6)
graph.add_edge(8, 6, 6)
graph.add_edge(4, 5, 10)
graph.add_edge(5, 4, 10)
graph.add_edge(5, 6, 2)
graph.add_edge(6, 5, 2)
graph.add_edge(3, 5, 14)
graph.add_edge(5, 3, 14)
graph.add_edge(6, 7, 1)
graph.add_edge(7, 6, 1)

algo = GraphAlgo(graph)
i = 1
while i <= 8:
    print(algo.shortest_path(0,i))
    i += 1