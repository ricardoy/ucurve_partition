from lattice.partition import Partition
from lattice.lattice import Lattice, LatticeIterator


class LatticeInterval:
    def __init__(self, low, high):
        self.low:Partition = low
        self.high:Partition = high

    def contains(self, partition:Partition):
        return self.high.is_superset(partition) and self.low.is_subset(partition)