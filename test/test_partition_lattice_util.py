from robdd import Robdd
from robdd.synthesis import synthesize as synth
from ucurve.robdd_util import add_restriction
from ucurve.partition_lattice_util import get_minimal_element
from robdd.operators import Bdd
from lattice import Partition
from unittest import TestCase


class TestRobddUtil(TestCase):
    def test_get_minimal_element_should_work(self):
        robdd = Robdd.false()

        a = (1, 1, 1, 1)
        pa = Partition(mask=(0, 0, 0))

        b = (1, 1, 0, 0)
        pb = Partition(mask=(0, 0, 1))

        c = (1, 0, 1, 0)
        pc = Partition(mask=(0, 1, 0))

        d = (1, 0, 0, 1)
        pd = Partition(mask=(0, 1, 1))

        e = (1, 0, 0, 0)
        pe = Partition(mask=(0, 1, 2))

        robdd = synth(robdd, Bdd.OR, add_restriction(a))
        robdd = synth(robdd, Bdd.OR, add_restriction(b))
        robdd = synth(robdd, Bdd.OR, add_restriction(c))
        robdd = synth(robdd, Bdd.OR, add_restriction(d))
        robdd = synth(robdd, Bdd.OR, add_restriction(e))

        mapping_partition_to_boolean = dict()
        mapping_partition_to_boolean[pa.mask] = a
        mapping_partition_to_boolean[pb.mask] = b
        mapping_partition_to_boolean[pc.mask] = c
        mapping_partition_to_boolean[pd.mask] = d
        mapping_partition_to_boolean[pe.mask] = e

        mapping_boolean_to_partition = dict()
        mapping_boolean_to_partition[a] = pa
        mapping_boolean_to_partition[b] = pb
        mapping_boolean_to_partition[c] = pc
        mapping_boolean_to_partition[d] = pd
        mapping_boolean_to_partition[e] = pe

        self.assertEqual((0, 1, 2), get_minimal_element(robdd, mapping_partition_to_boolean, mapping_boolean_to_partition))

    def test_get_minimal_element_should_work2(self):
        robdd = Robdd.false()

        a = (1, 1, 1, 1)
        pa = Partition(mask=(0, 0, 0))

        b = (1, 1, 0, 0)
        pb = Partition(mask=(0, 0, 1))

        c = (1, 0, 1, 0)
        pc = Partition(mask=(0, 1, 0))

        d = (1, 0, 0, 1)
        pd = Partition(mask=(0, 1, 1))

        e = (1, 0, 0, 0)
        pe = Partition(mask=(0, 1, 2))

        robdd = synth(robdd, Bdd.OR, add_restriction(a))
        robdd = synth(robdd, Bdd.OR, add_restriction(b))
        robdd = synth(robdd, Bdd.OR, add_restriction(c))
        robdd = synth(robdd, Bdd.OR, add_restriction(d))

        mapping_partition_to_boolean = dict()
        mapping_partition_to_boolean[pa.mask] = a
        mapping_partition_to_boolean[pb.mask] = b
        mapping_partition_to_boolean[pc.mask] = c
        mapping_partition_to_boolean[pd.mask] = d
        mapping_partition_to_boolean[pe.mask] = e

        mapping_boolean_to_partition = dict()
        mapping_boolean_to_partition[a] = pa
        mapping_boolean_to_partition[b] = pb
        mapping_boolean_to_partition[c] = pc
        mapping_boolean_to_partition[d] = pd
        mapping_boolean_to_partition[e] = pe

        minimal_element = get_minimal_element(robdd, mapping_partition_to_boolean, mapping_boolean_to_partition)

        self.assertTrue(minimal_element == (0, 0, 1) or minimal_element == (0, 1, 0) or minimal_element == (0, 1, 1))

    def test_get_minimal_element_should_return_none_if_empty(self):
        robdd = Robdd.false()

        self.assertIsNone(get_minimal_element(robdd, dict(), dict()))