import pytest

from zcalc.env import Env

@pytest.mark.parametrize('line', [
    '-12.34; abs; 12.34',
    '1; exp; 2.718281828459045',
    '2; ln; 0.6931471805599453',
    '2; log10; 0.3010299956639812',
    '6; 2; pow; 36',
    '256; sqrt; 16',
])
def test_sci(line):
    z = Env(prelude=False)
    z.use('sci')
    z.do(line)
    assert z.pop() == z.pop()


