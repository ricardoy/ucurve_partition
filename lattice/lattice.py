from __future__ import annotations
import random
from collections import defaultdict
from collections import deque
from lattice import Partition


# talvez dê para extender simpleNode utilizando um partition internamente

class SimpleNode(object):
    c = 0

    def __init__(self, key, value):
        self.cost = float('inf')
        self.key = key
        self.value = value
        self.predecessors = set()
        self.successors = set()
        self.id = self._generate_id()
        self._height = None

    def _generate_id(self):
        SimpleNode.c += 1
        return 'latticeobject{}'.format(SimpleNode.c)

    def is_leaf(self):
        return len(self.successors) == 0

    def add_predecessor(self, n:SimpleNode):
        self.predecessors.add(n)

    def add_successor(self, n:SimpleNode):
        self.successors.add(n)

    def has_successor(self):
        return len(self.successors) > 0

    def random_successor(self):
        return random.choice(list(self.successors))

    @property
    def height(self):
        if self._height is not None:
            return self._height
        max_children_height = -1
        for c in self.successors:
            h = c.height
            if h > max_children_height:
                max_children_height = h
        self._height = max_children_height + 1
        return self._height

    @height.setter
    def height(self, value):
        if not isinstance(value, int):
            raise AttributeError()
        if self._height is None:
            self._height = value
        if value > self._height:
            self._height = value


class LatticeIterator(object):
    def __init__(self, lattice):
        self.queue = deque()
        self.lattice = lattice

        if lattice.supremum is not None:
            self.queue.append(lattice.supremum)

    def __next__(self):
        if len(self.queue) > 0:
            e = self.queue.popleft()
            for successor in e.successors:
                self.queue.append(successor)
            return e
        raise StopIteration


class Lattice(object):
    def __init__(self):
        self._supremum = None
        self._infimum = None
        self.nodes = dict()

    @property
    def supremum(self):
        return self._supremum

    @supremum.setter
    def supremum(self, value):
        if isinstance(value, SimpleNode):
            self._supremum = value
        else:
            raise AttributeError()

    @property
    def infimum(self):
        return self._infimum

    @infimum.setter
    def infimum(self, value):
        if isinstance(value, SimpleNode):
            self._infimum = value
        else:
            raise AttributeError()

    def height(self):
        if self._supremum is None:
            return -1
        return self.supremum.height

    def width(self):
        count = defaultdict(int)
        for n in self.nodes.values():
            count[n.height] += 1
        return max(count.values())

    def get_nodes(self):
        return self.nodes.values()

    def exists_path(self, a:SimpleNode, b:SimpleNode):
        return b.value.is_subset(a.value)

    def contained(self, a:SimpleNode, b:SimpleNode):
        return self.exists_path(a, b)

    def is_upper_adjacent(self, t, a):
        return t.value.vc_dimension() == a.value.vc_dimension() + 1 and \
            a.value.is_subset(t.value)

    def get_all_neighbors(self, n:SimpleNode):
        return n.successors.union(n.predecessors)

    def find_node_by_key(self, key):
        return self.nodes[key]

    def complement(self, n: SimpleNode):
        nodes = set(self.nodes.values())
        nodes.remove(n)
        return nodes

    def add_edge(self, origin:SimpleNode, destination:SimpleNode):
        origin.add_successor(destination)
        destination.add_predecessor(origin)

    def __iter__(self):
        return LatticeIterator(self)
