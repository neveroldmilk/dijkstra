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
    tic = timeit.default_timer()
    import pycuda.autoinit
    import pycuda.driver as cuda
    from pycuda.compiler import SourceModule
    toc = timeit.default_timer()
    print 'cuda import: {0} seconds.'.format(toc - tic)

MAX_WEIGHT = 1000

if PYCUDA:
    MOD = SourceModule("""
    #include <stdio.h>
    __device__ int numV = 8;
    __global__ void Find_Vertex(int *weight_matrix, int *visited, int *len, int *updlen) {
        int u = threadIdx.x; // source
        if (visited[u] == 0) {
            visited[u] = 1;
            int v;
            for (v = 0; v < numV; v++) {
                int w = weight_matrix[u*numV + v]; //find_edge
                if (w < 1000) {
                    if (updlen[v] > len[u] + w) {
                        updlen[v] = len[u] + w;
                    }
                }
            }
        }
    }

    __global__ void Update_Paths(int *visited, int *len, int *updlen)
	{
         int u = threadIdx.x;
         if(len[u] > updlen[u])
           {
                len[u] = updlen[u];
                visited[u] = 0; //FALSO
            }

         updlen[u] = len[u];
        }

    """)

def cuda_proccess(weight_matrix, vertices, visited, lenx, updlenx):
    # init variables to device
    tic = timeit.default_timer()
    weight_matrix_gpu = cuda.mem_alloc(weight_matrix.size * weight_matrix.dtype.itemsize)
    visited_gpu = cuda.mem_alloc(visited.size * visited.dtype.itemsize)
    len_gpu = cuda.mem_alloc(lenx.size * lenx.dtype.itemsize)
    updlen_gpu = cuda.mem_alloc(updlenx.size * updlenx.dtype.itemsize)
    toc = timeit.default_timer()
    print 'memory alloc on device: {0} seconds.'.format(toc - tic)

    tic = timeit.default_timer()
    cuda.memcpy_htod(weight_matrix_gpu, weight_matrix)
    cuda.memcpy_htod(visited_gpu, visited)
    cuda.memcpy_htod(len_gpu, lenx)
    cuda.memcpy_htod(updlen_gpu, updlenx)
    toc = timeit.default_timer()
    print 'memory copy from host to device: {0} seconds.'.format(toc - tic)

    _find_vertex = MOD.get_function("Find_Vertex")
    _update_paths = MOD.get_function("Update_Paths")

    for i in xrange(vertices.size):
        _find_vertex(
            weight_matrix_gpu,
            visited_gpu,
            len_gpu,
            updlen_gpu,
            block=(numV,1,1))
        for k in xrange(vertices.size):
            _update_paths(visited_gpu, len_gpu, updlen_gpu,block=(numV,1,1))

    tic = timeit.default_timer()
    cuda.memcpy_dtoh(visited, visited_gpu)
    cuda.memcpy_dtoh(lenx, len_gpu)
    cuda.memcpy_dtoh(updlenx, updlen_gpu)
    toc = timeit.default_timer()
    print 'memory copy from device to host: {0} seconds.'.format(toc - tic)
    print "new len"
    print lenx

def print_info():
    device = pycuda.autoinit.device
    print "Model: {0}".format(device.name())

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

    tic = timeit.default_timer()
    vertices = np.array(g.nodes()).astype(np.int32)
    weight_matrix = nx.to_numpy_matrix(g,
        nodelist=sorted(g.nodes()),
        dtype=np.int32,
        nonedge=MAX_WEIGHT
    )
    numV = vertices.size
    visited = np.zeros_like(vertices).astype(np.int32)
    weights = np.zeros_like(vertices).astype(np.int32)
    lenx = np.zeros_like(vertices).astype(np.int32)
    updlenx = np.zeros_like(vertices).astype(np.int32)
    tmp = np.zeros_like(vertices).astype(np.int32)
    wmf = weight_matrix.getA1().astype(np.int32)
    toc = timeit.default_timer()
    print 'load data: {0} seconds.'.format(toc - tic)

    source = 0
    for i in xrange(vertices.size):
        if i == source:
            lenx[i] = 0
        else:
            lenx[i] = _find_weight(source, vertices[i], weight_matrix)
            updlenx[i] = lenx[i]

    print "old len"
    print lenx

    if PYCUDA:
        cuda_proccess(wmf, vertices, visited, lenx, updlenx)
