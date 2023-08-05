import pytest

from zcalc.env import Env

@pytest.mark.parametrize('line', [
    '12345 ; len ; 5',
    'ab.cd ; [replace . "" ; abcd',
])
def test_sci(line):
    z = Env(prelude=False)
    z.use('str')
    z.do(line)
    assert z.pop() == z.pop()


