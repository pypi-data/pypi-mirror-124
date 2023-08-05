from zcalc.lib import CalcError, op, reduce

@op(aliases=['='])
def apply(z):
    z.stack.append('=')
    z.stack.extend(z.get_stack())
    z.run()

@op(aliases=['c'])
def clear(z):
    z.stack.clear()

@op(aliases=['cp'])
def copy(z):
    a = z.pop()
    z.push(a)
    z.push(a)

@op(aliases=['dn'])
def down(z):
    if len(z.stack) == 0:
        return
    z.stack.insert(0, z.pop())

@op()
def each(z):
    ops = z.get_macro()
    n = len(z.stack)
    for i in range(n):
        z.stack.extend(ops)
        z.eval()
        down(z)

@op(aliases=['rev'])
def reverse(z):
    z.stack.reverse()

@op()
def run(z):
    z.run()

@op()
def sort(z):
    z.stack.sort()

@op(aliases=['sw'])
def swap(z):
    a = z.pop()
    b = z.pop()
    z.push(a)
    z.push(b)

@op(aliases=['u'])
def undo(z):
    if len(z.history) <= 1:
        raise CalcError('history empty')
    z.history.pop()
    z.stack = z.history.pop()

@op()
def up(z):
    if len(z.stack) == 0:
        return
    z.stack.append(z.stack.pop(0))

@op()
def use(z):
    z.use(z.pop())

