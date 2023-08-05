import pytest

from zcalc.env import Env
from zcalc.stdlib import math

@pytest.mark.parametrize('line,expected', [
    ('`double 2 *; 1; 2; 3; [each double', ['2', '4', '6']),
    ('42; `answer; clear; =answer', ['42']),
    ('3; 4; `other; 1; 2; =other', ['1', '2', '3', '4']),

    (', 1 2 3 4 ; rev',     ['4', '3', '2', '1']),
    (', 1 2 3 4 ; down',    ['4', '1', '2', '3']),
    (', 1 2 3 4 ; up',      ['2', '3', '4', '1']),
    (', 3 1 4 2 ; sort',    ['1', '2', '3', '4']),

    (', 1 2 ; swap',    ['2', '1']),
    (', 1 2 ; clear',   []),
    (', 1 2 ; c',       []),
])
def test_builtin(line, expected):
    z = Env(prelude=False)
    z.use('math')
    z.do(line)
    assert z.stack == expected

def test_builtin_history():
    z = Env(prelude=False)
    z.use('math')
    z.do('`double 2 *')
    z.do('1')
    z.do('2')
    z.do('3')
    z.do('[each double')
    z.do('[each double')
    z.do('undo')
    assert z.stack == ['2', '4', '6']
    z.do('undo')
    assert z.stack == ['1', '2', '3']
    z.do('undo')
    assert z.stack == ['1', '2']
