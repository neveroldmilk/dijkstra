/*
 * gml file
 * filename: gml.c
 */

#include <stdio.h>
#include "gml.h"

int main(int argc, char const *argv[]) {
  FILE *fp;
  printf("Dijkstra\n");
  printf("graph used: %s\n", argv[1]);
  fp = gml_open(argv[1]);
  gml_reader(fp);
  gml_close(fp);
  return 0;
}
