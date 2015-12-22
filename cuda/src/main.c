/*
 * gml file
 * filename: gml.c
 */

/*
 * input options
 * argv[1] -> number of lines (nl) in the graph file
 * argv[2] -> the graph file
 */

#include <stdio.h>
#include "gml.h"

int main(int argc, char const *argv[]) {
  FILE *fp;
  int nl = atoi(argv[1]);
  char *lines[nl];
  char *graph = argv[2];

  printf("Dijkstra\n");
  printf("graph used: %s\n", argv[2]);

  fp = gml_open(graph);
  gml_reader(fp, nl);
  gml_close(fp);
  return 0;
}
