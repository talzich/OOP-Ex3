from GraphInterface import GraphInterface
from Node import Node
from Edge import Edge


class DiGraph(GraphInterface):

    def __init__(self):
        self.nodes = dict()
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
        if id1 not in self.nodes or id2 not in self.nodes:
            return False

        src = self.nodes[id1]
        dest = self.nodes[id2]
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
        if node_id not in self.nodes:
            new_node = Node(node_id, pos)
            self.nodes[node_id] = new_node
            self.__node_size += 1
            self.__mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        pass

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self.nodes or node_id2 not in self.nodes:
            return False
        src = self.nodes[node_id1]
        dest = self.nodes[node_id2]

        src_outs = src.get_out()
        dest_ins = dest.get_in()

        if node_id2 not in src_outs:
            return False

        src.remove_out(node_id2)
        dest.remove_in(node_id1)
        self.__edge_size -= 1
        self.__mc += 1
        return True

    def __str__(self):
        return f'Node Size: {self.__node_size}, Edge Size: {self.__edge_size} mc: {self.__mc}'


graph = DiGraph()
graph.add_node(0)
graph.add_node(1)
print(graph.__str__())
print(graph.add_edge(0, 1, 5))
print(graph.__str__())
print(graph.add_edge(1, 0, 3))
print(graph.__str__())
graph.remove_edge(0, 1)
graph.remove_edge(1, 0)
print(graph.__str__())
graph.remove_edge(1, 0)
print(graph.__str__())
