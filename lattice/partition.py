from __future__ import annotations
import random
from typing import Tuple
from collections import defaultdict

from util import convert_to_binary_tuple


class Partition(object):
    def __init__(self, mask:Tuple[int, ...]=None, blocks:Tuple[Tuple[int, ...], ...]=None, cost=None):
        if mask is None and blocks is None:
            raise ValueError('Either mask or blocks must not be None.')
        self._mask = None
        self._blocks = None
        self.mask = mask
        self.blocks = blocks
        self._vc_dimension = None
        self.cost = cost

    def key(self):
        # return str(self.blocks)
        return '({})'.format(','.join(['({})'.format(','.join([str(y) for y in x])) for x in self.blocks]))

    def __str__(self):
        return '({})'.format(' | '.join(['({})'.format(','.join([str(y) for y in x])) for x in self.blocks]))
        # return str(self.blocks)

    def __repr__(self):
        return 'partition:{}'.format(str(self.blocks))

    @property
    def mask(self):
        if self._mask is not None:
            return self._mask

        # print(self._mask)
        # print(self._blocks)

        n = max([max(b) for b in self._blocks])+1

        r = [-1 for _ in range(n)]
        for repr, block in enumerate(self._blocks):
            for i in block:
                r[i] = repr

        self._mask = tuple(r)
        return self._mask

    @mask.setter
    def mask(self, value):
        if value is not None:
            self._mask = normalize_mask(value)

    @property
    def blocks(self):
        if self._blocks is not None:
            return self._blocks

        a = defaultdict(set)
        for i, repr in  enumerate(self._mask):
            a[repr].add(i)

        self._blocks = tuple(tuple(x) for x in a.values())
        return self._blocks

    @blocks.setter
    def blocks(self, value):
        if value is not None:
            self._blocks = normalize_blocks(value)

    def equals(self, other_partition:Partition):
        return self.is_subset(other_partition) and other_partition.is_subset(self)

    def is_superset(self, other_partition:Partition):
        return other_partition.is_subset(self)

    def is_subset(self, other_partition:Partition):
        '''
        π1 ≤ π2 ⇔ x ≡π1 y implies that x ≡π2 y
        :param other_partition: 
        :return: True if this partition is a subset of other_partition
        '''
        assert(self.total_dimension() == other_partition.total_dimension())
        n = self.total_dimension()

        for i in range(n):
            for j in range(i+1, n):
                if self.mask[i] == self.mask[j]:
                    if other_partition.mask[i] != other_partition.mask[j]:
                        return False
        return True

    def total_dimension(self):
        return len(self.mask)

    def vc_dimension(self):
        if self._vc_dimension is None:
            self._vc_dimension = len(set(self.mask))

        return self._vc_dimension

    def has_child(self):
        return self.vc_dimension() < self.total_dimension()

    def random_child(self):
        if self.vc_dimension() == self.total_dimension():
            return None

        feasible_blocks = [(i, b) for (i, b) in enumerate(self.blocks) if len(b) > 1]
        # print('f', feasible_blocks)
        i, block = random.choice(feasible_blocks)

        aux_blocks = []
        for j, b in enumerate(self.blocks):
            if i != j:
                aux_blocks.append(b)

        n = len(block)
        assert (n > 1)
        x = random.randint(1, 2 ** (n - 1) - 1)
        partition_mask = convert_to_binary_tuple(x, n)

        l = []
        r = []

        for i, k in enumerate(partition_mask):
            if k > 0:
                l.append(block[i])
            else:
                r.append(block[i])
        aux_blocks.append(l)
        aux_blocks.append(r)
        return Partition(blocks=tuple(aux_blocks))

    def neighbors(self):
        yield from self.generate_superset()
        yield from self.generate_subset()

    def generate_subset(self):
        if self.vc_dimension() == self.total_dimension():
            return None

        # TODO criar uma estrutura de dados para quebrar blocos de uma partição

        for i, main_block in enumerate(self.blocks):
            if len(main_block) == 1:
                continue
            aux_blocks = []
            for j, b in enumerate(self.blocks):
                if i != j:
                    aux_blocks.append(b)

            for l, r in self._block_partitions(main_block):
                aux_blocks.append(l)
                aux_blocks.append(r)
                yield(Partition(blocks=tuple(aux_blocks)))
                aux_blocks.pop()
                aux_blocks.pop()

    def generate_superset(self):
        if self.vc_dimension() == 1:
            return None

        for i in range(self.vc_dimension()):
            for j in range(i+1, self.vc_dimension()):
                v = list(self.mask)
                for k in range(self.total_dimension()):
                    if v[k] == j:
                        v[k] = i
                yield Partition(mask=tuple(v))


    def _block_partitions(self, block):
        n = len(block)
        assert(n>1)
        for x in range(1, 2**(n-1)):
            partition_mask = convert_to_binary_tuple(x, n)

            l = []
            r = []

            for i, k in enumerate(partition_mask):
                if k > 0:
                    l.append(block[i])
                else:
                    r.append(block[i])
            yield tuple(l), tuple(r)


def normalize_blocks(blocks:Tuple[Tuple[int, ...], ...]):
    return tuple(sorted(([tuple(sorted(x)) for x in blocks])))


def normalize_mask(mask:Tuple[int, ...]):
    c = 0
    d = dict()
    v = []
    for x in mask:
        if x in d:
            v.append(d[x])
        else:
            d[x] = c
            v.append(c)
            c += 1
    return tuple(v)


def generate_random_partition(n:int, parts:int=None):
    """
    :param n: number of dimensions
    :param parts: number of partitions
    :return:
    """
    if parts is None:
        parts = random.randint(1, n)
    else:
        assert (parts >= 1 and parts <= n)

    v = []
    acc = 0
    for _ in range(parts - 1):
        x = random.randint(0, n - parts - acc)
        v.append(x)
        acc += x
    v.append(n - parts - acc)

    a = []
    for v_i in v:
        a.append(1 + v_i)

    r = []
    for i, c in enumerate(a):
        for _ in range(c):
            r.append(i)

    random.shuffle(r)
    return Partition(mask=tuple(r))


class PartitionNode(Partition):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_leaf(self):
        return self.vc_dimension() == 0

    def add_predecessor(self, node:PartitionNode):
        raise Exception('should not be called')

    def add_successor(self, node:PartitionNode):
        raise Exception('should not be called')

    def has_successor(self):
        return self.vc_dimension() > 0

    def random_successor(self):
        return self.random_child()

    @property
    def height(self):
        raise Exception('should not be called')

    @height.setter
    def height(self, value):
        raise Exception('should not be called')


class PartitionLattice(object):
    def __init__(self):
        self._supremum = None
        self._infimum = None
        self.nodes = dict()

    @property
    def supremum(self):
        return self._supremum

    @supremum.setter
    def supremum(self, value):
        if isinstance(value, PartitionNode):
            self._supremum = value
        else:
            raise AttributeError

    @property
    def infimum(self):
        return self._infimum

    @infimum.setter
    def infimum(self, value):
        if isinstance(value, PartitionNode):
            self._infimum = value
        else:
            raise AttributeError

    def add_node(self, node):
        if not isinstance(node, PartitionNode):
            p:Partition = node
            node = PartitionNode()


def bell_number(n):
    bell = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    bell[0][0] = 1
    for i in range(1, n + 1):

        # Explicitly fill for j = 0
        bell[i][0] = bell[i - 1][i - 1]

        # Fill for remaining values of j
        for j in range(1, i + 1):
            bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1]

    return bell[n][0]
