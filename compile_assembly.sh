#!/bin/bash

name="$1"
name="$(basename "${name%.*}")"
as $1 -o "$name.o"
ld "$name.o" -o "build/$name"
