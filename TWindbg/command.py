import pykd
import sys
import context
import color
import traceback
import ctypes

from utils import *

all_commands = [
    'telescope',
    'ctx'
]

def set_alias(a, v):
    pykd.dbgCommand("as {} {}".format(a, v))

def wrap_commands():
    global all_commands
    for cmd in all_commands:
        set_alias(cmd, "!py -g winext\TWindbg\command.py {}".format(cmd))
    set_alias("tel", "!py -g winext\TWindbg\command.py telescope")

def init_command_obj():
    global command_obj
    if 'command_obj' not in globals():
        command_obj = Command()
        
def print_ptrs(addr):
    ptr_str = ""
    ptr_values, is_cylic = context.context_handler.smart_dereference(addr)
    for val in ptr_values:
        ptr_str += " --> {:#x}".format(val)
    if is_cylic:   
        ptr_str += color.dark_red(" ( cylic dereference )")
    pykd.dprintln("{:#x}:{}".format(addr, ptr_str), dml=True)
    
def print_nline_ptrs(start_addr, line_num):
    start_addr = ctypes.c_long(start_addr).value
    for addr in xrange(start_addr, start_addr + line_num * context.PTRSIZE, context.PTRSIZE):
        addr = ctypes.c_ulong(addr).value
        if not pykd.isValid(addr):
            raise CmdExecError("Invalid memory address: {:#x}".format(addr))
        else:
            print_ptrs(addr)  
           
class CmdExecError(Exception):
    def __init__(self, errmsg):
        self.errmsg = errmsg

class Command():
    def ctx(self, *args):
        """ctx: print the current context"""
        context.context_handler.print_context()

    def telescope(self, args):
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
        
        print_nline_ptrs(start_addr, line_num)

class CommandHandler():
    def __init__(self, func):
        self.func = func

    def invoke(self, args):
        try:
            self.func(args)
        except CmdExecError as e:
            print_err(e.errmsg)
            print_usage(self.func.__doc__)
        except Exception:
            traceback.print_exc()
                

init_command_obj()
if __name__ == "__main__":            
    if len(sys.argv) >= 2: # user input TWindbg command
        cmd = sys.argv[1]
        if hasattr(command_obj, cmd): # if the command mudule has the corresponded method, call it
            func = getattr(command_obj, cmd)
            CommandHandler(func).invoke(sys.argv[2::])
        else:
            print_err("Command: {} not found in TWindbg.".format(cmd))

