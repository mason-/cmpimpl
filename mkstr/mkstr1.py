import sys
from jit import *

# for (i = 0; i < argc; i++) {
#     printf(argv[i]);
#     putchar(' ');
# }
codes = [
    0x56,                    # push esi
    0x8b, 0x74, 0x24, 0x14,  # mov esi, dword ptr[esp+20]
    0xff, 0x36,              # 0:  push dword ptr[esi]
    0x83, 0xc6, 0x04,        #     add esi, 4
    0xff, 0x54, 0x24, 0x0c,  #     call [esp+12]
    0x83, 0xc4, 0x04,        #     add esp, 0x4
    0x6a, 0x20,              #     push 32
    0xff, 0x54, 0x24, 0x10,  #     call [esp+16]
    0x83, 0xc4, 0x04,        #     add esp, 0x4
    0xff, 0x4c, 0x24, 0x10,  #     dec dword ptr[esp+16]
    0x75, 0xe5,              #     jnz 0b
    0x5e,                    # pop esi
    0xc3,                    # ret
]

printf = CFUNCTYPE(None, c_char_p)(lambda s: sys.stdout.write(s))

p = VirtualAlloc(0, len(codes), MEM_COMMIT, PAGE_EXECUTE_READWRITE)
p[:] = codes
f = CFUNCTYPE(
        None, c_void_p, c_void_p, c_int, POINTER(c_char_p)
    )(getaddr(p))

if __name__ == "__main__":
    argc = len(sys.argv)
    argv = (c_char_p * argc)()
    argv[:] = sys.argv[:]
    f(printf, putchar, argc, argv)
    VirtualFree(p, 0, MEM_RELEASE)
