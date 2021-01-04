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
    #
    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id not in self.__nodes:
            new_node = Node(node_id, pos)
            self.__nodes[node_id] = new_node
            self.__node_size += 1
            self.__mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        pass

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        pass


graph = DiGraph()
graph.add_node(0)
graph.add_node(1)
graph.add_node(1)
graph.add_node(2)
graph.add_node(3)

graph.add_edge(0, 1, 0.1)
print()
