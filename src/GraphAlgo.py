import sys
from typing import List
from DiGraph import DiGraph
from Node import Node
from Edge import Edge
from GraphAlgoInterface import GraphAlgoInterface
import json
from queue import PriorityQueue
import math


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph):
        self.graph = graph
        self.parents = {}
        self.unvisited = 1
        self.visited = 0

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
        src = self.graph.get_node(id1)
        dest = self.graph.get_node(id2)

        if src is None or dest is None:
            return (float("inf"), [])
        elif id1 == id2:
            return (0, [id1])

        self.set_infinity_weight()
        self.set_unvisited()
        self.dijkstra(src)

        if dest.get_weight() == float("inf"):
            return (float("inf"), [])

        child = id2
        path = [child]

        while True:
            father = self.parents[child]
            path.append(father)
            if father == id1:
                break
            child = father

        path.reverse()
        return (dest.get_weight(), path)

    def dijkstra(self, src: Node):
        pq = PriorityQueue()

        src.set_weight(0.0)
        pq.put((src.get_weight(), src))
        src.set_tag(self.visited)

        while not pq.empty():
            cur_pair = pq.get()
            src = cur_pair[1]
            src.set_tag(self.visited)

            if src.get_out() is None or not bool(src.get_out()):
                continue

            for edge in src.get_out().values():
                dest_node = self.graph.get_node(edge.get_dest())
                path_weight = src.get_weight() + edge.get_weight()

                if dest_node.get_weight() > path_weight:
                    dest_node.set_weight(path_weight)

                    self.parents[dest_node.get_key()] = src.get_key()

                if dest_node.get_tag() == self.unvisited:
                    pq.put((dest_node.get_weight(), dest_node))

    def set_infinity_weight(self):
        for key in self.graph.get_v():
            node = self.graph.get_node(key)
            node.set_weight(float("inf"))

    def set_unvisited(self):
        for key in self.graph.get_v():
            node = self.graph.get_node(key)
            node.set_tag(self.unvisited)


    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass

    # def shortest_path_dist(self, src: int, dest: int):
    #     if self.graph is None or self.graph.v_size == 0:
    #         return -1
    #
    #     if src == dest:
    #         return 0
    #
    #     src_node = self.graph.get_node(src)
    #     dest_node = self.graph.get_node(dest)
    #
    #     if src_node is None or dest_node is None:
    #         return -1



