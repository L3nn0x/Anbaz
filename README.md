# The Anbaz language
This is an educational language to learn more about language design, compilers, linkers and assemblers.
The goal of the project is to have a language that can compile itself to a binary format.

Explicit non-goal: be 100% compliant with architectures.

This is an educational project. As such, shortcuts will be taken. I'll try to be explicit in supported and non-supported features.

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

# How to use
Right now the project relies on `as` and `ld` to assemble and link on macos.
to compile, run `> ./compile.sh <file>` which will create a `build/` directory with all the generated artifacts (assembly file, object file and resulting binary).
