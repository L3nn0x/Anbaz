import json
import sys
import platform

from .passes import run_passes

from .aarch64 import AArch64

data = sys.stdin.read()

ir = json.loads(data)

ir = run_passes(ir)

p = None
if platform.system() == "Darwin" and platform.processor() == "arm":
    p = AArch64
if p is None:
    print("Platform not supported")
    exit(1)

ir = p.allocate_registers(ir)
p.lower_program(ir)
