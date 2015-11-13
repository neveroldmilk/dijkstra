#!/usr/bin/env python

import os
import sys
import scipy
import timeit
import argparse

from dfs import DFS
from graph import MyGraph
try:
    import graph_tool.all as gt
    GT_ENABLED = True
except ImportError as e:
    print "error while import: {0}".format(e)
    GT_ENABLED = False

CWD = os.getcwd()

def main_parser():
    parser = argparse.ArgumentParser(prog='dfs')
    parser.add_argument("-g", "--graph",
        help="set graph file to be used",
        dest="graph_name")
    args = parser.parse_args()

    if not args.graph_name:
        print parser.print_help()
        sys.exit(-1)
    else:
        print args.graph_name


def main():
    g = MyGraph(100)
    graph = g.generate()
    # graph = g.static()
    d = DFS()
    v = d.dfs(g.graph, 1)
    print v
    g.render()

def main_gt():
    if GT_ENABLED:
        conf()
        info()
    else:
        print "graph_tool module was not import properly"
        sys.exit(-1)
    pass

def conf():
    print "--- configuring module ---"
    pass

def info():
    print "--- info about graph_tool module ---"
    print "\t* openmp enabled? {0}".format(gt.openmp_enabled())
    print "\t* number of threads: {0}".format(gt.openmp_get_num_threads())
    print "\t* graph used: {0}".format('graph-1M.gml')


if __name__ == '__main__':
    main_parser()
    main_gt()
