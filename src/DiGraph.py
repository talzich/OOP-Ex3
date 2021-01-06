from GraphInterface import GraphInterface
from Node import Node
from Edge import Edge


class DiGraph(GraphInterface):

    def __init__(self):
        self.__nodes = dict()
        self.__edge_size = 0
        self.__node_size = 0
        self.__mc = 0

    def v_size(self) -> int:
        return self.__node_size

    def e_size(self) -> int:
        return self.__edge_size

    def get_mc(self) -> int:
        return self.__mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.__nodes or id2 not in self.__nodes:
            return False

        src = self.__nodes[id1]
        dest = self.__nodes[id2]
        src_outs = src.get_out()

        if id1 == id2:
            return False

        elif id2 in src_outs:
            return False

        else:
            edge = Edge(id1, id2, weight)
            src.add_out(id2, edge)
            dest.add_in(id1, edge)
            self.__edge_size += 1
            self.__mc += 1
            return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id not in self.__nodes:
            new_node = Node(node_id, pos)
            self.__nodes[node_id] = new_node
            self.__node_size += 1
            self.__mc += 1
            return True
        return False

    def add_node_object(self, node:  Node):
        if node.get_key() not in self.__nodes:
            self.__nodes[node.get_key()] = node
            self.__node_size += 1
            self.__mc += 1
            return True
        return False

    def add_edge_object(self, edge: Edge):
        if edge.get_src() not in self.__nodes or edge.get_dest() not in self.__nodes:
            return False

        src = self.__nodes[edge.get_src()]
        dest = self.__nodes[edge.get_dest()]
        src_outs = src.get_out()

        if src.get_key() == dest.get_key():
            return False

        elif dest.get_key() in src_outs:
            return False

        else:
            src.add_out(dest.get_key(), edge)
            dest.add_in(src.get_key(), edge)
            self.__edge_size += 1
            self.__mc += 1
            return True

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self.__nodes:
            return False

        node = self.__nodes[node_id]
        out_keys = list(node.get_out().keys())
        in_keys = list(node.get_in().keys())

        for key in out_keys:
            self.remove_edge(node_id, key)
        for key in in_keys:
            self.remove_edge(key, node_id)

        self.__nodes.pop(node_id)
        self.__mc += 1
        self.__node_size -= 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self.__nodes or node_id2 not in self.__nodes:
            return False
        src = self.__nodes[node_id1]
        dest = self.__nodes[node_id2]

        src_outs = src.get_out()

        if node_id2 not in src_outs:
            return False

        src.remove_out(node_id2)
        dest.remove_in(node_id1)
        self.__edge_size -= 1
        self.__mc += 1
        return True

    def get_v(self):
        return list(self.__nodes.keys())

    def get_e(self):

        keys = self.get_v()
        edges = []

        for key in keys:
            node = self.__nodes[key]
            outs = list(node.get_out().values())
            for edge in outs:
                edges.append(edge)

        return edges

    def get_node(self, key: int):
        if key < 0 or self.__nodes[key] is None:
            return None
        else:
            return self.__nodes[key]

    def clear_graph(self):
        self.__nodes.clear()
        self.__edge_size = 0
        self.__node_size = 0
        self.__mc = 0

    def __str__(self):
        return f'Node Size: {self.__node_size}, Edge Size: {self.__edge_size} mc: {self.__mc}'
