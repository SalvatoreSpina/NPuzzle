#!/bin/bash

if [ $# -eq 1 ]; then
    if [ "$1" = "u" ]; then
        python puzzle_generator.py 3 -u > test && python3 srcs/main.py test
    else
        echo "Invalid argument: $1"
    fi
else
    python puzzle_generator.py 3 -s > test && python3 srcs/main.py test
fi
