from itertools import tee

class Peekable:
    def __init__(self, it):
        self.it = it

    def peek(self):
        current, backup = tee(self.it)
        self.it = backup
        try:
            return next(current)
        except StopIteration:
            return None
    
    def __next__(self):
        try:
            return next(self.it)
        except StopIteration:
            return None

