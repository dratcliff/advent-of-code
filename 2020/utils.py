from timeit import default_timer as timer

def timed(f):
    def t(*args, **kwargs):
        start = timer()
        result = f(*args, **kwargs)
        end = timer()
        print(f.__name__, "took", (end-start)*1000, "ms")
        return result
    return t