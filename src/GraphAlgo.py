from typing import List
from DiGraph import DiGraph
from Node import Node
from GraphAlgoInterface import GraphAlgoInterface
import json


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph):
        self.graph = graph

    def load_from_json(self, file_name: str) -> bool:
        pass

    def save_to_json(self, file_name: str) -> bool:

        if not file_name.endswith(".json"):
            if "." not in file_name:
                file_name += ".json"
            else:
                return False

        graph_json = {}
        nodes_json = {}
        edges_json = {}
        keys = self.graph.get_v()
        edges = self.graph.get_e()
        file = open(file_name, "w")

        for key in keys:
            node = self.graph.get_node(key)
            nodes_json[key] = node.to_json()
        graph_json["nodes"] = nodes_json

        i = 0
        for edge in edges:
            edges_json[i] = edge.to_json()
            i += 1
        graph_json["edges"] = edges_json

        json.dump(graph_json, file)
        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass


graph = DiGraph()
node0 = Node(0, (1, 2), 1, 5, "black")
node1 = Node(1, (2, 3), 2, 4.5, "White")
node2 = Node(2, (3, 4), 4, 1.2, "pink")

graph.add_node_object(node0)
graph.add_node_object(node1)
graph.add_node_object(node2)

graph.add_edge(0, 1, 4)
graph.add_edge(2, 1, 2)
graph.add_edge(2, 0, 3)

algo = GraphAlgo(graph)
print(algo.save_to_json("test.json"))
