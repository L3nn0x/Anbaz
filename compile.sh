#!/bin/bash

mkdir -p build

python -m frontend $1 | python backend.py > "build/$1.s"
./compile_assembly.sh "build/$1.s"
