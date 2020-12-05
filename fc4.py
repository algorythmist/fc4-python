import csv
import os
from graphviz import Digraph


class Weapon:

    def __init__(self, name, type, stats):
        self.name = name.strip()
        self.type = name.strip()
        self.stats = [int(s) for s in stats.strip().split('/')]

    def __str__(self):
        return self.name + '\n' + str(self.stats)

    def __lt__(self, other):
        return all(self.stats[i] <= other.stats[i] for i in range(len(self.stats)))

    def __gt__(self, other):
        return other < self


# Read CSV and convert to list of weapons
def read_weapons(filename):
    with (open(filename)) as file:
        reader = csv.reader(file)
        return [Weapon(row[0], row[1], row[2]) for row in reader]


def build_graph(weapons, name):
    g = Digraph(name, filename=name + '.dot')
    # set some formatting attributes
    g.attr('node', shape='box')
    g.attr('node', style='filled')
    g.attr('node', fillcolor='azure')
    # add all weapons as vertices
    [g.node(str(weapon)) for weapon in weapons]
    # Add edges between nodes that are comparable
    for i in range(len(weapons) - 1):
        for j in range(i + 1, len(weapons)):
            if weapons[i] > weapons[j]:
                g.edge(str(weapons[i]), str(weapons[j]))
            elif weapons[i] < weapons[j]:
                g.edge(str(weapons[j]), str(weapons[i]))
    return g


def build_graph_for_file(filename):
    weapons = read_weapons(filename + '.csv')
    return build_graph(weapons, filename)


# Use the command line tool for transitive reduction
def transitive_reduction(name):
    tred_command = 'tred {name}.dot > {name}.reduced.dot'.format(name=name)
    os.system(tred_command)
    pdf_command = 'dot -Tpng {name}.reduced.dot -o {name}.reduced.png'.format(name=name)
    os.system(pdf_command)


if __name__ == '__main__':
    g1 = build_graph_for_file('sidearms')
    g2 = build_graph_for_file('weapons')
    g1.save()
    g2.save()
    transitive_reduction('sidearms')
    transitive_reduction('weapons')
