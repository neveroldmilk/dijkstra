# Simple Makefile
# learning in http://www.gnu.org/software/make/manual/make.html#Overview

CC = gcc
CC_FLAGS = -fopenmp
BIN_PATH = bin/
INC_PATH = include/
SRC_PATH = src/

all: main.o gml.o
	$(CC) $(CC_FLAGS) -o $(BIN_PATH)main $(BIN_PATH)main.o $(BIN_PATH)gml.o

gml.o: $(SRC_PATH)gml.c $(INC_PATH)gml.h
	$(CC) $(CC_FLAGS) -I$(INC_PATH) -c $(SRC_PATH)gml.c -o $(BIN_PATH)gml.o

main.o: $(SRC_PATH)main.c $(SRC_PATH)gml.c $(INC_PATH)gml.h
	$(CC) $(CC_FLAGS) -I$(INC_PATH) -c $(SRC_PATH)main.c -o $(BIN_PATH)main.o

clean:
	rm $(BIN_PATH)main.o \
		 $(BIN_PATH)gml.o \
		 $(BIN_PATH)main
