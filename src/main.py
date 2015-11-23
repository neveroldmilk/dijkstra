#!/usr/bin/env python

from dfs import DFS
from graph import Graph

def main():
    g = Graph(100)
    g.generate()
    # g.render()
    # g.static()
    g.render()
    d = DFS()
    v = d.dfs(g.graph, 3)
    print v

if __name__ == '__main__':
    main()
