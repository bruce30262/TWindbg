# -*- coding: utf-8 -*-

import pykd
import color
import sys
import traceback

from utils import *

ARCH = None
PTRMASK = None
PTRSIZE = None
MAX_DEREF = 20

def init_arch():
    global ARCH, PTRMASK, PTRSIZE
    cpu_mode = pykd.getCPUMode() 
    if cpu_mode == pykd.CPUType.I386:
        ARCH = 'x86'
        PTRMASK = 0xffffffff
        PTRSIZE = 4
    elif cpu_mode == pykd.CPUType.AMD64:
        ARCH = 'x64'
        PTRMASK = 0xffffffffffffffff
        PTRSIZE = 8
    else:
        print_err("CPU mode: {} not supported.".format(cpu_mode))
        sys.exit(-1)

def init_context_handler():
    global context_handler
    if 'context_handler' not in globals():
        context_handler = ContextHandler(Context())

class Context():
    def __init__(self):
        self.regs_name = []
        self.seg_regs_name = ['cs', 'ds', 'es', 'fs', 'gs', 'ss']
        self.regs = {}
        self.eflags_tbl = {
            0: "carry",
            2: "parity",
            4: "auxiliary",
            6: "zero",
            7: "sign",
            8: "trap",
            9: "interrupt",
            10: "direction",
            11: "overflow",
            14: "nested",
            16: "resume",
            17: "virtualx86"
        }
        self.is_changed = {}
        self.sp_name = ""
        self.sp = None
        self.pc_name = ""
        self.pc = None
                
        self.init_regs_name()
        self.init_regs()
        
    def init_regs_name(self):
        if ARCH == 'x86':
            self.regs_name = ['eax', 'ebx', 'ecx', 'edx', 'edi', 'esi', 'ebp', 'esp', 'eip']
            self.sp_name = 'esp'
            self.pc_name = 'eip'
        else:
            self.regs_name = ['rax', 'rbx', 'rcx', 'rdx', 'rdi', 'rsi', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15', 'rbp', 'rsp', 'rip']
            self.sp_name = 'rsp'
            self.pc_name = 'rip'
    
    def init_regs(self):
        for reg_name in self.regs_name + self.seg_regs_name:
            self.regs[reg_name] = None
            self.is_changed[reg_name] = False
            
    def update_regs(self):
        for reg_name in self.regs_name + self.seg_regs_name:
            reg_data = pykd.reg(reg_name)
            if reg_data != self.regs[reg_name]: # is changed
                self.is_changed[reg_name] = True
            else:
                self.is_changed[reg_name] = False
            
            self.regs[reg_name] = reg_data
        # update sp & pc
        self.sp = self.regs[self.sp_name]
        self.pc = self.regs[self.pc_name]

class ContextHandler(pykd.eventHandler):
    def __init__(self, context):
        pykd.eventHandler.__init__(self)
        self.context = context
        
    def onExecutionStatusChange(self, status):
        if status == pykd.executionStatus.Break: # step, trace, ...
            self.print_context()

    def print_context(self):
        self.context.update_regs()
        pykd.dprintln(color.yellow("[------ Register --------------------------------------------------------------------------------------------]"), dml=True)
        self.print_regs()
        pykd.dprintln(color.yellow("[------ Code ------------------------------------------------------------------------------------------------]"), dml=True)
        self.print_code()
        pykd.dprintln(color.yellow("[------ Stack -----------------------------------------------------------------------------------------------]"), dml=True)
        self.print_stack()
        pykd.dprintln(color.yellow("[------------------------------------------------------------------------------------------------------------]"), dml=True)
        
    def print_regs(self):
        self.print_general_regs()
        self.print_seg_regs()
        self.print_eflags()
        
    def print_general_regs(self):
        for reg_name in self.context.regs_name:
            reg_data = self.context.regs[reg_name]
            reg_str = '{:3}: '.format(reg_name.upper())
            reg_color = self.set_reg_color(reg_name, color_changed=color.red, color_unchanged=color.lime)
            pykd.dprint(reg_color(reg_str), dml=True)

            # if reg_data is a valid virtual address and is able to be dereferenced, print it with print_ptrs(), or else just print it directly
            if pykd.isValid(reg_data) and ( deref_ptr(reg_data) != None ):
                self.print_ptrs(reg_data)
            else:
                pykd.dprintln("{:#x}".format(reg_data))

    def print_seg_regs(self):
        first_print = True
        for reg_name in self.context.seg_regs_name:
            reg_data = self.context.regs[reg_name]
            reg_str = '{:2}={:#x}'.format(reg_name.upper(), reg_data)
            reg_color = self.set_reg_color(reg_name, color_changed=color.red, color_unchanged=color.green)

            if first_print:
                pykd.dprint(reg_color(reg_str), dml=True)
                first_print = False
            else:
                pykd.dprint(" | " + reg_color(reg_str), dml=True)
        pykd.dprintln("")
    
    def print_eflags(self):
        eflags = pykd.reg('efl')
        eflags_str = color.green("EFLAGS: {:#x}".format(eflags))
        eflags_str += " ["
        for bit, flag_name in self.context.eflags_tbl.items():
            is_set = eflags & (1<<bit)
            eflags_str += " "
            if is_set:
                eflags_str += color.dark_red(flag_name)
            else:
                eflags_str += color.green(flag_name)
        eflags_str += " ]"
        pykd.dprintln(eflags_str, dml=True)

    def set_reg_color(self, reg_name, color_changed, color_unchanged):
        if self.context.is_changed[reg_name]:
            return color_changed
        else:
            return color_unchanged

    def print_code(self):
        pc = self.context.pc
        for offset in range(-3, 6): # pc-3 ~ pc+5
            addr = pykd.disasm().findOffset(offset)
            op_str, asm_str = disasm(addr)
            code_str = "{:#x}: {:20s}{}".format(addr, op_str, asm_str)
            if addr == pc: # current pc, highlight
                pykd.dprintln(color.lime_highlight(code_str), dml=True)
            else:
                pykd.dprintln(code_str)
    
    def print_stack(self):
        self.print_nline_ptrs(self.context.sp, 8)
        
    def print_nline_ptrs(self, start_addr, line_num):
        for i in range(line_num):
            pykd.dprint("{:02d}:{:04x}| ".format(i, i * PTRSIZE))
            addr = start_addr + i * PTRSIZE
            if not pykd.isValid(addr):
                print_err("Invalid memory address: {:#x}".format(addr))
                break
            else:
                self.print_ptrs(addr)  

    def print_ptrs(self, addr):
        ptrs_str = ""
        ptr_values, is_cyclic = self.smart_dereference(addr)
        # print all ptrs except last two
        for ptr in ptr_values[:-2:]:
            ptrs_str += "{:#x} --> ".format(ptr)
        # handle last two's format
        last_ptr, last_val = ptr_values[-2], ptr_values[-1]
        if is_cyclic:
            ptrs_str += "{:#x} --> {:#x}".format(last_ptr, last_val) + color.dark_red(" ( cyclic dereference )")
        else:
            ptrs_str += self.enhance_type(last_ptr, last_val)
        pykd.dprintln(ptrs_str, dml=True)

    def enhance_type(self, ptr, val):
        ret_str = ""
        if is_executable(ptr): # code page
            symbol = pykd.findSymbol(ptr) + ":"
            asm_str = disasm(ptr)[1]
            ret_str = "{:#x}".format(ptr)
            ret_str += color.gray(" ({:45s}{})".format(symbol, asm_str))
        else:
            ret_str = "{:#x} --> {:#x}".format(ptr, val)
            val_str = get_string(ptr)
            if val_str: # val is probably a string
                ret_str += color.white(" (\"{}\")".format(val_str))
        return ret_str

    def smart_dereference(self, ptr):
        ptr_values, is_cyclic = [ptr], False
        for _ in range(MAX_DEREF):
            val = deref_ptr(ptr)
            if val == None: # no more dereference
                return ptr_values, is_cyclic

            ptr_values.append(val)
            # Check if the newly pushed value is in ptr_values[:-1:]
            # If it does means there's a cyclic dereference in the current pointer chain
            # Otherwise the newly pushed value will become the new pointer to be dereferenced next
            if val in ptr_values[:-1:]: 
                is_cyclic = True
                return ptr_values, is_cyclic
            else:
                ptr = val

