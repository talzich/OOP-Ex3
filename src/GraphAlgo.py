from typing import List
from DiGraph import DiGraph
from Node import Node
from Edge import Edge
from GraphAlgoInterface import GraphAlgoInterface
import json


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph):
        self.graph = graph

    def load_from_json(self, file_name: str) -> bool:
        if not file_name.endswith(".json"):
            if "." not in file_name:
                file_name += ".json"
            else:
                return False

        if self.graph is not None:
            self.graph.clear_graph()
        else:
            self.graph = DiGraph()

        try:
            json_file = open(file_name, "r")
            json_obj_graph = json.load(json_file)
            nodes = json_obj_graph["nodes"]
            edges = json_obj_graph["edges"]
            mc = json_obj_graph["mc"]

            for node in nodes:
                new_node = Node(node["key"], tuple(node["pos"]), node["tag"], node["weight"], node["info"])
                self.graph.add_node_object(new_node)

            for edge in edges:
                new_edge = Edge(edge["src"], edge["dest"], edge["weight"], edge["tag"], edge["info"])
                self.graph.add_edge_object(new_edge)

            return True

        except IOError as e:
            print(e)
            return False

    def save_to_json(self, file_name: str) -> bool:

        if not file_name.endswith(".json"):
            if "." not in file_name:
                file_name += ".json"
            else:
                return False

        graph_json = {}
        nodes_json = []
        edges_json = []
        keys = self.graph.get_v()
        edges = self.graph.get_e()
        try:
            file = open(file_name, "w")

            for key in keys:
                node = self.graph.get_node(key)
                nodes_json.append(node.to_json())
            graph_json["nodes"] = nodes_json

            for edge in edges:
                edges_json.append(edge.to_json())

            graph_json["edges"] = edges_json
            graph_json["mc"] = self.graph.get_mc()
            graph_json["node size"] = self.graph.v_size()
            graph_json["edge size"] = self.graph.e_size()

            json.dump(graph_json, file)
            return True
        except IOError as e:
            print(e)
            return False

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
node2 = Node(2, (3, 4), 4, 1.2, "yellow")

graph.add_node_object(node0)
graph.add_node_object(node1)
graph.add_node_object(node2)

graph.add_edge(0, 1, 4)
graph.add_edge(2, 1, 2)
graph.add_edge(2, 0, 3)

algo = GraphAlgo(graph)
print(algo.save_to_json("test.json"))

graph.clear_graph()

print(algo.load_from_json("test.json"))
print()