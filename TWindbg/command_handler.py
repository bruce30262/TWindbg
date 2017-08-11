import pykd
import sys
import traceback
import command

from utils import *

all_commands = [
    'telescope',
    'ctx'
]

def set_alias(a, v):
    pykd.dbgCommand("as {} {}".format(a, v))

def wrap_command(cmd, real_cmd):
    set_alias(cmd, "!py -g winext\TWindbg\command_handler.py {}".format(real_cmd))

def wrap_all_commands():
    global all_commands
    for cmd in all_commands:
        wrap_command(cmd, cmd)
    wrap_command("tel", "telescope")

class CommandHandler():
    def __init__(self, func):
        self.func = func

    def invoke(self, args):
        try:
            self.func(args)
        except command.CmdExecError as e:
            print_err(e.errmsg)
            print_usage(self.func.__doc__)
        except Exception:
            traceback.print_exc()
                
if __name__ == "__main__":            
    if len(sys.argv) >= 2: # user input TWindbg command
        cmd = sys.argv[1]
        if hasattr(command, cmd): # if the command mudule has the corresponded method, call it
            func = getattr(command, cmd)
            CommandHandler(func).invoke(sys.argv[2::])
        else:
            print_err("Command: {} not found in TWindbg.".format(cmd))

