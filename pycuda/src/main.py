#!/usr/bin/env python

import os
import sys
import numpy
import timeit
import argparse
import networkx as nx

GRAPHS_DIRECTORY = os.path.abspath(
    os.path.join(__file__, '../../../graphs')) + '/{0}'
PYCUDA = False
if PYCUDA:
    import pycuda.autoinit
    import pycuda.driver as cuda
    from pycuda.compiler import SourceModule

MAX_WEIGHT = 10000

if PYCUDA:
    MOD = SourceModule("""
    __global__ void Find_Vertex(int *vertices, int *edges, int *weights, int *length, int *updateLength) {
        int source = threadIdx.x; // source
        if(vertices[source].visited == FALSE) {
            vertices[u].visited = TRUE;

            int v;
            for(v = 0; v < V; v++) {
                // Find the weight of the edge
                int weight = findEdge(vertices[u], vertices[v], edges, weights);

                // Checks if the weight is a candidate
                if(weight < MAX_WEIGHT) {
                    // If the weight is shorter than the current weight, replace it
                    if(updateLength[v] > length[u] + weight) {
                        updateLength[v] = length[u] + weight;
                    }
                }
            }
        }
    }
    __host__ int findEdge(Vertex u, Vertex v, Edge *edges, int *weights) {
        int i;
        for(i = 0; i < E; i++) {
            if(edges[i].u == u.title && edges[i].v == v.title) {
                return weights[i];
            }
        }
    return MAX_WEIGHT;
    }
    """)

def cuda_proccess(verticies, edges, weights):
    pass

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

def _find_weight(source, target, edges, weights):
    for i, k in enumerate(edges):
        # k[0] = source; k[1] = target
        if k[0] == source and k[1] == target:
            return weights[i]
    return MAX_WEIGHT

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
    args = main_parser()
    g = load_gml(args)

    edges = g.edges()
    verticies = [dict(id=k, visited=False) for k in g.nodes()]
    weights = tuple([w['weight'] for (source, target, w) in g.edges(data=True)])

    print verticies
    print edges
    print _find_weight(0, 4, edges, weights)
    if PYCUDA:
        cuda_proccess(verticies, edges, weights)
