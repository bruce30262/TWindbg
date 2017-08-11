import pykd
import sys
import context
import color
import traceback

from utils import *

class CmdExecError(Exception):
    def __init__(self, errmsg):
        self.errmsg = errmsg

def ctx(args):
    """ctx: print the current context"""
    context.context_handler.print_context()

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
