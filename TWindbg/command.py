import pykd
import sys
import context
import color
import traceback

from utils import *
from functools import wraps

all_commands = [
    'TWindbg',
    'telescope',
    'ctx'
]

class CmdExecError(Exception):
    def __init__(self, errmsg):
        self.errmsg = errmsg

def wrap_usage(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if len(args[0]) == 1 and args[0][0] == "help":
            print_usage(func.__doc__)
            return
        func(*args, **kwargs)
    return wrap

def print_all_usage():
    global all_commands
    for cmd in all_commands:
        cmd_info = globals()[cmd].__doc__.split("\n")[0].split(":")[1]
        pykd.dprintln("{:15s}{}".format(cmd, cmd_info))

@wrap_usage
def TWindbg(args):
    """TWindbg: List all the command in TWindbg """
    if len(args) != 0:
        raise CmdExecError("Invalid argument number")
    banner = color.yellow("TWindbg: PEDA-like debugger UI for WinDbg\n")
    banner += color.gray("For latest update, check the project page: ")
    banner += color.white("https://github.com/bruce30262/TWindbg\n")
    banner += color.orange("Use \"[cmd] help\" for further command usage\n")
    pykd.dprintln(banner, dml=True)
    print_all_usage()

@wrap_usage
def ctx(args):
    """ctx: Print the current context"""
    context.context_handler.print_context()

@wrap_usage
def telescope(args):
    """telescope: Display memory content at an address with smart dereferences
    Usage: telescope/tel [addr] [line to display, default=8, maximum=100] 
    """
    # check argument number
    if not arg_num_in_range(args, 1, 2):
        raise CmdExecError("Invalid argument number")
    # get start address and line number
    start_addr = to_addr(args[0])
    line_num = 8 if len(args) == 1 else to_int(args[1])
    # check valid address
    is_addr, errmsg = check_valid_addr(args[0])
    if not is_addr:
        raise CmdExecError(errmsg)
    # check valid line number
    if not check_in_range(line_num, 1, 100):
        raise CmdExecError("Invalid line number: {}, should be 1 ~ 100".format(args[1]))
    
    context.context_handler.print_nline_ptrs(start_addr, line_num)
