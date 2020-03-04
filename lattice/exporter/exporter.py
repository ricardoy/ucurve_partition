import numpy as np
import sys
from collections import defaultdict
from contextlib import contextmanager
from lattice import SimpleNode


@contextmanager
def file_writer(file_name=None):
    if file_name is None:
        writer = sys.stdout
    else:
        writer = open(file_name, 'w')

    yield writer

    if file_name is not None:
        writer.close()


class LatexExporter(object):
    def __init__(self, lattice, width_coef=1., height_coef=1.):
        self.lattice = lattice
        self.width_coef = width_coef
        self.height_coef = height_coef

    def node_value_to_latex(self, value):
        return value

    def generate_node(self, node:SimpleNode, x, y):
        return '\\node ({}) at ({}, {}) {{{}}};\n'.format(
            node.id,
            x,
            y,
            self.node_value_to_latex(node.value))

    def get_level(self, node):
        return node.height

    def process_nodes(self):
        visited_nodes = set()
        total_nodes_by_level = defaultdict(int)
        for node in self.lattice:
            if node in visited_nodes:
                continue
            visited_nodes.add(node)
            level = self.get_level(node)
            total_nodes_by_level[level] += 1

        s = ''
        current_total_by_level = defaultdict(int)
        visited_nodes.clear()
        for node in self.lattice:
            if node in visited_nodes:
                continue
            visited_nodes.add(node)
            level = self.get_level(node)

            current_total_by_level[level] += 1

            if total_nodes_by_level[level] == 1:
                x = 0
            elif total_nodes_by_level[level] % 2 == 0:
                if current_total_by_level[level] / float(total_nodes_by_level[level]) > 0.5:
                    x = total_nodes_by_level[level] - current_total_by_level[level]
                else:
                    x = -1 * current_total_by_level[level]
                x += 0.5
            else:
                median = total_nodes_by_level[level] // 2 + 1
                if current_total_by_level[level] == median:
                    x = 0
                else:
                    x = current_total_by_level[level] - median

            s += self.generate_node(node, x*self.width_coef, level*self.height_coef)

        return s

    def process_edges(self):
        s = ''
        for node in self.lattice:
            for child in node.successors:
                s += '\\draw ({}) -- ({});\n'.format(node.id, child.id)
        return s

    def export(self, generate_header_footer=True):
        if generate_header_footer:
            s = """
            \\documentclass[a1paper]{slides}
            \\usepackage[margin=0pt]{geometry}
            \\usepackage{tikz}
            \\begin{document}\n"""
        else:
            s = ''

        s += '\\begin{tikzpicture}\n'

        s = s + self.process_nodes()
        s = s + self.process_edges()

        s += '\\end{tikzpicture}'

        if generate_header_footer:
            s = s + '\\end{document}'

        return s


def grid_to_latex(v, h=.1, w=.1):
    s = ''
    rows = len(v)
    for i, row in enumerate(v):
        i = rows - i - 1
        for j, elem in enumerate(row):
            if elem > 0:
                s += '\\fill ({:.5f}, {:.5f}) rectangle ({:.5f}, {:.5f});\n'.format(h*(j), w*(i), h*(j+1), w*(i+1))
            else:
                s += '\\draw ({:.5f}, {:.5f}) rectangle ({:.5f}, {:.5f});\n'.format(h * (j), w * (i), h * (j + 1),                                                                                 w * (i + 1))
    return s


class LatexExporterGrid(LatexExporter):
    def __init__(self, *args, **kwargs):
        LatexExporter.__init__(self, *args, **kwargs)
        self.h_grid = .1
        self.w_grid = .1
        self.ordered_dimensions = None

    def node_value_to_latex(self, value):
        s = '\\begin{tikzpicture}\n'
        s += grid_to_latex(value, self.h_grid, self.w_grid)
        s += '\\end{tikzpicture}'
        return s

    def export(self, generate_header_footer=False):
        if generate_header_footer:
            s = """
            \\documentclass[a1paper]{slides}
            \\usepackage[margin=0pt]{geometry}
            \\usepackage{tikz}
            \\begin{document}\n"""
        else:
            s = ''

        s += '\\begin{tikzpicture}\n'

        s = s + self.process_nodes()
        s = s + self.process_edges()

        s += '\\end{tikzpicture}'

        if generate_header_footer:
            s = s + '\\end{document}'

        return s

    def _process_dimensions(self):
        dimensions = set()
        for x in self.lattice.nodes:
            dimensions.add(np.array(x.value).sum())

        self.ordered_dimensions = dict()

        for i, x in enumerate(sorted(dimensions)):
            self.ordered_dimensions[x] = i

    def get_level(self, node):
        if self.ordered_dimensions is None:
            self._process_dimensions()

        return self.ordered_dimensions[np.array(node.value).sum()]


def export_latex(lattice, output_file_name=None, generate_document=True, width_coef=1, height_coef=1):
    le = LatexExporter(lattice,
                       width_coef=width_coef,
                       height_coef=height_coef)
    with file_writer(output_file_name) as writer:
        writer.write(le.export(generate_document))


def export_latex_grid(lattice, output_file_name=None, generate_document=True, width_coef=1, height_coef=.5):
    le = LatexExporterGrid(lattice,
                           width_coef=width_coef,
                           height_coef=height_coef)
    with file_writer(output_file_name) as writer:
        writer.write(le.export(generate_document))