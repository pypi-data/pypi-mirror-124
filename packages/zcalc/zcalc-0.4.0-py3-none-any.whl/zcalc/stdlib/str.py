from zcalc.lib import op

@op(name='len')
def len_(z):
    z.op1(len)

@op()
def replace(z):
    new = z.pop()
    old = z.pop()
    s = z.pop()
    z.push(s.replace(old, new))
