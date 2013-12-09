from cli import CLI
import sys

def startup():
    if len(sys.argv) > 1:
        CLI().onecmd(' '.join(sys.argv[1:]))
    else:
        CLI().onecmd('run')