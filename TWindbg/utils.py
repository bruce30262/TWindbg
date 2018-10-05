import pykd
import color
import context
import string

def to_int(val):
    """
    Convert a string to int number
    from https://github.com/longld/peda
    """
    try:
        return int(str(val), 0)
    except:
        return None

def to_addr(val):
    """ Convert a value to a memory address """
    try:
        addr = to_int(get_expr(val))
        if pykd.isValid(addr):
            return addr & context.PTRMASK
    except:
        pass
        
    return None

def get_expr(val):
    """ Convert a windbg expression to real value """
    try:
        return pykd.expr(val)
    except:
        return None
    
def print_err(msg):
    pykd.dprintln(color.red(msg), dml=True)

def print_usage(doc_str):
    pykd.dprintln(color.blue(doc_str), dml=True)

def check_in_range(val, low, up):
    """ check if low <= val <= up """
    int_val = to_int(val)
    if int_val == None:
        return False
    elif low <= int_val and int_val <= up:
        return True
    else:
        return False

def check_valid_addr(val):
    """ check if val is valid memory address """
    addr, real_val = to_addr(val), get_expr(val)
    if not addr:
        errmsg = "Invalid address: "
        if real_val != None:
            errmsg += "{:#x}".format(real_val & context.PTRMASK)
        else:
            errmsg += "{}".format(val)
        return False, errmsg
    else:
        return True, None

def arg_num_in_range(args, low, up):
    """ check if low <= len(args) <= up """
    return check_in_range(len(args), low, up)

def disasm(addr):
    """ disassemble, return opcodes and  assembly string """
    resp = pykd.disasm().disasm(addr).split(" ")
    op_str = resp[1]
    asm_str = ' '.join(c for c in resp[2::]).strip()
    return op_str, asm_str

def is_executable(addr):
    if "Execute" in str(pykd.getVaProtect(addr)):
        return True
    else:
        return False

def get_string(ptr):
    """ try to get string from a pointer """
    def load_str(load_str_func):
        max_length = 30
        try:
            s = load_str_func(ptr)
            if not all(c in string.printable for c in s):
                return None
            if len(s) > max_length:
                return s[:max_length:] + "..."
            else:
                return s
        except:
            return None

    ret = load_str(pykd.loadWStr) # try load WString (unicode) first
    if not ret: ret = load_str(pykd.loadCStr) # if failed, load CStr ( ascii )

    return ret
    

def deref_ptr(ptr):
    try:
	return pykd.loadPtrs(ptr, 1)[0] & context.PTRMASK
    except pykd.MemoryException:
	return None
