import unittest

from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
import random


def graph_build_test_d():
    g = DiGraph()
    for i in range(5):
        g.add_node(i)
    g.add_edge(0, 1, 5)
    g.add_edge(1, 0, 8)
    g.add_edge(0, 2, 2)
    g.add_edge(2, 0, 1)
    g.add_edge(2, 3, 1)
    g.add_edge(3, 2, 0.5)
    g.add_edge(3, 4, 12)
    g.add_edge(4, 3, 1)
    g.add_edge(0, 4, 20)
    g.add_edge(4, 0, 20)
    g.add_edge(4, 1, 5)
    g.add_edge(1, 4, 5)
    return g


def connected_graph(num):
    g = DiGraph();
    for i in range(num):
        g.add_node(i)

    for i in range(2, num):
        w = random.randrange(0, 100)
        g.add_edge(0, i, w)
        g.add_edge(i, 0, w)
        g.add_edge(1, i, w)
    g.add_edge(1, 0, 1)
    g.add_edge(0, 1, 1)
    g.add_edge(0, 1, 1)
    return g


class MyTestCase(unittest.TestCase):

    def test_a(self):
        g = DiGraph()
        a = GraphAlgo()
        a.__init__(g)
        self.assertTrue(g == a.get_graph())

    def test_b(self):
        g = DiGraph()
        a = GraphAlgo(g)
        self.assertEqual(0, len(a.connected_components()))

    def test_b1(self):
        g = DiGraph()
        a = GraphAlgo(g)
        g.add_node(0)
        self.assertEqual(1, len(a.connected_components()))

    def test_c1(self):
        g = DiGraph()
        a = GraphAlgo(g)
        g.add_node(0)
        g.add_node(1)
        self.assertEqual(2, len(a.connected_components()))

    def test_c2(self):
        g = DiGraph()
        a = GraphAlgo(g)
        g.add_node(0)
        g.add_node(1)
        g.add_edge(0, 1, 10.3)
        g.add_edge(1, 0, 3.15)
        self.assertEqual(1, len(a.connected_components()))

    def test_d1(self):
        g = graph_build_test_d()
        a = GraphAlgo(g)
        self.assertEqual(10, a.shortest_path(0, 4)[0])

    def test_d2(self):
        g = graph_build_test_d()
        a = GraphAlgo(g)
        self.assertEqual(3, len(a.shortest_path(0, 4)[1]))

    def test_d3(self):
        g = graph_build_test_d()
        a = GraphAlgo(g)
        self.assertEqual(2.5, a.shortest_path(4, 0)[0])

    def test_d4(self):
        g = graph_build_test_d()
        a = GraphAlgo(g)
        l = a.shortest_path(4, 0)[1]
        self.assertEqual(4, len(l))

    def test_d5(self):
        g = graph_build_test_d()
        a = GraphAlgo(g)
        g.remove_node(2)
        l = a.shortest_path(4, 0)[1]
        self.assertEqual(3, len(l))

    def test_e1(self):
        g = connected_graph(100)
        a = GraphAlgo(g)
        self.assertEqual(1, len(a.connected_components()))

    def test_e2(self):
        g = connected_graph(1000)
        a = GraphAlgo(g)
        self.assertEqual(1, len(a.connected_components()))

    def test_f1(self):
        g = graph_build_test_d()
        a = GraphAlgo(g)
        self.assertTrue(a.save_to_json("testf1.json"))

    def test_f2(self):
        self.test_f1()
        a = GraphAlgo()
        self.assertTrue(a.load_from_json("testf1.json"))

if __name__ == '__main__':
    unittest.main()
