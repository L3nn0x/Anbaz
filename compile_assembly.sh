#!/bin/bash

nasm -fmacho64 $1 -o "$1.o"
ld -static "$1.o" -o "build/a.out"
