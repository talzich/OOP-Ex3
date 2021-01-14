from typing import List
from DiGraph import DiGraph
from Node import Node
from Edge import Edge
from GraphAlgoInterface import GraphAlgoInterface
from queue import PriorityQueue
import json
import random
import matplotlib.pyplot as plt
import time
import timeit


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph=None):
        self.__graph = graph
        self.__parents = {}
        self.__unvisited = 1
        self.__visited = 0
        self.__SCC = []
        self.__boundaries = []

        if graph is not None:
            self.__mc_scc = self.__graph.get_mc()
            self.__mc_sp = self.__graph.get_mc()

    def get_graph(self):
        return self.__graph

    # Loading a json file to the underlying graph this instance is working on
    def load_from_json(self, file_name: str) -> bool:

        # We need a clean graph to load into
        if self.__graph is not None:
            self.__graph.clear_graph()
        else:
            self.__graph = DiGraph()

        try:

            json_file = open(file_name, "r")
            json_obj_graph = json.load(json_file)

            # Lists of nodes and edges
            nodes = json_obj_graph["Nodes"]
            edges = json_obj_graph["Edges"]

            # Load all the nodes to the graph
            for node in nodes:
                if 'pos' in node:
                    str_pos = node['pos']
                    pos = str_pos.split(',')
                    x = float(pos[0])
                    y = float(pos[1])
                    new_node = Node(key=node["id"], pos=(x, y))
                else:
                    new_node = Node(key=node['id'])
                self.__graph.add_node_object(new_node)

            # Connect the relevant nodes
            for edge in edges:
                new_edge = Edge(src=edge["src"], dest=edge["dest"], weight=edge["w"])
                self.__graph.add_edge_object(new_edge)

            self.__mc_scc = self.__graph.get_mc()
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
        keys = self.__graph.get_v()
        edges = self.__graph.get_e()

        try:
            file = open(file_name, "w")

            # Adding nodes to the nodes list
            for key in keys:
                node = self.__graph.get_node(key)
                nodes_json.append(node.to_json())

            # Adding the nodes list to the dictionary
            graph_json["Nodes"] = nodes_json

            # Adding edges to edges list
            for edge in edges:
                edges_json.append(edge.to_json())

            # Adding all the data to the dictionary
            graph_json["Edges"] = edges_json

            # Dump the dictionary into a json file format
            json.dump(graph_json, file)
            return True

        except IOError as e:
            print(e)
            return False

    # Returns a pair -> (distance from src to dest, the actual path)
    def shortest_path(self, id1: int, id2: int) -> (float, list):

        # Objects of type Node
        src = self.__graph.get_node(id1)
        dest = self.__graph.get_node(id2)

        if src is None or dest is None:
            return (float("inf"), [])

        # Node to itself
        elif id1 == id2:
            return (0, [id1])

        # If algorithm already ran for this pair and nothing in the graph had changes since, we can return
        # the correct answer from node's attribute
        if src.get_path(id2) and self.__mc_sp == self.__graph.get_mc():
            return src.get_path(id2)

        self.__mc_sp == self.__graph.get_mc()

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
            father = self.__parents[child]
            path.append(father)
            if father == id1:
                break
            child = father

        # Reversing the list
        path.reverse()

        src.set_path(id2, (dest.get_weight, path))
        return dest.get_weight(), path

    # This method is a python implementation of dijkstra's algorithm
    def dijkstra(self, src: Node):
        # Will determine which node we will explore next
        pq = PriorityQueue()

        # Node's distance from itself is 0
        src.set_weight(0.0)

        pq.put((src.get_weight(), src))
        src.set_tag(self.__visited)

        # While there are still nodes to explore
        while not pq.empty():
            # We will operate with pairs of (weight, node)
            cur_pair = pq.get()

            src = cur_pair[1]
            src.set_tag(self.__visited)

            # If current node has no outgoing edges
            if src.get_out() is None or not bool(src.get_out()):
                continue

            # If we find a "cheaper" path, we should replace the relevant variables
            for edge in src.get_out().values():
                dest_node = self.__graph.get_node(edge.get_dest())
                path_weight = src.get_weight() + edge.get_weight()

                if dest_node.get_weight() > path_weight:
                    dest_node.set_weight(path_weight)

                    self.__parents[dest_node.get_key()] = src.get_key()

                if dest_node.get_tag() == self.__unvisited:
                    pq.put((dest_node.get_weight(), dest_node))

    # Utility - Sets all nodes' weights to float("inf")
    def set_infinity_weight(self):
        for key in self.__graph.get_v():
            node = self.__graph.get_node(key)
            node.set_weight(float("inf"))

    # Utility - Sets all nodes' tags to unvisited
    def set_unvisited(self):
        for key in self.__graph.get_v():
            node = self.__graph.get_node(key)
            node.set_tag(self.__unvisited)

    def connected_component(self, id1: int) -> list:
        if not self.__SCC:
            self.connected_components()

        src = self.__graph.get_node(id1)
        if self.__graph is None or src is None:
            return []
        for i in self.__SCC:
            if id1 in i:
                return i

    def connected_components(self) -> List[list]:
        self.kosaraju()
        return self.__SCC

    def plot_graph(self) -> None:
        self.plot_nodes()
        self.plot_edges()
        plt.show()
        return None

    # ********** Utility Methods ********** #

    def reverse_graph(self):
        reversed_graph = DiGraph()
        for key in self.__graph.get_v():
            node = self.__graph.get_node(key)
            new_node = Node()
            new_node.copy(node)
            new_node.set_tag(self.__unvisited)
            reversed_graph.add_node_object(new_node)

        for edge in self.__graph.get_e():
            reversed_graph.add_edge(edge.get_dest(), edge.get_src(), edge.get_weight())

        return reversed_graph

    def fill_util(self, edges: list, dfs_stack, k_stack):
        for edge in edges:
            curr_child = self.__graph.get_node(edge.get_dest())
            if curr_child.get_tag() is self.__unvisited:
                curr_child.set_tag(self.__visited)
                dfs_stack.append(curr_child.get_key())
                return
        k_stack.append(dfs_stack.pop())

    def dfs_fill(self, k_stack: list, dfs_stack: list, node: Node):

        dfs_stack.append(node.get_key())

        while dfs_stack:
            last = len(dfs_stack) - 1
            node = self.__graph.get_node(dfs_stack[last])

            if (not node.get_out()) or node.get_out() is None:
                k_stack.append(dfs_stack.pop())
                continue

            edges = list(node.get_out().values())
            self.fill_util(edges, dfs_stack, k_stack)

    def empty_util(self, edges: list, comp: list, dfs_stack: list, graph_t: DiGraph):

        for edge in edges:
            curr_child = graph_t.get_node(edge.get_dest())
            if curr_child.get_tag() is self.__unvisited:
                curr_child.set_tag(self.__visited)
                dfs_stack.append(curr_child.get_key())
                comp.append(curr_child.get_key())
                return
        dfs_stack.pop()

    def dfs_empty(self, dfs_stack: list, graph_t: DiGraph, curr_key: int):
        node = graph_t.get_node(curr_key)

        if node.get_tag() is self.__unvisited:
            node.set_tag(self.__visited)

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

        if self.__graph is None:
            return []

        if self.__SCC and self.__mc_scc == self.__graph.get_mc():
            return

        self.__mc_scc = self.__graph.get_mc()
        # This stack will keep track of which nodes finished exploring
        k_stack = list()

        # This stack will manage the way we explore our graph and will maintain a DFS approach
        dfs_stack = list()

        self.set_unvisited()

        for key in self.__graph.get_v():
            node = self.__graph.get_node(key)
            if node.get_tag() == self.__unvisited:
                node.set_tag(self.__visited)
                self.dfs_fill(k_stack, dfs_stack, node)

        reversed_graph = self.reverse_graph()

        while k_stack:
            comp = self.dfs_empty(dfs_stack, reversed_graph, k_stack.pop())
            if comp is not None:
                self.__SCC.append(comp)

    def plot_nodes(self):

        # Constant values
        node_color = "#BDA3FA"  # Kinda purple

        # data would be a dictionary in which key is a node's key and value is a node's position
        data = self.__graph.get_positions()

        # If there is a node with no position
        if None in data.values():
            self.set_randoms(data)

        x_val = []
        y_val = []

        for point in data.values():
            x_val.append(point[0])
            y_val.append(point[1])

        fig, ax = plt.subplots()
        ax.scatter(x_val, y_val)

        arrow = {}

        for item in data:
            ax.annotate(item, data[item])

        self.set_boundaries(data)
        plt.scatter(x_val, y_val, color=node_color, s=75)

    def plot_edges(self):

        edges = self.__graph.get_e()
        for edge in edges:
            dest = self.__graph.get_node(edge.get_dest())
            src = self.__graph.get_node(edge.get_src())
            dest_pos = dest.get_pos()
            src_pos = src.get_pos()
            plt.annotate(text=" ", xy=dest_pos, xytext=src_pos,
                         arrowprops=dict(facecolor='k', width=0.5, headwidth=3))

    def set_randoms(self, data: dict):

        x_comp = list()
        y_comp = list()
        points = list(data.values())

        for point in points:
            if point is not None:
                x_comp.append(point[0])
                y_comp.append(point[1])

        if len(x_comp) < 2:
            for item in data:

                if data[item] is None:
                    rand_x = random.randrange(-10, 10)
                    rand_y = random.randrange(-10, 10)
                    rand_point = (rand_x, rand_y)

                    if rand_point in data.values():
                        rand_point = (rand_x * 1.1, rand_y * 1.1)

                    data[item] = rand_point
                    self.__graph.get_node(item).set_pos(rand_point)

        else:
            min_x = min(x_comp)
            min_y = min(y_comp)

            max_x = max(x_comp)
            max_y = max(y_comp)

            for item in data:

                if data[item] is None:
                    rand_x = random.randrange(min_x, max_x)
                    rand_y = random.randrange(min_y, max_y)
                    rand_point = (rand_x, rand_y)

                    if rand_point in data.values():
                        rand_point = (rand_x * 1.1, rand_y * 1.1)

                    data[item] = rand_point
                    self.__graph.get_node(item).set_pos(rand_point)

            max_point = (max_x, max_y)
            min_point = (min_x, min_y)

            self.__boundaries[0] = min_point
            self.__boundaries[1] = max_point

    def set_boundaries(self, data):

        x_comp = list()
        y_comp = list()
        points = list(data.values())

        for point in points:
            x_comp.append(point[0])
            y_comp.append(point[1])

        min_x = min(x_comp)
        min_y = min(y_comp)

        max_x = max(x_comp)
        max_y = max(y_comp)

        min_point = (min_x, min_y)
        max_point = (max_x, max_y)

        self.__boundaries = [min_point, max_point]
    # ********** Utility Methods ********** #
