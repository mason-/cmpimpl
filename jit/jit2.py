from ctypes import *
from struct import *

VirtualAlloc = windll.kernel32.VirtualAlloc
VirtualFree  = windll.kernel32.VirtualFree
MEM_COMMIT   = 0x1000
MEM_RELEASE  = 0x8000
PAGE_EXECUTE_READWRITE = 0x40

codes = (c_ubyte * 32)(
    0x6a, 0x42,                     # push 65
    0xe8, 0x00, 0x00, 0x00, 0x00,   # call xxxx
    0x83, 0xc4, 0x04,               # add esp, 4
    0xc3,                           # ret
)

buflen = len(codes)
p = VirtualAlloc(0, buflen, MEM_COMMIT, PAGE_EXECUTE_READWRITE)

getaddr = CFUNCTYPE(c_void_p, c_void_p)(lambda p: p)
putchar = cdll.msvcrt.putchar

codes[3:7] = map(lambda a: ord(a), pack("<L", getaddr(putchar) - (p + 7)))
memmove(p, addressof(codes), buflen)

f = CFUNCTYPE(None)(p)
f()

VirtualFree(p, 0, MEM_RELEASE)



