import re
from pathlib import Path
import pytest

from zcalc.env import Env

doc_globs = [
    'doc/stdlib/*.md',
    'tests/stdlib/*.md',
    'README.md',
]

def backquoted(s):
    s = s.strip()
    if s.startswith('``') and s.endswith('``'):
        return s[2:-2]
    if s.startswith('`') and s.endswith('`'):
        return s[1:-1]
    return s

def build_markdown_test(base_name, f):
    module = ''
    tests = []
    name = None
    table = []
    in_table = False
    for line in f:
        if line.startswith('# '):
            module = line[2:].strip()
        if line.startswith('#'):
            name = base_name + ': ' + ' '.join(line.split()[1:])
        if line.startswith('| Input'):
            in_table = True
            continue
        if in_table and line.startswith('|-'):
            continue
        if in_table and line.startswith('| '):
            cells = line.split('|')
            assert len(cells) == 3
            table.append((backquoted(cells[1]), backquoted(cells[2])))
        else:
            in_table = False
            if len(table) > 0:
                tests.append((module, name, table))
                table = []
    if len(table) > 0:
        tests.append((module, name, table))
    return tests

def build_markdown_tests():
    base_dir = Path(__file__).resolve().parents[1]
    tests = []
    for doc_glob in doc_globs:
        doc_files = list(base_dir.glob(doc_glob))
        for doc_file in doc_files:
            with doc_file.open() as f:
                tests.extend(build_markdown_test(doc_file.name, f))
    return tests

@pytest.mark.parametrize('module,op,table', build_markdown_tests())
def test_markdown(module, op, table):
    z = Env()
    z.use(module)
    print(f'| {"line":15} | {"actual":18} | {"expected"}')
    for (line, expected) in table:
        z.do(line)
        actual = ' ; '.join(z.stack)
        print(f'| {line:15} | {actual:18} | {expected}')
        assert actual == expected
