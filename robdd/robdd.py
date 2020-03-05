#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from typing import List

from random import choice

from collections import deque, defaultdict
from robdd.ite import Ite


version = sys.version
if version[0] == '2':
    from sys import maxint
elif version[0] == '3':
    from sys import maxsize as maxint


class Robdd:

    # static helper methods

    @staticmethod
    def true():
        return Robdd.make(Ite(1, 1, 1))

    @staticmethod
    def false():
        return Robdd.make(Ite(1, 0, 0))

    @staticmethod
    def make_x(i):
        return Robdd.make(Ite(i, 1, 0))

    @staticmethod
    def make_not_x(i):
        return Robdd.make(Ite(i, 0, 1))

    @staticmethod
    def make(_ite):
        r = Robdd()
        r.build(_ite)
        return r

    # instance definition

    def __init__(self):
        self.clear()

    def clear(self):
        self.items = [] 
        self.inverse = {}

        self.variables = []

        self.insert_attempts = 0
        self.insert_distinct = 0
        
        self.root = None # root of the robdd tree

        self._insert(maxint, None, None) # inserts a node for True
        self._insert(maxint, None, None) # inserts a node for False


    # builds a structure from a Ite expression
    def build(self, expression, clear=False) :

        if not isinstance(expression, Ite) :
            raise Exception("Expression is not an Ite class object")

        if clear == True :
            self.clear()

        self.root = self._build(expression)

        return self.root

    def _build(self, expression) :
        
        inserting_t = expression.t if expression.t_is_bool() else self._build(expression.t)
        inserting_f = expression.f if expression.f_is_bool() else self._build(expression.f)

        return self.insert(expression.i, inserting_t, inserting_f)


    # inserts nodes w/ redundancy check
    # Num i - variable number
    # Num t - variable number of the T child
    # Num f - variable number of the F child
    def insert(self, i, t, f):

        self.insert_variable(i)
        self.insert_attempts += 1

        if t == f :
            # the t and the f children are equal, 
            # so the i variable can be ignored
            self.root = t
            return t

        # check if this is a redundant node
        n = self.find_by_inverse(i, t, f)

        if n == None :
            n = self._insert(i, t, f)
            self.insert_distinct += 1

        self.root = n

        return n

    def insert_variable(self, i):
        if i in self.variables :
            return

        self.variables.append(i)

    def _insert(self, v, t, f) :
        index = len(self.items)

        self.items.append((v, t, f))
        self.inverse[(v, t, f)] = index

        return index

    def find_by_inverse(self, v, t, f):
        return self.inverse[(v, t, f)] if (v, t, f) in self.inverse else None

    def __str__(self):
        return self.show(self.root)

    def show(self, index, ident=0):
        ident_str = ident * " "

        if index <= 1 :
            return ident_str + str(index)

        i, t, f = self.items[index]

        return ident_str + "x{}\n".format(i) + \
            self.show(t) + "\n" + \
            self.show(f)

    def list(self):
        result = ""

        for index in range(len(self.items)):
            i, t, f = self.items[index]
            result += "{} ({}, {}, {})\n".format(index, i, t, f)

        return result

    def get_root(self):
        return (len(self.items) - 1) if self.root == None else self.root

    def solutions_len(self):
        return self._solutions_len(self.get_root())

    def _solutions_len(self, index):
        if index < 0 :
            raise Exception("invalid index")

        if index < 2 :
            return index

        i, t, f = self.items[index]

        return self._solutions_len(t) + self._solutions_len(f)

    def get_solutions(self, expected_solution):
        assert(expected_solution == 0 or expected_solution == 1)
        return self._get_solutions(self.get_root(), expected_solution)

    def _get_solutions(self, index, expected_solution=1):
        result = []

        i, t, f = self.items[index]

        result.extend(self._get_solutions_in_child(i, t, True, expected_solution))
        result.extend(self._get_solutions_in_child(i, f, False, expected_solution))

        return result

    def _get_solutions_in_child(self, current_index, child_index, child_type, expected_solution):
        if child_index < 0:
            raise Exception("Invalid index in T child")

        # print 'child index: {} | {} | current index: {} | child type: {}'.format(child_index, child_index <= 1, current_index, child_type)

        if child_index <= 1:
            if child_index == expected_solution:
                return [{current_index: child_type}]
            else:
                return []

        # now child index is greater than 1

        child_solutions = self._get_solutions(child_index, expected_solution)
        result = []

        for solution in child_solutions:
            solution[current_index] = child_type
            result.append(solution)

        return result


    def evaluate(self, expression:List[int]):
        v = self.get_root()

        if v == 0:
            return False
        elif v == 1:
            return True

        while True:
            i, t, f = self.items[v]
            if expression[i] == 0:
                v = f
            else:
                v = t

            if v == True:
                return True
            elif v == False:
                return False


    def get_index(self, idx):
        i, t, f = self.items[idx]
        if t == False:
            t = 0
        elif t == True:
            t = 1

        if f == False:
            f = 0
        elif f == True:
            f = 1

        return i, t, f


    #TODO: se uma variável é don't care, o zero é sempre escolhido
    def get_random_solution(self, expected_solution:int=1):
        '''
        :param expected_solution: 0 ou 1
        :return: um vetor Booleana que é mapeado para a solução expected_solution
        '''
        r = [0] * len(self.variables)
        v = self.get_root()
        if v <= 1:
            if v == expected_solution:
                return r
            else:
                return None

        while v > 1:
            i, t, f = self.get_index(v)
            if t <= 1 and t != expected_solution:
                nextv = f
            elif f <= 1 and f != expected_solution:
                nextv = t
            else:
                nextv = choice([t, f])

            if nextv == t:
                r[i] = 1

            v = nextv

        return r

    def graphviz(self, path=None):
        # if path is not None:
        #     path = path + '1'

        s = 'graph D {\n'
        s += '    node[shape=circle];\n'
        s += self.graphviz_nodes_and_edges(path)
        s += '}'
        return s

    def graphviz_nodes_and_edges(self, path):
        if self.get_root() == 0:
            return 'false [shape=square, label=0];\n'
        elif self.get_root() == 1:
            return 'true [shape=square, label=1];\n'

        s = ''
        if len(self.get_solutions(0)) > 0:
            s += 'false [shape=square, label=0];\n'
        if len(self.get_solutions(1)) > 0:
            if path is None:
                s += 'true [shape=square, label=1];\n'
            else:
                s += 'true [shape=square, label=1, style=filled, fillcolor=green];\n'


        queue = deque()
        i, t, f = self.items[self.get_root()]

        queue.append((self.get_root(), i, t, f))

        nodes = dict()
        rank = defaultdict(set)

        contador = 0

        while len(queue) > 0:
            # print ''
            contador += 1
            x, i, t, f = queue.popleft()

            # print 'evaluating node ', i, x

            # print x, i, t, f
            # print t is True, t is False, f is True, f is False

            if x not in nodes:
                # if marked:
                #     s += 'x{} [label=<X<SUB>{}</SUB>> style=filled, fillcolor=green]\n'.format(x, i)
                # else:
                #     s += 'x{} [label=<X<SUB>{}</SUB>>]\n'.format(x, i)
                if i == 0:
                    if path is None:
                        nodes[x] = (i, False)
                    else:
                        nodes[x] = (i, True)
                else:
                    nodes[x] = (i, False)
                if i < maxint:
                    rank[i].add(x)
            else:
                continue

            if t is True:
                s += 'x{}--true [];\n'.format(x)
            elif t is False:
                s += 'x{}--false [];\n'.format(x)
            else:
                i_, t_, f_ = self.items[t]
                s += 'x{}--x{};\n'.format(x, t)
                # print 'append:' ,(t, i_, t_, f_), contador
                queue.append((t, i_, t_, f_))

            if f is True:
                s += 'x{}--true [style=dotted];\n'.format(x)
            elif f is False:
                s += 'x{}--false [style=dotted];\n'.format(x)
            else:
                i_, t_, f_ = self.items[f]
                s += 'x{}--x{} [style=dotted];\n'.format(x, f)
                # print 'append:', (f, i_, t_, f_), contador
                # queue.append((f, i_, t_, f_, False))
                queue.append((f, i_, t_, f_))

        # print nodes

        if path is not None:
            x = self.get_root()
            while x > 1:
                print(x)
                i, t, f = self.items[x]
                if path[i] == '1':
                    i_, t_, f_ = self.items[t]
                    if i_ < maxint:
                        nodes[t] = (i_, True)
                    x = t
                else:
                    i_, t_, f_ = self.items[f]
                    if i_ < maxint:
                        nodes[f] = (i_, True)
                    x = f

        for x, (i, marked) in nodes.items():
            if marked:
                s += 'x{} [label=<X<SUB>{}</SUB>> style=filled, fillcolor=green]\n'.format(x, i)
            else:
                s += 'x{} [label=<X<SUB>{}</SUB>>]\n'.format(x, i)

        for v in rank.values():
            s += '{{rank=same; {};}}'.format('; '.join(['x{}'.format(x) for x in v]))

        return s

