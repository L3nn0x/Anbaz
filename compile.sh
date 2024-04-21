#!/bin/bash

mkdir -p build

name="$1"
name="$(basename "${name%.*}")"
python -m frontend $1 | python backend.py > "build/$name.s"
./compile_assembly.sh "build/$name.s"
