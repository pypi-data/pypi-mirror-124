import decimal
import operator
from zcalc.lib import CalcError, op, reduce

round_rules_parse = {
    'ceiling': decimal.ROUND_CEILING,
    'down': decimal.ROUND_DOWN,
    'floor': decimal.ROUND_FLOOR,
    'half-down': decimal.ROUND_HALF_DOWN,
    'half-even': decimal.ROUND_HALF_EVEN,
    'half-up': decimal.ROUND_HALF_UP,
    'up': decimal.ROUND_UP,
    '05up': decimal.ROUND_05UP,
}

round_rules_format = {v: k for k, v in round_rules_parse.items() }

@op(aliases=['+', 'a'])
def add(z):
    z.op2(operator.add, z.pop_number)

@op(aliases=['/', 'd'])
def div(z):
    try:
        z.op2(operator.truediv, z.pop_number)
    except decimal.DivisionByZero:
        raise CalcError('division by zero')

@op()
def frac(z):
    def fn(d):
        (num, denom) = d.as_integer_ratio()
        return f'{num}/{denom}'
    z.op1(fn, z.pop_decimal)

@op(name='int')
def int_(z):
    z.op1(int, z.pop_number)

@op(aliases=['%'])
def mod(z):
    z.op2(operator.mod, z.pop_number)

@op(aliases=['*', 'm'])
def mul(z):
    z.op2(operator.mul, z.pop_number)

@op()
def neg(z):
    z.op1(operator.neg, z.pop_number)

@op()
def norm(z):
    z.op1(lambda d: d.normalize(), z.pop_decimal)

@op()
def places(z):
    places = z.pop_int()
    if places < 0:
        raise CalcError('invalid number of places')
    z.places = places

@op(name='places-info')
def places_info(z):
    if z.places:
        z.info = str(z.places)
    else:
        z.info = 'auto'

@op()
def prec(z):
    places = z.pop_int()
    decimal.getcontext().prec = places

@op(name='prec-info')
def prec_info(z):
    z.info = str(decimal.getcontext().prec)

@op(aliases=['r'])
def round(z):
    digits = z.pop_int()
    number = z.pop_decimal()
    amount = '.' + ('0' * (digits - 1)) + '1'
    z.push(number.quantize(decimal.Decimal(amount)))

@op(name='round-rule')
def round_rule(z):
    str_rule = z.pop()
    try:
        rule = round_rules_parse[str_rule]
        decimal.getcontext().rounding = rule
    except KeyError:
        raise CalcError(f'invalid round rule: {str_rule}')

@op(name='round-rule-info')
def round_rule_info(z):
    z.info = round_rules_format[decimal.getcontext().rounding]

@op(aliases=['-', 's'])
def sub(z):
    z.op2(operator.sub, z.pop_number)

@op()
def sum(z):
    reduce(z, ['add'])

