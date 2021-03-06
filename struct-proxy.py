
import time

N = 100000000

class Fish(object):
    def __init__(self, weight, color):
        self.weight = weight
        self.color  = color

class Proxy(object):
    def __init__(self, inner, refs, sets):
        object.__setattr__(self, "inner", inner)
        object.__setattr__(self, "refs", refs)
        object.__setattr__(self, "sets", sets)

    def __getattribute__(self, name):
        check = object.__getattribute__(self, "refs").get(name, None)
        inner = object.__getattribute__(self, "inner")
        val   = getattr(inner, name)
        if check is None:
            return val
        return check(inner, val)

    def __setattr__(self, name, val):
        inner = object.__getattribute__(self, "inner")
        check = object.__getattribute__(self, "sets").get(name, None)
        if check is None:
            return setattr(inner, name, val)
        new_val = check(inner, val)
        return setattr(inner, name, new_val)

def loop(f):
    start = time.clock() * 1000
    for i in xrange(N):
        f.weight
    delta = time.clock() * 1000 - start

    print "RESULT-cpu: %s\nRESULT-total: %s" % (delta, delta)

fish = Proxy(Fish(1, "blue"), refs={"weight": lambda f, v: v}, sets={"weight": lambda f, v: v})
print "proxy"
loop(fish)

