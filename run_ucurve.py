import argparse
from ucurve.partition_to_boolean import partittion_to_boolean_generator
from ucurve.path_start import get_initial_robdd, add_restriction, remove_interval_sup, remove_interval_inf
from robdd.synthesis import synthesize as synth
from robdd.operators import Bdd

from typing import Dict, List


def get_initialized_robdd(partition_to_boolean:Dict[List[int], List[int]]):
    robdd = get_initial_robdd()
    for p, b in partition_to_boolean.items():
        # print(b)
        robdd = synth(robdd, Bdd.OR, add_restriction(b))

    return robdd


def main(number_of_items):
    partition_to_boolean = dict()
    for p, b in partittion_to_boolean_generator(number_of_items):
        partition_to_boolean[p] = b

    print('Partitions generated.')

    robdd = get_initialized_robdd(partition_to_boolean)

    # with open('/tmp/b.dot', 'w') as fh:
    #     fh.write(robdd.graphviz())


    robdd = remove_interval_inf(robdd, [1, 0, 0, 0])
    robdd = remove_interval_inf(robdd, [1, 1, 0, 0])
    robdd = remove_interval_inf(robdd, [1, 0, 0, 1])



    # for b in partition_to_boolean.values():
    #     print(b)
    #     robdd = remove_interval_inf(robdd, b)
    #     print('random solution', robdd.get_random_solution(1))
    #     print('random solution', robdd.get_random_solution(1))

    # with open('/tmp/a.dot', 'w') as fh:
    #     fh.write(robdd.graphviz())


    print('random solution:', robdd.get_random_solution(1))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int)

    args = parser.parse_args()
    main(args.n)

