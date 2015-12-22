/*
 * gml file
 * filename: gml.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "gml.h"


#define NUM_V 0;

FILE* gml_open(char const *path) {
    FILE *fp = fopen(path, "r");
    if (fp == NULL) {
        printf("The file didn't open.\n");
        return 0;
    }
    return fp;
}
void gml_close(FILE *fp) {
  close(fp);
}

void gml_reader(FILE *fp, int nl) {
  int v;
  char line[20];
  char *lines[nl];
  int k = 0;
  while (fgets(line, sizeof line, fp) != NULL) {
    lines[k] = malloc(256 * sizeof(char));
    strcpy(lines[k], line);
    k++;
  }

  // v = gml_parser(line);
  for (int k = 0; k < nl; k++) {
    printf("%s", lines[k]);
  }
}

int gml_parser(char *line) {
  char *delimeter = " ";
  char *token;
  char *directed = "directed";
  char *node = "node";
  char *edge = "edge";
  char *source = "source";
  char *target = "target";
  token = strtok(line, delimeter);
  while (token != NULL) {
    if (!strcmp(token, directed)) {
      printf("%s\n", token);
      return 0;
    }

    else if (!strcmp(token, node)) {
      return 1; // compute node
    }

    else if (!strcmp(token, edge)) {
      return 2; // compute edge
    }

    else if (!strcmp(token, source)) {
      printf("%s\n", source);
      token = strtok(NULL, delimeter);
      printf("%s\n", token);
    }
    token = strtok(NULL, delimeter);
  }
  return 0;
}
