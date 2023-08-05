import os
from argparse import ArgumentParser

from .env import Env

try:
    import readline
except ModuleNotFoundError:
    # For windows
    from pyreadline import Readline
    readline = Readline()

# To enable ANSI codes in Windows
if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

CLEAR_SCREEN    = '\033[2J'
MOVE_TO_BOTTOM  = '\033[200;0H' # go to line 200, column 0
RESET           = '\033[0m'
BOLD            = '\033[1m'
LIGHT_GREEN     = '\033[1;32m'
LIGHT_BLUE      = '\033[1;36m'
BRIGHT_YELLOW   = '\033[1;93m'

prompt = f'{LIGHT_GREEN}zcalc{RESET}> '

def cmd():
    parser = ArgumentParser()
    parser.add_argument('-r', '--raw', action='store_true')
    parser.add_argument('-u', '--use', action='append')
    args = parser.parse_args()

    z = Env()
    readline.parse_and_bind('tab: complete')
    readline.set_completer(z.completer)
    readline.set_completer_delims('')
    if args.use is not None:
        for mod in args.use:
            z.use(mod.strip())

    if not args.raw:
        print(CLEAR_SCREEN)
        print(MOVE_TO_BOTTOM)
    while True:
        try:
            line = input(prompt)
        except EOFError:
            return
        except KeyboardInterrupt:
            return
        z.do(line)
        if not args.raw:
            print(CLEAR_SCREEN)
        if z.output:
            print(z.output)
        else:
            for (i, item) in enumerate(z.stack):
                if i == len(z.stack) - 1:
                    print(f'{BOLD}{item}{RESET}')
                else:
                    print(f'{LIGHT_BLUE}{item}{RESET}')
        if z.error:
            print(f'{BRIGHT_YELLOW}(!) {z.error}{RESET}')
        elif z.info:
            print(f'{LIGHT_BLUE}(?) {z.info}{RESET}')
        else:
            print()

if __name__ == '__main__':
    cmd()
