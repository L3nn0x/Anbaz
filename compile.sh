#!/bin/bash

mkdir -p build

python frontend.py $1 | python backend.py > "build/$1.s"
./compile_assembly.sh "build/$1.s"
