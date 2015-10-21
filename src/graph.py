#!/usr/bin/env python

from graphviz import Digraph
import numpy.random as nprnd

class Graph(object):
    """Graph class"""
    def __init__(self, max_depth, max_childrens = 4):
        self.graph = dict()
        self.max_depth = max_depth
        self.max_childrens = max_childrens

    def generate(self):
        nodes = xrange(1, self.max_depth)
        for node in nodes:
            children_nodes = nprnd.randint(self.max_depth,
                                           size=self.max_childrens)
            children_nodes = [k for k in children_nodes if k > node]
            self.graph[node] = list(set(children_nodes))

    def render(self):
        u = Digraph('graph', filename='example', format='png')

        for key, values in self.graph.iteritems():
            print "chave:", key,
            print "valores:",
            for v in values:
                print v,
                u.edge(str(key), str(v))
            print '\r'

        u.render()


    def __str__(self):
        return str(self.graph)

    def clear(self):
        self.graph.clear()
