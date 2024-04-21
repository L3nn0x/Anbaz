.section __TEXT,__text
.p2align 2
.globl _main

_main:
bl main
ldr x16, =0x2000001
svc #0x80

.globl main
main:
mov x0, #42
ret
