import operator
from zcalc.lib import op

@op(name='and', aliases=['&'])
def and_(z):
    return z.op2(operator.and_, z.pop_int)

@op(name='bin')
def bin_(z):
    return z.op1(bin, z.pop_int)

@op()
def dec(z):
    return z.op1(int, z.pop_int)

@op(name='hex')
def hex_(z):
    return z.op1(hex, z.pop_int)

@op(name='oct')
def oct_(z):
    return z.op1(oct, z.pop_int)

@op(name='or', aliases=['|'])
def or_(z):
    return z.op2(operator.or_, z.pop_int)

@op(name='shift-left', aliases=['shl', '<<'])
def shift_left(z):
    return z.op2(operator.lshift, z.pop_int)

@op(name='shift-right', aliases=['shr', '>>'])
def shift_right(z):
    return z.op2(operator.rshift, z.pop_int)

@op(aliases=['^'])
def xor(z):
    return z.op2(operator.xor, z.pop_int)
