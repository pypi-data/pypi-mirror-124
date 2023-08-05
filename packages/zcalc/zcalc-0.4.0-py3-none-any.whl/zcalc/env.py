import re
import unicodedata

from decimal import Decimal, InvalidOperation, getcontext
from importlib import import_module
from pygtrie import Trie

from .lib import CalcError

class Env:

    def __init__(self, prelude=True):
        self.stack = []
        self.history = [[]]
        self.max_history = 25
        self.ops = {}
        self.macros = {}
        self.info = None
        self.error = None
        self.output = None
        self.trie = Trie()
        self.places = 0
        self.use('builtin')
        if prelude:
            self.use('bit')
            self.use('math')
            self.use('sci')
            self.use('str')
        getcontext().prec = 16

    def eval(self):
        self.info = None
        self.error = None
        if len(self.stack) == 0:
            return
        entry = self.stack.pop()
        try:
            if not self._eval_op(entry):
                #self.stack.append(entry.strip())
                self.push(entry.strip())
        except CalcError as e:
            self.error = e

    def do(self, line):
        self.info = None
        self.error = None
        # When entering a blank line, clear output if that is being
        # displayed. Otherwise, pop a value of the stack if able.
        if len(line) == 0:
            if self.output or self.info:
                self.output = None
                self.input = None
                return
            if len(self.stack) > 0:
                self.stack.pop()
        else:
            entries = parse_entries(line)
            for entry in entries:
                self._eval_entry(entry)
                if self.error:
                    break
        if len(self.history) == 0 or self.stack != self.history[-1]:
            self.history.append(self.stack.copy())
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def _eval_entry(self, entry):
        try:
            first = entry[0] if len(entry) > 0 else ''
            if first == ',':
                self._eval_items(entry[1:])
            elif first == '[':
                self._eval_prefix(entry[1:])
            elif first == '`':
                self._define_macro(entry[1:])
            elif first == '=':
                self._invoke_macro(entry[1:])
            elif first == '"' or first == "'":
                self.stack.append(entry[1:])
            else:
                self.stack.append(entry)
                self.eval()
        except CalcError as e:
            self.error = e

    def _define_macro(self, line):
        args = parse_args(line.strip())
        if len(args) == 0:
            raise CalcError('macro name missing')
        name = args[0]
        if len(args) == 1:
            self.macros[name] = self.stack
            self.stack = []
        else:
            self.macros[name] = args[1:]

    def _invoke_macro(self, line):
        args = parse_args(line.strip())
        if len(args) > 1:
            raise CalcError('too many arguments')
        name = args[0] if len(args) > 0 else '='
        macro = self.get_macro(name)
        for item in macro:
            self.stack.append(item)
            self.eval()

    def _eval_prefix(self, line):
        args = parse_args(line)
        self.stack += args[1:]
        self._eval_entry(args[0])

    def _eval_items(self, line):
        args = parse_args(line)
        for arg in args:
            self.push(arg)
            self.eval()
            if self.error:
                break

    def _eval_op(self, name):
        name = name.strip()
        op = self.ops.get(name)
        if not op:
            return False
        result = op(self)
        if result is not None:
            self.push(result)
        return True

    def use(self, name):
        try:
            mod = import_module(f'zcalc.stdlib.{name}')
        except ModuleNotFoundError:
            try:
                mod = import_module(name)
            except ModuleNotFoundError:
                raise CalcError(f'no such module: {name}')
        for export in dir(mod):
            obj = getattr(mod, export)
            if hasattr(obj, 'zcalc_mod'):
                obj(self)
                continue
            if hasattr(obj, 'zcalc_ops'):
                vals = obj()
                for (name, fn) in vals:
                    self.ops[name] = fn
                    self.trie[name] = name + ' '
            if not hasattr(obj, 'zcalc_name'):
                continue
            self.ops[obj.zcalc_name] = obj
            self.trie[obj.zcalc_name] = obj.zcalc_name + ' '
            for alias in obj.zcalc_aliases:
                self.ops[alias] = obj
                self.trie[alias] = alias + ' '

    def pop(self):
        try:
            return self.stack.pop()
        except IndexError:
            raise CalcError('stack empty')

    def pop_float(self):
        return parse_float(self.pop())

    def pop_decimal(self):
        return parse_decimal(self.pop())

    def pop_int(self):
        return parse_int(self.pop())

    def pop_number(self):
        n = self.pop()
        parsers = [
            parse_decimal,
            parse_int,
        ]
        for parse in parsers:
            try:
                return parse(n)
            except CalcError:
                pass
        raise CalcError(f'not a number: ${n}')

    def push(self, v):
        s = str(v)
        if isinstance(v, Decimal):
            if self.places:
                spec = '{:.' + str(self.places) + 'f}'
                s = spec.format(v)
            else:
                if v.is_zero():
                    s = '0'
                # Remove any trailing zeros after the decimal point
                if '.' in s:
                    s = s.rstrip('0').rstrip('.')
            # Replace with a more modern looking exponent
            s = s.replace('E+', 'e')
            s = s.replace('E-', 'e-')
        if isinstance(v, str):
            if self.places:
                try:
                    d = Decimal(v)
                    spec = '{:.' + str(self.places) + 'f}'
                    s = spec.format(d)
                except InvalidOperation:
                    pass
        self.stack.append(s)

    def binary_op(self, pop, push, op):
        b = pop()
        a = pop()
        return push(op(a, b))

    def unary_op(self, pop, push, op):
        a = pop()
        return push(op(a))

    def op2(self, op, pop=None, push=None):
        pop = pop if pop is not None else self.pop
        push = push if push is not None else self.push
        b = pop()
        a = pop()
        return push(op(a, b))

    def op1(self, op, pop=None, push=None):
        pop = pop if pop is not None else self.pop
        push = push if push is not None else self.push
        a = pop()
        return push(op(a))

    def get_macro(self, name=None):
        if not name:
            name = self.pop()
        try:
            return self.macros[name]
        except KeyError:
            raise CalcError(f'no such macro: {name}')

    def completer(self, text, index):
        vals = self.trie.values(text)
        return None if index >= len(vals) else vals[index]


def _clean_numeric(dirty):
    clean = []
    for char in dirty:
        if char == ',':
            continue
        if unicodedata.category(char) == 'Sc': # symbol, currency
            continue
        clean.append(char)
    return ''.join(clean)


def parse_int(n):
    try:
        return int(_clean_numeric(n), 0)
    except ValueError:
        raise CalcError(f'not an integer: {n}')


def parse_decimal(n):
    try:
        return Decimal(_clean_numeric(n))
    except ValueError:
        raise CalcError(f'not a decimal: {n}')
    except InvalidOperation:
        raise CalcError(f'not a decimal: {n}')

def parse_float(n):
    try:
        return float(_clean_numeric(n))
    except ValueError:
        raise CalcError(f'not a float: ${n}')


def parse_entries(line):
    entries = []
    entry = []
    for char in line:
        if char.isspace() and len(entry) == 0:
            continue
        if char == ';':
            entries.append(''.join(entry))
            entry = []
            continue
        entry.append(char)
    if len(entry) > 0:
        entries.append(''.join(entry))
    return entries


def parse_args(line):
    args = []
    arg = []
    quote = None
    for char in line:
        # Space outside of quotes marks the end of the current argument
        if not quote and char.isspace() and len(arg) > 0:
            args.append(''.join(arg))
            arg = []
            continue
        # Ignore whitespace if not yet parsing an argument
        if not quote and char.isspace():
            continue
        # Is this the start of a quote?
        if not quote and (char == "'" or char == '"'):
            quote = char
            continue
        # Is this the end of a quote? If so, it is also the end of the
        # current argument
        if quote and char == quote:
            quote = None
            args.append(''.join(arg))
            arg = []
            continue
        # Otherwise, add this character to the current argument
        arg.append(char)
    # When the end of line is reached, finish the current argument
    if len(arg) > 0:
        args.append(''.join(arg))
    return args


