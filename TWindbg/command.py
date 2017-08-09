import pykd
import sys
import context
import color

from utils import *

commands = [
    'telescope',
    'ctx'
]

def set_alias(a, v):
    pykd.dbgCommand("as {} {}".format(a, v))

def wrap_commands():
    global commands
    for cmd in commands:
        set_alias(cmd, "!py -g winext\TWindbg\command.py {}".format(cmd))
    set_alias("tel", "!py -g winext\TWindbg\command.py telescope")

class CommandHandler():
    def ctx(self, *args):
        """print the current context"""
        context.context_handler.print_context()

    def telescope(self, *args):
        """Display memory content at an address with smart dereferences
        Usage: telescope/tel < addr > < line to display, default=8, maximum=100 >  
        """
        if len(args) == 0 or len(args) > 2:
            print_usage(self.telescope.__doc__)

        line_num = 8
        start_addr = to_int(args[0])
        line_num = to_int(args[1])
        if not line_num or line_num > 100:
            print_err
        for addr in xrange()
        if not addr or not pykd.isValid(addr):
            print_err("{} is not a valid memory address".format(addr))

if len(sys.argv) >= 2: # user input TWindbg command
    cmd = sys.argv[1]
    if cmd in globals(): # if the command mudule has the corresponded method, call it
        globals()[cmd](sys.argv[2::])
    else:
        pykd.dprintln(color.red("Command: {} not found in TWindbg.".format(cmd)), dml=True)
    
