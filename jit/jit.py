from ctypes import *
import sys

VirtualAlloc = windll.kernel32.VirtualAlloc
VirtualFree  = windll.kernel32.VirtualFree
MEM_COMMIT   = 0x1000
MEM_RELEASE  = 0x8000
PAGE_EXECUTE_READWRITE = 0x40

putchar = CFUNCTYPE(None, c_int)(
    lambda ch: sys.stdout.write(chr(ch)))

codes = (c_ubyte * 32)(
    0x6a, 0x41,             # push 65
    0xff, 0x54, 0x24, 0x08, # call [esp+8]
    0x83, 0xc4, 0x04,       # add esp, 4
    0xc3,                   # ret
)

buflen = len(codes)
p = VirtualAlloc(0, buflen, MEM_COMMIT, PAGE_EXECUTE_READWRITE)
memmove(p, addressof(codes), buflen)
f = CFUNCTYPE(None, c_void_p)(p)

f(putchar)

VirtualFree(p, 0, MEM_RELEASE)
