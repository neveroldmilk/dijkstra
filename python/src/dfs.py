#!/usr/bin/env python


class DFS(object):
    """implement DFS algorithm"""
    def __init__(self):
        pass

    def dfs(self, graph, start):
        visited, stack = set(), [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(graph[node] - visited)
        return visited
