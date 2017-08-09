import pykd
import color

def to_int(val):
    """
    Convert a string to int number
    from https://github.com/longld/peda
    """
    try:
        return int(str(val), 0)
    except:
        return None

def print_err(msg):
    pykd.dprintln(color.red(msg), dml=True)

def print_usage(doc_str):
    pykd.dprintln(color.blue(doc_str), dml=True)
