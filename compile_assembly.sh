#!/bin/bash

as $1 -o "$1.o"
ld "$1.o" -o "build/a.out"
