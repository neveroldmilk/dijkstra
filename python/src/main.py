#!/usr/bin/env python

from dfs import DFS
from graph import Graph

def main():
    g = Graph(100)
    graph = g.generate()
    # graph = g.static()
    d = DFS()
    v = d.dfs(g.graph, 1)
    print v
    g.render()

if __name__ == '__main__':
    main()
