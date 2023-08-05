import pytest

from zcalc import env
from zcalc.env import Env
from zcalc.lib import CalcError

@pytest.mark.parametrize('line,expected', [
    [
        'fn one two three',
        ['fn', 'one', 'two', 'three']
    ],
    [
        '  fn  one   two  three   ',
        ['fn', 'one', 'two', 'three']
    ],
    [
        'fn "one and one" two three',
        ['fn', 'one and one', 'two', 'three']
    ],
    [
        'fn "one and one',
        ['fn', 'one and one']
    ],
])
def test_parse_args(line, expected):
    assert env.parse_args(line) == expected
