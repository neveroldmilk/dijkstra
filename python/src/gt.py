import scipy
import timeit
import numpy as np
from graph_tool.all import *

gt_generation = graph_tool.generation
gt_draw = graph_tool.draw
gt_search = graph_tool.search

# print graph_tool.show_config()
# graph_tool.openmp_set_num_threads(1)

def sample_k(max):
  accept = False
  while not accept:
    k = np.random.randint(1,max+1)
    accept = np.random.random() < 1.0/k
  return k

def simple_k(max):
    k = np.random.randint(1, max+1)
    return k

class VisitorExample(gt_search.DFSVisitor):

    def __init__(self, pred, time):
        self.pred = pred
        self.time = time
        self.last_time = 0

    def discover_vertex(self, u):
        # print("-->", u, "has been discovered!")
        self.time[u] = self.last_time
        self.last_time += 1

    # def examine_edge(self, e):
        # print("edge (%s, %s) has been examined..." % \
            # (e.source(), e.target()))

    def tree_edge(self, e):
        self.pred[e.target()] = int(e.source())


##### generating graph #####
p = scipy.stats.poisson
tic=timeit.default_timer()
g = gt_generation.random_graph(100000, lambda: (sample_k(19), sample_k(19)),
    model="probabilistic",
    vertex_corr=lambda a,b: (p.pmf(a[0], b[1]) *p.pmf(a[1], 20 - b[0])),
    n_iter=100)
toc = timeit.default_timer()
print "graph generate in: {0} seconds".format(toc - tic)

##### applying labels #####
label = g.new_vertex_property("string")
g.vp.label = label
tic=timeit.default_timer()
for v in g.vertices():
    g.vp.label[v] = g.vertex_index[v]
toc = timeit.default_timer()
print "applying labels took {0} seconds".format(toc - tic)

##### loading graph #####
# tic=timeit.default_timer()
# g = load_graph('../graphs/graph-1M.gml')
# toc = timeit.default_timer()
# print "graph loaded in: {0} seconds".format(toc - tic)

# time = g.new_vertex_property("int")
# pred = g.new_vertex_property("int64_t")
# tic = timeit.default_timer()
# gt_search.dfs_search(g, g.vertex(0), VisitorExample(time, pred))
# for k in xrange(10):
# gt_search.bfs_search(g, g.vertex(0), BFSVisitor())
# toc = timeit.default_timer()
# print "graph covered in: {0} seconds".format(toc - tic)

# drawing graph
# gt_draw.graph_draw(g, output="graph-100k.svg")
# saving grpahs into gml format
g.save('graph-100k.gml')
