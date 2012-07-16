import sys, struct
from ctypes import *

def VirtualAlloc(address, size, allocationType, protect):
    VirtualAlloc = windll.kernel32.VirtualAlloc
    VirtualAlloc.restype = POINTER(ARRAY(c_ubyte, size))
    VirtualAlloc.argtype = [c_void_p, c_size_t, c_int, c_int]
    return VirtualAlloc(address, size, allocationType, protect)[0]

VirtualFree = windll.kernel32.VirtualFree
VirtualFree.argtype = [c_void_p, c_int, c_int]
MEM_COMMIT  = 0x1000
MEM_RELEASE = 0x8000
PAGE_EXECUTE_READWRITE = 0x40

putchar = CFUNCTYPE(None, c_int)(lambda ch: sys.stdout.write(chr(ch)))
getaddr = CFUNCTYPE(c_void_p, c_void_p)(lambda p: p)

def conv32(dw):
    return map(lambda x: ord(x), struct.pack(
        "<l" if dw < 0 else "<L", dw))

"""
print "---- jit.py debug start"
print "putchar : " + hex(getaddr(putchar))
print "getchar : " + hex(getaddr(getaddr))
print "---- jit.py debug end"
"""

def debug(va):
    """
    print "debug start"
    for i,a in enumerate(va):
        print '%(#)03d : %(val)x' % {"#" : i, "val":a}
    """
