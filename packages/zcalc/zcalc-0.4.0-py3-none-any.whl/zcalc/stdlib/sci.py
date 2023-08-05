import math
import operator
from zcalc.lib import op, ops

@ops()
def const():
    return [
        ('e',   lambda z: math.e),
        ('pi',  lambda z: math.pi),
    ]

@op(name='abs')
def abs_(z):
    z.op1(abs, z.pop_number)

@op()
def exp(z):
    z.op1(lambda d: d.exp(), z.pop_decimal)

@op()
def ln(z):
    z.op1(lambda d: d.ln(), z.pop_decimal)

@op()
def log10(z):
    z.op1(lambda d: d.log10(), z.pop_decimal)

@op(aliases=['**'])
def pow(z):
    z.op2(operator.pow, z.pop_number)

@op()
def sqrt(z):
    z.op1(lambda d: d.sqrt(), z.pop_decimal)
