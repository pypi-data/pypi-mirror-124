import pytest

from zcalc.env import Env
from zcalc.stdlib import math

@pytest.mark.parametrize('line', [
    '0      ; C->F ; 32',
    '0      ; C->K ; 273.15',
    '32     ; F->C ; 0',
    '32     ; F->K ; 273.15',
    '273.15 ; K->C ; 0',
    '273.15 ; K->F ; 32',
])
def test_bit(line):
    z = Env()
    z.use('unit.temp')
    z.do(line)
    assert z.pop() == z.pop()