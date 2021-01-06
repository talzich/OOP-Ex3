import math
import sys
from queue import PriorityQueue
from Node import Node

node0 = Node(0)
node1 = Node(1)
node2 = Node(2)

node0.set_tag(2)
node1.set_tag(1)
node2.set_tag(0)

pair1 = (node1.get_tag(), node1)
pair2 = (node2.get_tag(), node2)
pair3 = (node0.get_tag(), node0)
print(pair3[0])

pq = PriorityQueue()

pq.put(pair1)
pq.put(pair2)
pq.put(pair3)

d = {}
empty = not bool(d)
print(empty)
print(math.inf)
while not pq.empty():
    next = pq.get()
    print(next)
