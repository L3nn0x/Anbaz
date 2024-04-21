class GenerateIr:
    def __init__(self):
        self.instrs = []
        self.output = []
        self.current_type = None
        self.current_expr = None
        self.regs = 0

    def visit_type(self, t):
        self.current_type = None if t.t == "void" else t.t

    def visit_const(self, c):
        self.current_expr = f"r{self.regs}"
        self.instrs.append({"op": "const", "type": self.current_type, "dest": self.current_expr, "value": c.value})
        self.current_type = None
        self.regs += 1

    def visit_return(self, r):
        self.instrs.append({"op":"ret","args":[] if not self.current_expr else [self.current_expr]})
        self.current_expr = None

    def visit_function(self, f):
        self.output.append({
            "name": f.name,
            "type": self.current_type,
            "args": f.args,
            "instrs": self.instrs
            })
        self.instrs = []
        self.current_type = None

    def generate(self):
        return {
                "functions": self.output
                }
