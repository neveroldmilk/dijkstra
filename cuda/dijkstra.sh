#!/bin/bash

GRAPH="../graphs/$1"
NUMBER_OF_LINES=`grep -c "." $GRAPH`

./bin/main $NUMBER_OF_LINES $GRAPH
