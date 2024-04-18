# The Anbaz language
This is an educational language to learn more about language design, compilers, linkers and assemblers.
The goal of the project is to have a language that can compile itself to a binary format.

# The Anbaz language
The target for the language is for now a subset of C. Changes will happen later to diverge a little (for example references instead of pointers etc...) to experiment.

# The compiler
The compiler is currently bootstraped with python code and is split in 2:
- The frontend that takes Anbaz and emits [Bril](https://capra.cs.cornell.edu/bril/intro.html) (in progress).
- The backend that takes a Bril output and emits assembly (currently targetting marm64 and maybe x64 later) (TODO).

# The assembler
The assembler takes assembly and transpiles to machine code (TODO).

# The linker
The linker that links and produces an executable (TODO).
