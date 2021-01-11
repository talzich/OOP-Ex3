from typing import List
from DiGraph import DiGraph
from Node import Node
from Edge import Edge
from GraphAlgoInterface import GraphAlgoInterface
from queue import PriorityQueue
import json
import matplotlib.pyplot as plt
import numpy as np
import random




class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph):
        self.graph = graph
        self.parents = {}
        self.unvisited = 1
        self.visited = 0

        # A list of lists. Looks like:
        # [
        #    [node0, node2]
        #    [node1, node3]
        #    [node4, node5]
        #  ]

        self.SCC = []

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
        src = self.graph.get_node(id1)
        if self.graph is None or src is None:
            return []
        for i in self.SCC:
            if id1 in i:
                return i

    def connected_components(self) -> List[list]:
        self.kosaraju()
        return self.SCC

    def plot_graph(self) -> None:
        self.plot_nodes()
        self.plot_edges()
        plt.show()
        return None

    # ********** Utility Methods ********** #
    def reverse_graph(self):
        reversed_graph = DiGraph()
        for key in self.graph.get_v():
            node = self.graph.get_node(key)
            new_node = Node()
            new_node.copy(node)
            new_node.set_tag(self.unvisited)
            reversed_graph.add_node_object(new_node)

        for edge in self.graph.get_e():
            reversed_graph.add_edge(edge.get_dest(), edge.get_src(), edge.get_weight())

        return reversed_graph

    def fill_util(self, edges: list, dfs_stack, k_stack):
        for edge in edges:
            curr_child = self.graph.get_node(edge.get_dest())
            if curr_child.get_tag() is self.unvisited:
                curr_child.set_tag(self.visited)
                dfs_stack.append(curr_child.get_key())
                return
        k_stack.append(dfs_stack.pop())

    def dfs_fill(self, k_stack: list, dfs_stack: list, node: Node):

        dfs_stack.append(node.get_key())

        while dfs_stack:
            last = len(dfs_stack) - 1
            node = self.graph.get_node(dfs_stack[last])

            if (not node.get_out()) or node.get_out() is None:
                k_stack.append(dfs_stack.pop())
                continue

            edges = list(node.get_out().values())
            self.fill_util(edges, dfs_stack, k_stack)

    def empty_util(self, edges: list, comp: list, dfs_stack: list, graph_t: DiGraph):

        for edge in edges:
            curr_child = graph_t.get_node(edge.get_dest())
            if curr_child.get_tag() is self.unvisited:
                curr_child.set_tag(self.visited)
                dfs_stack.append(curr_child.get_key())
                comp.append(curr_child.get_key())
                return
        dfs_stack.pop()

    def dfs_empty(self, dfs_stack: list, graph_t: DiGraph, curr_key: int):
        node = graph_t.get_node(curr_key)

        if node.get_tag() is self.unvisited:
            node.set_tag(self.visited)

            comp = list()
            comp.append(node.get_key())

            dfs_stack.append(node.get_key())

            while dfs_stack:
                last = len(dfs_stack) - 1
                node = graph_t.get_node(dfs_stack[last])

                if (not node.get_out()) or node.get_out() is None:
                    dfs_stack.pop()
                    continue

                edges = list(node.get_out().values())
                self.empty_util(edges, comp, dfs_stack, graph_t)
            return comp
        return None

    def kosaraju(self):

        if self.graph is None:
            return []

        # This stack will keep track of which nodes finished exploring
        k_stack = list()

        # This stack will manage the way we explore our graph and will maintain a DFS approach
        dfs_stack = list()

        self.set_unvisited()

        for key in self.graph.get_v():
            node = self.graph.get_node(key)
            if node.get_tag() == self.unvisited:
                node.set_tag(self.visited)
                self.dfs_fill(k_stack, dfs_stack, node)

                reversed_graph = self.reverse_graph()

                while k_stack:
                    comp = self.dfs_empty(dfs_stack, reversed_graph, k_stack.pop())
                    if comp is not None:
                        self.SCC.append(comp)

    def plot_nodes(self):

        # Constant values
        node_color = "#BDA3FA"  # Kinda purple
        rand_node_color = "#F5B1AE"  # Kinda orange
        node_shape = "o"
        node_area = 100.0

        # data would be a dictionary in which key is a node's key and value is a node's position
        data = self.graph.get_positions()
        points = list(data.values())
        keys = list(data.keys())
        rand_indices = list()
        rand_points = list()

        x_vals = list()
        y_vals = list()

        for i, point in enumerate(points):
            # If a node has no position, add its key to the rand_indices list for later
            if point is not None:
                x_vals.append(point[0])
                y_vals.append(point[1])
            else:
                rand_indices.append(i)

        self.random_positions(x_vals, y_vals, rand_indices, rand_points)

        # Adding annotations with each node's key
        fig, ax = plt.subplots()
        ax.scatter(x_vals, y_vals)

        for i, txt in enumerate(keys):
            key_x_pos = x_vals[i] - 0.04
            key_y_pos = y_vals[i] - 0.055
            ax.annotate(keys[i], (key_x_pos, key_y_pos))

        # Scattering the shapes for non-random points
        plt.scatter(x_vals, y_vals, node_area, node_color, node_shape)
        plt.scatter(rand_points, node_area, rand_node_color, node_shape)

    def plot_edges(self):
        pass

    def random_positions(self, x_vals, y_vals, keys, rand_points):

        x_compare = list()
        y_compare = list()

        for x in x_vals:
            if x is not None:
                x_compare.append(x)

        for y in y_vals:
            if y is not None:
                y_compare.append(y)

        min_x = min(x_compare)
        min_y = min(y_compare)

        max_x = max(x_compare)
        max_y = max(y_compare)

        for key in keys:

            rand_x = random.randrange(min_x, max_x)
            rand_y = random.randrange(min_y, max_y)

            while rand_x in x_vals:
                rand_x = random.randrange(min_x, max_x)

            while rand_y in y_vals:
                rand_y = random.randrange(min_y, max_y)

            rand_points.append((rand_x, rand_y))

    # ********** Utility Methods ********** #
