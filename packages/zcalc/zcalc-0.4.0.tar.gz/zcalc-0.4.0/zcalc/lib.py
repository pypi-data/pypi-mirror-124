class CalcError(Exception):
    pass

def op(name=None, aliases=None):
    def op_impl(fn):
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapper.zcalc_name = name if name is not None else fn.__name__
        wrapper.zcalc_aliases = aliases if aliases is not None else []
        return wrapper
    return op_impl

def mod():
    def mod_impl(fn):
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapper.zcalc_mod = True
        return wrapper
    return mod_impl


def ops():
    def vals_impl(fn):
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapper.zcalc_ops = True
        return wrapper
    return vals_impl

def reduce(z, ops):
    n = len(z.stack)
    while n > 1:
        z.stack.extend(ops)
        z.eval()
        if len(z.stack) >= n:
            raise CalcError('operation is not reducing')
        n = len(z.stack)
