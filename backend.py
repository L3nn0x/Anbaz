import json
import sys

data = sys.stdin.read()

ir = json.loads(data)

for f in ir["functions"]:
    print(f"global {f['name']}")

print("global start")
print()
print("section .text")
print()
print("start:")
print("call main")
print()

for f in ir["functions"]:
    print(f"{f['name']}:")
    for i in f['instrs']:
        if i['op'] == 'ret':
            print("mov rax, 0x02000001")
            print("mov rdi, 0x0") # exit code
            print("syscall")
