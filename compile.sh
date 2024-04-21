#!/bin/bash

mkdir -p build

name="$1"
name="$(basename "${name%.*}")"
python -m frontend $1 | python -m backend > "build/$name.s"
./compile_assembly.sh "build/$name.s"
