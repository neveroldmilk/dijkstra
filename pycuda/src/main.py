#!/usr/bin/env python

import os
import sys
import timeit
import argparse
import numpy as np
import networkx as nx
from collections import namedtuple

GRAPHS_DIRECTORY = os.path.abspath(
    os.path.join(__file__, '../../../graphs')) + '/{0}'
PYCUDA = True
if PYCUDA:
    import pycuda.autoinit
    import pycuda.driver as cuda
    from pycuda.compiler import SourceModule

MAX_WEIGHT = 1000

if PYCUDA:
    MOD = SourceModule("""
    __global__ void Find_Vertex(int *weight_matrix, int *verticies, int *visited, int *weights, int numV) {
        int u = threadIdx.x; // source
        if (visited[u] == 0) {
            visited[u] = numV;
            int v;
            for (v = 0; v < numV; v++) {
               int w = weight_matrix[u*numV + v];
               if (w != 0) {
                   weights[v] = w;
               }
            }

        }
    }
    """)

def cuda_proccess(weight_matrix, verticies, visited, weights, numV):
    # init variables to device
    weight_matrix_gpu = cuda.mem_alloc(weight_matrix.size * weight_matrix.dtype.itemsize)
    verticies_gpu = cuda.mem_alloc(verticies.size * verticies.dtype.itemsize)
    visited_gpu = cuda.mem_alloc(visited.size * visited.dtype.itemsize)
    weights_gpu = cuda.mem_alloc(weights.size * weights.dtype.itemsize)
    # numV_gpu = cuda.mem_alloc(sys.getsizeof(numV))

    cuda.memcpy_htod(weight_matrix_gpu, weight_matrix)
    cuda.memcpy_htod(verticies_gpu, verticies)
    cuda.memcpy_htod(visited_gpu, visited)
    cuda.memcpy_htod(weights_gpu, weights)

    _find_vertex = MOD.get_function("Find_Vertex")
    _find_vertex(
        weight_matrix_gpu,
        verticies_gpu,
        visited_gpu,
        weights_gpu,
        np.int32(numV),
        block=(numV,1,1))

    # dest = np.zeros_like(dest)
    cuda.memcpy_dtoh(verticies, verticies_gpu)
    cuda.memcpy_dtoh(visited, visited_gpu)
    cuda.memcpy_dtoh(weights, weights_gpu)
    print "verticies visited"
    print visited
    print "weights"
    print weights


def print_info():
    device = pycuda.autoinit.device
    giga = 1073741824.0
    print "Model: {0}".format(device.name())
    print "Memory: {:.03} (in GigaBytes)".format(device.total_memory() / giga)

# reading gml
def load_gml(args):
    tic = timeit.default_timer()
    graph = GRAPHS_DIRECTORY.format(args.graph_name)
    g = nx.read_gml(graph)
    toc = timeit.default_timer()
    print 'graph loaded in {0} seconds.'.format(toc - tic)
    return g

def _find_weight(source, target, weight_matrix):
    return weight_matrix[source, target]

# parsing values
def main_parser():
    parser = argparse.ArgumentParser(prog='dijkstra')
    parser.add_argument("-g", "--graph",
        help="set graph file to be used with option -g",
        dest="graph_name")
    args = parser.parse_args()

    if not args.graph_name:
        print parser.print_help()
        sys.exit(-1)
    return args

if __name__ == '__main__':
    # Vertex = namedtuple("Vertex", ["id", "visited"])
    args = main_parser()
    g = load_gml(args)

    edges = g.edges()
    verticies = np.array(g.nodes()).astype(np.int32)
    weight_matrix = nx.to_numpy_matrix(g,
        nodelist=sorted(g.nodes()),
        dtype=np.int32,
        # nonedge=MAX_WEIGHT
    )

    wv = weight_matrix.flatten()
    print wv

    numV = len(verticies)
    visited = np.zeros_like(verticies).astype(np.int32)
    weights = np.zeros_like(verticies).astype(np.int32)
    # verticies = [dict(id=k, visited=0) for k in g.nodes()]
    # weights = tuple([w['weight'] for (source, target, w) in g.edges(data=True)])
    # verticies = [Vertex(id=i, visited=0) for i in g.nodes()]

    print weight_matrix
    print visited
    if PYCUDA:
        cuda_proccess(weight_matrix, verticies, visited, weights, numV)
