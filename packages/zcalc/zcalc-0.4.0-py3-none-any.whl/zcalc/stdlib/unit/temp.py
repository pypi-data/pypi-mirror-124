from zcalc.lib import ops

@ops()
def temp():
    return [
        ('C->F', lambda z: z.do(', 9 5 / * 32 +')),
        ('C->K', lambda z: z.do(', 273.15 +')),
        ('F->C', lambda z: z.do(', 32 - 5 9 / *')),
        ('F->K', lambda z: z.do(', 459.67 + 5 9 / *')),
        ('K->C', lambda z: z.do(', 273.15 -')),
        ('K->F', lambda z: z.do(', 9 5 / * 459.67 -'))
    ]


