#!/usr/bin/env python
# -*- coding: utf-8 -*-

from robdd import Robdd
from robdd.synthesis import synthesize as synth
from robdd.operators import Bdd


def remove_interval_up(original, s):
    r = Robdd.false()
    for i, b in enumerate(s):
        if b == '0':
            current_var = Robdd.make_x(i)
            r = synth(r, Bdd.OR, current_var)

    return synth(original, Bdd.AND, r)


def remove_interval_down(original, s):
    r = Robdd.false()
    for i, b in enumerate(s):
        if b == '1':
            current_var = Robdd.make_not_x(i)
            r = synth(r, Bdd.OR, current_var)

    return synth(original, Bdd.AND, r)


def add_negated(s):
    r = Robdd.false()
    for i, b in enumerate(s):
        # if i == 0:
        #     continue
        # if i >= 8:
        #     continue

        if b == '0':
            current_var = Robdd.make_x(i)
        else:
            current_var = Robdd.make_not_x(i)

        r = synth(r, Bdd.OR, current_var)
    return r


def add_restriction(s):
    r = Robdd.true()
    for i, b in enumerate(s):
        # if i == 0:
        #     continue
        # if i >= 8 :
        #     continue

        if b == '1':
            current_var = Robdd.make_x(i)
        else:
            current_var = Robdd.make_not_x(i)

        r = synth(r, Bdd.AND, current_var)
    return r


def blah():
    v = [
        '1000000000000001',
        '1100000000000011',
        '1010000000000101',
        '1000000110000001',
        '1000100000010001',
        '1001000000001001',
        '1000010000100001',
        '1000001001000001',
        '1111000000001111',
        '1010010110100101',
        '1001100110011001',
        '1100110000110101',
        '1010101001010101',
        '1100001111000011',
        '1111111111111111'
    ]
    #
    # '''
    # 1000010000100001
    # 1000000110000001
    # 1010000000000101
    # 1010010110100101
    # '''

    # print v[2]

    solution = None
    for __v__ in v:
        if solution is None:
            solution = add_restriction(__v__)
        else:
            solution = synth(solution, Bdd.OR, add_restriction(__v__))

    # solution = add_restriction(v[0])

    # for i in range(len(v)):
    #     if i in [0, 1, 13]:
    #         continue
    #     solution = synth(solution, Bdd.AND, add_negated(v[i]))

    # solution = remove_interval_down(solution, v[6])
    # solution = remove_interval_down(solution, v[2])
    # solution = remove_interval_down(solution, v[4])
    # solution = remove_interval_down(solution, v[5])
    #
    # solution = remove_interval_up(solution, v[1])



    # solution = Robdd.make_x(0)
    # solution = synth(solution, Bdd.OR, Robdd.make_not_x(0))
    # solution = synth(solution, Bdd.OR, Robdd.make_x(1))


    solution = Robdd.false()
    solution = synth(solution, Bdd.OR, Robdd.make_not_x(0))

    with open('/tmp/graph.dot', 'w') as fh:
        fh.write(solution.graphviz())

    return solution


if __name__ == "__main__":
    from time import time


    start = time()

    result = blah()

    elapsed = time() - start


    print("   solutions       =", result.solutions_len())
    print("   elapsed time    = %.2fs" % elapsed)
    print("   variables       =", len(result.variables))
    print("   nodes (reduced) =", result.insert_distinct)
    print("   nodes (attempts)=", result.insert_attempts)

    # print "\nTrue"
    # true_solution = result.get_solutions(True)
    # if len(true_solution) == 0:
    #     print('sem solução')
    # else:
    #     for x in result.get_solutions(True):
    #         print(x)

    # print "\nFalse"
    # false_solution = result.get_solutions(False)
    # if len(false_solution) == 0:
    #     print('sem solução')
    # else:
    #     for x in result.get_solutions(False):
    #         print(x)