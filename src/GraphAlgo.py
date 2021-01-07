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

    # Loading a json file to the underlying graph this instance is working on
    def load_from_json(self, file_name: str) -> bool:

        if not file_name.endswith(".json"):

            # If file has no extension at all
            if "." not in file_name:
                file_name += ".json"

            # If file has extension different from .json
            else:
                return False

        # We need a clean graph to load into
        if self.graph is not None:
            self.graph.clear_graph()
        else:
            self.graph = DiGraph()

        try:

            json_file = open(file_name, "r")
            json_obj_graph = json.load(json_file)

            # Lists of nodes and edges
            nodes = json_obj_graph["nodes"]
            edges = json_obj_graph["edges"]

            # Load all the nodes to the graph
            for node in nodes:
                new_node = Node(node["key"], tuple(node["pos"]), node["tag"], node["weight"], node["info"])
                self.graph.add_node_object(new_node)

            # Connect the relevant nodes
            for edge in edges:
                new_edge = Edge(edge["src"], edge["dest"], edge["weight"], edge["tag"], edge["info"])
                self.graph.add_edge_object(new_edge)

            return True

        except IOError as e:
            print(e)
            return False

    # Saving this graph into a json file
    def save_to_json(self, file_name: str) -> bool:

        if not file_name.endswith(".json"):

            # If file has no extension at all
            if "." not in file_name:
                file_name += ".json"

            # If file has extension different from .json
            else:
                return False

        graph_json = {}
        nodes_json = []
        edges_json = []
        keys = self.graph.get_v()
        edges = self.graph.get_e()

        try:
            file = open(file_name, "w")

            # Adding nodes to the nodes list
            for key in keys:
                node = self.graph.get_node(key)
                nodes_json.append(node.to_json())

            # Adding the nodes list to the dictionary
            graph_json["nodes"] = nodes_json

            # Adding edges to edges list
            for edge in edges:
                edges_json.append(edge.to_json())

            # Adding all the data to the dictionary
            graph_json["edges"] = edges_json
            graph_json["node size"] = self.graph.v_size()
            graph_json["edge size"] = self.graph.e_size()

            # Dump the dictionary into a json file format
            json.dump(graph_json, file)
            return True

        except IOError as e:
            print(e)
            return False

    # Returns a pair -> (distance from src to dest, the actual path)
    def shortest_path(self, id1: int, id2: int) -> (float, list):

        # Objects of type Node
        src = self.graph.get_node(id1)
        dest = self.graph.get_node(id2)

        if src is None or dest is None:
            return (float("inf"), [])

        # Node to itself
        elif id1 == id2:
            return (0, [id1])

        # Setting up for dijkstra
        self.set_infinity_weight()
        self.set_unvisited()

        # Running dijkstra's algorithm to determine each node's distance from src
        self.dijkstra(src)

        # If there is no path from src to dest
        if dest.get_weight() == float("inf"):
            return (float("inf"), [])

        child = id2
        path = [child]

        # Filling the list with the shortest path from dest to src
        while True:
            father = self.parents[child]
            path.append(father)
            if father == id1:
                break
            child = father

        # Reversing the list
        path.reverse()

        return dest.get_weight(), path

    # This method is a python implementation of dijkstra's algorithm
    def dijkstra(self, src: Node):
        # Will determine which node we will explore next
        pq = PriorityQueue()

        # Node's distance from itself is 0
        src.set_weight(0.0)

        pq.put((src.get_weight(), src))
        src.set_tag(self.visited)

        # While there are still nodes to explore
        while not pq.empty():
            # We will operate with pairs of (weight, node)
            cur_pair = pq.get()

            src = cur_pair[1]
            src.set_tag(self.visited)

            # If current node has no outgoing edges
            if src.get_out() is None or not bool(src.get_out()):
                continue

            # If we find a "cheaper" path, we should replace the relevant variables
            for edge in src.get_out().values():
                dest_node = self.graph.get_node(edge.get_dest())
                path_weight = src.get_weight() + edge.get_weight()

                if dest_node.get_weight() > path_weight:
                    dest_node.set_weight(path_weight)

                    self.parents[dest_node.get_key()] = src.get_key()

                if dest_node.get_tag() == self.unvisited:
                    pq.put((dest_node.get_weight(), dest_node))

    # Utility - Sets all nodes' weights to float("inf")
    def set_infinity_weight(self):
        for key in self.graph.get_v():
            node = self.graph.get_node(key)
            node.set_weight(float("inf"))

    # Utility - Sets all nodes' tags to unvisited
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





