from jit import *

codes = [
    0x6a, 0x41,             # push 65
    0xff, 0x54, 0x24, 0x08, # call [esp+8]
    0x83, 0xc4, 0x04,       # add esp, 4
    0xc3,                   # ret
]

p = VirtualAlloc(0, len(codes), MEM_COMMIT, PAGE_EXECUTE_READWRITE)
p[:] = codes

CFUNCTYPE(c_void_p)(getaddr(p))(putchar)

VirtualFree(p, 0, MEM_RELEASE)
