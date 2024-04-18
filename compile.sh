#!/bin/bash

python frontend.py $1 | python backend.py > "$1.s"
./compile_assembly.sh "$1.s"
