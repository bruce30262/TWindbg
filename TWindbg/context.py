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
            if reg_name == self.sp_name:
                self.sp = reg_data
            if reg_name == self.pc_name:
                self.pc = reg_data
    
class ContextHandler(pykd.eventHandler):
    def __init__(self, context):
        pykd.eventHandler.__init__(self)
        self.context = context
        
    def onExecutionStatusChange(self, status):
        if status == pykd.executionStatus.Break: # step, trace, ...
            self.context.update_regs()
            self.print_context()

    def print_context(self):
        #pykd.dbgCommand('.cls')
        if self.context.pc == None: # if no context, update it
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
            reg_str = '{:3}: {:#x}'.format(reg_name.upper(), reg_data)
            reg_color = None
            if self.context.is_changed[reg_name]:
                reg_color = color.red 
            else:
                reg_color = color.lime
            
            pykd.dprintln(reg_color(reg_str), dml=True)

    def print_seg_regs(self):
        first_print = True
        for reg_name in self.context.seg_regs_name:
            reg_data = self.context.regs[reg_name]
            reg_str = '{:2}={:#x}'.format(reg_name.upper(), reg_data)
            reg_color = None
            if self.context.is_changed[reg_name]:
                reg_color = color.red 
            else:
                reg_color = color.green
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

    def print_code(self):
        pc = self.context.pc
        for offset in xrange(-3, 6): # pc-3 ~ pc+5
            addr = pykd.disasm().findOffset(offset)
            inst = pykd.disasm().disasm(addr)
            start = len(inst.split(" ")[0])
            inst = inst[start::] # strip the address info
            code_str = "{:#x}: {}".format(addr, inst)
            if addr == pc: # current pc, highlight
                pykd.dprintln(color.lime_highlight(code_str), dml=True)
            else:
                pykd.dprintln(code_str)
    
    def print_stack(self):
        sp = self.context.sp
        for i in xrange(8):
            cur_sp = sp + i * PTRSIZE
            pykd.dprint("{:02d}:{:04x}| ".format(i, i * PTRSIZE))
            ptr_values, is_cylic = self.smart_dereference(cur_sp)
            stack_str = '{:#x}'.format(cur_sp)
            for val in ptr_values:
                stack_str += " --> {:#x}".format(val)

            if is_cylic:   
                stack_str += color.dark_red(" ( cylic dereference )")
            
            pykd.dprintln(stack_str, dml=True)
            
    def smart_dereference(self, addr):
        ptr_values, is_cyclic = [], False
        for _ in xrange(MAX_DEREF):
            try:
                val = pykd.loadPtrs(addr, 1)[0] & PTRMASK
                ptr_values.append(val)
                if val in ptr_values[:-1:] or val == addr: # cyclic dereference
                    is_cyclic = True
                    break
                else:
                    addr = val
            except pykd.MemoryException: # no more dereference
                break

        return ptr_values, is_cyclic

