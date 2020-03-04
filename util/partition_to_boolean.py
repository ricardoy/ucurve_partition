import argparse
from lattice.partition import Partition


class MyVector:
    def __init__(self, *args):
        if len(args) == 1:
            value = args[0]
            if type(value) == int:
                self.v = [0] * value
            elif type(value) == list:
                self.v = value
            elif type(value) == tuple:
                self.v = list(value)
            else:
                raise AttributeError
            self.ini = 1
            self.end = len(self.v)
        elif len(args) == 2:
            if args[0] > args[1]:
                raise AttributeError
            self.ini = args[0]
            self.end = args[1]
            self.v = [0] * (self.end - self.ini + 1)
        else:
            raise AttributeError

    def copy(self):
        c = MyVector(self.ini, self.end)
        c.v = self.v.copy()
        return c

    def __getitem__(self, idx: int):
        if type(idx) != int:
            raise IndexError('invalid type for get {}'.format(idx))

        if idx < self.ini or idx > self.end:
            raise IndexError('invalid index for get {}'.format(idx))

        return self.v[idx - self.ini]

    def __setitem__(self, idx: int, value):
        if type(idx) != int:
            raise IndexError('invalid type for get {}'.format(idx))

        if idx < self.ini or idx > self.end:
            raise IndexError('invalid index for get {}'.format(idx))

        self.v[idx - self.ini] = value

    def __len__(self):
        return len(self.v)

    def __repr__(self):
        return self.v.__repr__()


def _to_decimal(v, n):
    k = 2**(n-1)

    r = 0
    for i in range(n):
        if v[i] == 1:
            r += k
        k = k // 2

    return int(r)


def partition_to_boolean_r(blocks, idx, k, aux, r):
    if idx == k:
        r[_to_decimal(aux, len(aux))] = 1
        return

    for i in blocks[idx]:
        aux[i] = 0

    partition_to_boolean_r(blocks, idx + 1, k, aux, r)

    if idx != 0:
        for i in blocks[idx]:
            aux[i] = 1

        partition_to_boolean_r(blocks, idx + 1, k, aux, r)


def partition_to_boolean(blocks, k):
    r = [0] * (2 ** (k-1))
    r[0] = 1
    aux = [0] * k
    partition_to_boolean_r(blocks, 0, len(blocks), aux, r)
    return r


def visit(a):
    p = Partition(mask=a)
    r = partition_to_boolean(p.blocks, len(p.mask))
    print(p.blocks, r)


def main(n):
    for x in partittion_to_boolean_generator(n):
        visit(x)


def partittion_to_boolean_generator(n):
    # algoritmo do Knuth
    a = MyVector([0] * n)
    b = MyVector([1] * n)
    d = MyVector([1] * n)

    while True:
        p = Partition(mask=a.v)
        r = partition_to_boolean(p.blocks, len(p.mask))
        yield p, r
        j = n
        while a[j] == d[j]:
            d[j] = 1 - d[j]
            j -= 1
        if j == 1:
            return
        if d[j] != 0:
            if a[j] == 0:
                a[j] = b[j]
                m = a[j] + 1

            elif a[j] == b[j]:
                a[j] = b[j] - 1
                m = b[j]
            else:
                a[j] = a[j] - 1
                continue
        else:
            if a[j] == b[j] - 1:
                a[j] = b[j]
                m = a[j] + 1
            elif a[j] == b[j]:
                a[j] = 0
                m = b[j]
            else:
                a[j] = a[j] + 1
                continue

        for k in range(j+1, n+1):
            b[k] = m


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int)

    args = parser.parse_args()
    main(args.n)