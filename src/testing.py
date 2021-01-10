import math
import sys
from queue import PriorityQueue
from Node import Node
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo

# node0 = Node(0)
# node1 = Node(1)
# node2 = Node(2)
#
# node0.set_tag(2)
# node1.set_tag(1)
# node2.set_tag(0)
#
# pair1 = (node1.get_tag(), node1)
# pair2 = (node2.get_tag(), node2)
# pair3 = (node0.get_tag(), node0)
# print(pair3[0])
#
# pq = PriorityQueue()
#
# pq.put(pair1)
# pq.put(pair2)
# pq.put(pair3)
#
# d = {}
# empty = not bool(d)
# print(empty)
# print(math.inf)
# while not pq.empty():
#     next = pq.get()
#     print(next)

# graph = DiGraph()
# graph.add_node(0)
# graph.add_node(1)
# graph.add_node(2)
# graph.add_node(3)
# graph.add_node(4)
# graph.add_edge(0, 1, 3)
# graph.add_edge(0, 4, 8)
# graph.add_edge(0, 3, 7)
# graph.add_edge(4, 3, 3)
# graph.add_edge(1, 3, 4)
# graph.add_edge(1, 2, 1)
# graph.add_edge(3, 2, 2)
# graph_algo = GraphAlgo(graph)
# revered_graph = graph_algo.reverse_graph()
# print(revered_graph.get_v())
# print(revered_graph.v_size())

# test for connected_components:
graph1 = DiGraph()
graph1.add_node(0)
graph1.add_node(1)
graph1.add_node(2)
graph1.add_node(3)
graph1.add_node(4)

graph1.add_edge(0, 3, 1)
graph1.add_edge(0, 2, 1)
graph1.add_edge(1, 0, 1)
graph1.add_edge(2, 1, 1)
graph1.add_edge(3, 4, 1)

algo = GraphAlgo(graph1)
print(algo.connected_components())
