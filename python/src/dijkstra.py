# coding: utf-8

import timeit
import networkx as nx
import matplotlib.pyplot as plt

from itertools import count
from heapq import heappush, heappop

tic = timeit.default_timer()
g = nx.read_gml('../../graphs/graph-1M.gml')
toc = timeit.default_timer()
print 'graph loaded in {0} seconds->'.format(toc - tic)

# draw graph
# pos = nx.spring_layout(g)
# nx.draw_networkx_nodes(g,pos)
# nx.draw_networkx_edges(g,pos)
# nx.draw_networkx_labels(g,pos)
# plt.show()


# dijkstra initialization
# parameters: source, get_weight (function), target (optional)
source = 1;
target = 99999;
weight = 'weight'
g_adj = g.adj
paths = {source: [source]}
pred = None
dist = {} # dictionary of distances
seen = {source: 0} # dictionary of visited vertex
c = count()
fringe = list() # margem?? # pilha?
heappush(fringe, (0, next(c), source))

get_weight = lambda u, v, data: data.get(weight, 1)

# dijkstra main loop
# enable 2 lines below when run into terminal
# figure_order = 0
# plt.savefig("{0}_figure_v{1}.png".format(figure_order, source), format="PNG")

tic = timeit.default_timer()
while fringe:
    (d, _, v) = heappop(fringe)
    if v in dist:
        continue # vertex already visited
    dist[v] = d
    if v == target:
        break

    for u, e in g_adj[str(v)].items():
        cost = get_weight(v, u, e)
        if cost is None:
            continue
        vu_dist = dist[v] + cost
        if u in dist:
            if vu_dist < dist[u]:
                print 'contradictory paths found: negative weights?'
                v = target
                break

        elif u not in seen or vu_dist < seen[u]:
            # draw graph with each of vertex painted
            # nx.draw_networkx_nodes(g,pos, nodelist=[u], node_color="b")
            # plt.savefig("{0}_figure_v{1}.png".format(figure_order, u), format="PNG")
            # figure_order += 1
            seen[u] = vu_dist
            heappush(fringe, (vu_dist, next(c), u))
            if paths is not None:
                paths[u] = paths[v] + [u]
            if pred is not None:
                pred[u] = [v]
        elif vu_dist == seen[u]:
            if pred is not None:
                pred[u].append(v)
toc = timeit.default_timer()


# dijkstra output
print 'graph covered in {0} seconds->'.format(toc - tic)
# print 'dist->', dist
# print 'paths->', paths
print 'shortest path to target', paths[str(target)]


# In[ ]:
