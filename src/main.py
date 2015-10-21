#!/usr/bin/env python

from dfs import DFS
from graph import Graph

def main():
    g = Graph(100)
    g.generate()
    g.render()

if __name__ == '__main__':
    main()
