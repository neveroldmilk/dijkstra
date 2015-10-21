#!/usr/bin/env python


class DFS(object):
    """implement DFS algorithm"""
    def __init__(self):
        pass

    def dfs(self, start, graph):
        visited, stack = set(), [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(self.graph[node] - visited)
        return visited
