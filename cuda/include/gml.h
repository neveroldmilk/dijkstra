/*
 * GML header file
 * filename: gml.h
 */

FILE* gml_open(char const *path);
void gml_close(FILE *fp);
void gml_reader(FILE *fp, int nl);
int gml_parser(char *line);
