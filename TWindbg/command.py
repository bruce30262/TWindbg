import pykd
import context

commands = [
    'telescope',
    'context'
]

def set_alias(a, v):
    pykd.dbgCommand("as {} {}".format(a, v))

def set_aliases():
    global commands
    for cmd in commands:
        set_alias(cmd, "!py winext\TWindbg\TWindbg.py {}".format(cmd))

def context():
    context.context_handler.print_context()
   
    