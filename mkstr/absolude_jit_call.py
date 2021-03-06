from jit import *

codes = [
    0x6a, 0x41,                   # push 65
    0xb8, 0x00, 0x00, 0x00, 0x00, # mov eax, 0
    0xff, 0xd0,                   # call eax
    0x83, 0xc4, 0x04,             # add esp, 4
    0xc3,                         # ret
]

p = VirtualAlloc(0, len(codes), MEM_COMMIT, PAGE_EXECUTE_READWRITE)
p[:] = codes
debug(p)
p[3:7] = conv32(getaddr(putchar))
debug(p)

CFUNCTYPE(None)(getaddr(p))()

VirtualFree(p, 0, MEM_RELEASE)

