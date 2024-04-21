class AArch64:
    def allocate_registers(ir):
        for f in ir['functions']:
            for i in f['instrs']:
                if 'dest' in i:
                    i['dest'] = 'x0'
                if 'args' in i and i['args']:
                    for n in range(len(i['args'])):
                        i['args'][n] = 'x0'
        return ir

    def lower_instr(instr):
        if instr['op'] == 'const':
            print(f"mov {instr['dest']}, #{instr['value']}") # TODO handle big literals
        elif instr['op'] == 'ret':
            if instr['args'] and instr['args'][0] != "x0": # ABI is return value in x0
                print(f"mov x0, {instr['args']}")
            print(f"ret")

    def lower_function(f):
        print(f".globl {f['name']}")
        print(f"{f['name']}:")
        for instr in f['instrs']:
            AArch64.lower_instr(instr)

    def lower_program(ir):
        print(".section __TEXT,__text")
        print(".p2align 2")
        print(".globl _main")
        print()
        print("_main:")
        print("bl main")
        print("ldr x16, =0x2000001")
        print("svc #0x80")
        print()
        for f in ir["functions"]:
            AArch64.lower_function(f)
