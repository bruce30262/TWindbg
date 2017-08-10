import pykd
import color
import context

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
    try:
        addr = to_int(get_expr(val))
        if pykd.isValid(addr):
            return addr & context.PTRMASK
    except:
        pass
        
    return None

def get_expr(val):
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
    if not int_val:
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
            errmsg += "{:#x}".format(real_val)
        else:
            errmsg += "{}".format(val)
        return False, errmsg
    else:
        return True, None

def arg_num_in_range(args, low, up):
    """ check if low <= len(args) <= up """
    return check_in_range(len(args), low, up)