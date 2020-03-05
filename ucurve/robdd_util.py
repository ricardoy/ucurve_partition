#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

from robdd import Robdd
from robdd.synthesis import synthesize as synth
from robdd.operators import Bdd


def get_initial_robdd():
    return Robdd.false()


def remove_interval_inf(original:Robdd, s:List[int]):
    r = Robdd.false()
    for i, b in enumerate(s):
        if b == 0:
            current_var = Robdd.make_x(i)
            r = synth(r, Bdd.OR, current_var)

    return synth(original, Bdd.AND, r)


def remove_interval_sup(original:Robdd, s:List[int]):
    r = Robdd.false()
    for i, b in enumerate(s):
        if b == 1:
            current_var = Robdd.make_not_x(i)
            r = synth(r, Bdd.OR, current_var)

    return synth(original, Bdd.AND, r)


def add_negated(s:List[int]):
    r = Robdd.false()
    for i, b in enumerate(s):
        if b == 0:
            current_var = Robdd.make_x(i)
        else:
            current_var = Robdd.make_not_x(i)

        r = synth(r, Bdd.OR, current_var)
    return r


def add_restriction(s:List[int]):
    r = Robdd.true()
    for i, b in enumerate(s):
        if b == 1:
            current_var = Robdd.make_x(i)
        else:
            current_var = Robdd.make_not_x(i)

        r = synth(r, Bdd.AND, current_var)
    return r


def main():
    v = [
        [1, 1, 1],
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]

    solution = Robdd.false()
    output(solution)


    solution = synth(solution, Bdd.OR, add_restriction(v[0]))
    output(solution)

    solution = synth(solution, Bdd.OR, add_restriction(v[1]))
    output(solution)

    solution = synth(solution, Bdd.OR, add_restriction(v[2]))
    output(solution)

    solution = synth(solution, Bdd.OR, add_restriction(v[3]))
    output(solution)

    # remove intervalos

    solution = remove_interval_sup(solution, v[2])
    print('((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((')
    print(solution.get_root())
    print(solution.items)
    output(solution)
    print('))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))')

    solution = remove_interval_inf(solution, v[2])
    output(solution)

    return solution



def output(solution):
    global contador_imagem

    with open('/tmp/robdd_{:02d}.dot'.format(contador_imagem), 'w') as fh:
        fh.write(solution.graphviz())

    contador_imagem += 1