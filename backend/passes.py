passes = []

def run_passes(ir):
    global passes
    for p in passes:
        ir = p(ir)
    return ir
