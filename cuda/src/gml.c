/*
 * gml file
 * filename: gml.c
 */

#include <stdio.h>
#include <string.h>
#include "gml.h"

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

void gml_reader(FILE *fp) {
  char line[20];
  while (fgets(line, sizeof line, fp) != NULL) {
    gml_parser(line);
  }
}

void gml_parser(char *line) {
  char *delimeter = " ";
  char *token;
  char *directed = "directed";
  char *node = "node";
  token = strtok(line, delimeter);
  while (token != NULL) {
    if (!strcmp(token, directed)) {
      printf("%s\n", token);
      token = strtok(NULL, delimeter);
      printf("%s\n", token);
    }
    token = strtok(NULL, delimeter);
  }
}
