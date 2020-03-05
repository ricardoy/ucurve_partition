from robdd import Robdd
from robdd.synthesis import synthesize as synth
from robdd.operators import Bdd
from unittest import TestCase


class TestRobdd(TestCase):
    def test_evaluate_should_always_return_false(self):
        robdd = Robdd.false()
        self.assertFalse(robdd.evaluate([0]))
        self.assertFalse(robdd.evaluate([1]))
        self.assertFalse(robdd.evaluate([0, 0]))
        self.assertFalse(robdd.evaluate([0, 1, 1, 0]))

    def test_evaluate_should_always_return_true(self):
        robdd = Robdd.true()
        self.assertTrue(robdd.evaluate([0]))
        self.assertTrue(robdd.evaluate([1]))
        self.assertTrue(robdd.evaluate([0, 0]))
        self.assertTrue(robdd.evaluate([0, 1, 1, 0]))

    def test_evaluate_should_return_true_for_x1(self):
        robdd = Robdd.false()
        v = robdd.make_x(0)
        robdd = synth(robdd, Bdd.OR, v)

        self.assertTrue(robdd.evaluate([1]))
        self.assertTrue(robdd.evaluate([1, 0]))
        self.assertTrue(robdd.evaluate([1, 1, 0, 1]))

        self.assertFalse(robdd.evaluate([0]))
        self.assertFalse(robdd.evaluate([0, 1]))
        self.assertFalse(robdd.evaluate([0, 1, 1, 1]))


