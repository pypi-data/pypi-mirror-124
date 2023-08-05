from zcalc.lib import ops

@ops()
def units():
    return [
        ('yotta', lambda z: '1e24'),
        ('zetta', lambda z: '1e21'),
        ('exa',   lambda z: '1e18'),
        ('peta',  lambda z: '1e15'),
        ('tera',  lambda z: '1e12'),
        ('giga',  lambda z: '1e9'),
        ('mega',  lambda z: '1e6'),
        ('kilo',  lambda z: '1e3'),
        ('hecto', lambda z: '1e2'),
        ('deca',  lambda z: '1e1'),
        ('deci',  lambda z: '1e-1'),
        ('centi', lambda z: '1e-2'),
        ('milli', lambda z: '1e-3'),
        ('micro', lambda z: '1e-6'),
        ('nano',  lambda z: '1e-9'),
        ('pico',  lambda z: '1e-12'),
        ('femto', lambda z: '1e-15'),
        ('atto',  lambda z: '1e-18'),
        ('zepto', lambda z: '1e-21'),
        ('yocto', lambda z: '1e-24'),
    ]
