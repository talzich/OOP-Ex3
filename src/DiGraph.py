from GraphInterface import GraphInterface
from Node import Node
from Edge import Edge


class DiGraph(GraphInterface):

    def __init__(self):
        self.__nodes = dict()
        self.__edge_size = 0
        self.__node_size = 0
        self.__mc = 0

    # Returns number of vertices in this graph
    def v_size(self) -> int:
        return self.__node_size

    # Returns number of edges in this graph
    def e_size(self) -> int:
        return self.__edge_size

    # Returns mode counter for edges in this graph
    def get_mc(self) -> int:
        return self.__mc

    # Adds an edge from id1 to id2 with specified weight
    def add_edge(self, id1: int, id2: int, weight: float) -> bool:

        # If the specified nodes are not in this graph
        if id1 not in self.__nodes or id2 not in self.__nodes:
            return False
        # Objects of type Node - declared so we could access their list of ingoing and outgoing edges
        src = self.__nodes[id1]
        dest = self.__nodes[id2]

        # A dictionary representation of all the outgoing connections of src
        src_outs = src.get_out()

        # If they are the same node
        if id1 == id2:
            return False

        # If the nodes are already connected
        elif id2 in src_outs:
            return False

        # The actual connection
        else:
            edge = Edge(id1, id2, weight)
            src.add_out(id2, edge)
            dest.add_in(id1, edge)
            self.__edge_size += 1
            self.__mc += 1
            return True

    # Adds a node with specified key to this graph. If node already exists, does nothing.
    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        # If node is not already in this graph
        if node_id not in self.__nodes:
            new_node = Node(node_id, pos)
            self.__nodes[node_id] = new_node
            self.__node_size += 1
            self.__mc += 1
            return True
        return False

    # Utility - Adds the node passed as parameter to this graph. If node already exists, does nothing.
    def add_node_object(self, node:  Node):
        if node.get_key() not in self.__nodes:
            self.__nodes[node.get_key()] = node
            self.__node_size += 1
            self.__mc += 1
            return True
        return False

    # Utility - Adds the edge passed as parameter to this graph. If edge already exists, does nothing.
    def add_edge_object(self, edge: Edge):

        # If the nodes the specified edge is connected
        if edge.get_src() not in self.__nodes or edge.get_dest() not in self.__nodes:
            return False

        # Objects of type Node - declared so we could access their list of ingoing and outgoing edges
        src = self.__nodes[edge.get_src()]
        dest = self.__nodes[edge.get_dest()]

        # A dictionary representation of all the outgoing connections of src
        src_outs = src.get_out()

        # If they are the same node
        if src.get_key() == dest.get_key():
            return False

        # If they are already connected
        elif dest.get_key() in src_outs:
            return False

        # Making the connection
        else:
            src.add_out(dest.get_key(), edge)
            dest.add_in(src.get_key(), edge)
            self.__edge_size += 1
            self.__mc += 1
            return True

    # Remove specified node from this graph, along with all its outgoing and outgoing edges.
    def remove_node(self, node_id: int) -> bool:

        # If the node specified are not in this graph.
        if node_id not in self.__nodes:
            return False

        # Object of type Node - The node we want to remove
        node = self.__nodes[node_id]

        # Lists containing the keys of all the outgoing and ingoing connections of node
        out_keys = list(node.get_out().keys())
        in_keys = list(node.get_in().keys())

        # Removing all the edges that has anything to do with node
        for key in out_keys:
            self.remove_edge(node_id, key)
        for key in in_keys:
            self.remove_edge(key, node_id)

        # Removing the node
        self.__nodes.pop(node_id)
        self.__mc += 1
        self.__node_size -= 1
        return True

    # Remove the edge that is going out of id1 and in to id2.
    def remove_edge(self, node_id1: int, node_id2: int) -> bool:

        # If the nodes specified are not in this graph.
        if node_id1 not in self.__nodes or node_id2 not in self.__nodes:
            return False

        # Objects of type Node - declared so we could access their list of ingoing and outgoing edges
        src = self.__nodes[node_id1]
        dest = self.__nodes[node_id2]

        # A dictionary representation of all the outgoing connections of src
        src_outs = src.get_out()

        # If the nodes are not connected
        if node_id2 not in src_outs:
            return False

        # The actual disconnection
        src.remove_out(node_id2)
        dest.remove_in(node_id1)
        self.__edge_size -= 1
        self.__mc += 1
        return True

    # Returns a list of all the keys of all the nodes in this graph.
    def get_v(self):
        return list(self.__nodes.keys())

    # Returns a list of all the edges in this graph.
    def get_e(self):

        keys = self.get_v()
        edges = []

        for key in keys:
            node = self.__nodes[key]
            outs = list(node.get_out().values())
            for edge in outs:
                edges.append(edge)

        return edges

    # Returns a node with the specified key
    def get_node(self, key: int):
        if key < 0 or self.__nodes[key] is None:
            return None
        else:
            return self.__nodes[key]

    # Utility - To be used in GraphAlgo.
    # Clears this graph of all nodes and edges.
    def clear_graph(self):
        self.__nodes.clear()
        self.__edge_size = 0
        self.__node_size = 0
        self.__mc = 0

    # A simple to string method
    def __str__(self):
        return f'Node Size: {self.__node_size}, Edge Size: {self.__edge_size} mc: {self.__mc}'

    def get_positions(self):
        my_positions = dict()
        nodes = list(self.__nodes.values())
        for node in nodes:
            my_positions[node.get_key()] = node.get_pos()
        return my_positions
