#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, struct
from ctypes import *

VirtualAlloc = windll.kernel32.VirtualAlloc
VirtualFree  = windll.kernel32.VirtualFree
MEM_COMMIT   = 0x1000
MEM_RELEASE  = 0x8000
PAGE_EXECUTE_READWRITE = 0x40

putchar = CFUNCTYPE(None, c_int)(lambda ch: sys.stdout.write(chr(ch)))
getchar = CFUNCTYPE(c_int)(lambda: ord(sys.stdin.read(1)))
getaddr = CFUNCTYPE(c_void_p, c_void_p)(lambda p: p)
def conv32(dw): return map(lambda x: ord(x), struct.pack("<l", dw))

f = open(sys.argv[1])
bf = f.read()
f.close()

mem = (c_ubyte * 30000)()
codes = []
begin = []

codes += [0x56]                             # push esi
codes += [0x8b, 0x74, 0x24, 0x08]           # mov esi, [esp+8]

for cur in bf:
    if cur == "+":
        codes += [0xfe,0x06]                # inc byte ptr[esi]
    elif cur == "-":
        codes += [0xfe,0x0e]                # dec byte ptr[esi]
    elif cur == ">":
        codes += [0x46]                     # inc esi
    elif cur == "<":
        codes += [0x4e]                     # dec esi
    elif cur == ".":
        codes += [0x0f, 0xb6, 0x06]         # movzx eax, byte ptr[esi]
        codes += [0x50]                     # push eax
        codes += [0xff, 0x54, 0x24, 0x10]   # call [esp+16]
        codes += [0x83, 0xc4, 0x04]         # add esp, 4
    elif cur == ",":
        codes += [0xff, 0x54, 0x24, 0x10]   # call [esp+16]
        codes += [0x88, 0x06]               # mov byte ptr[esi], al
    elif cur == "[":
        begin += [len(codes)]
        codes += [0x80, 0x3e, 0x00]         # cmp byte ptr[esi], 0
        codes += [0x0f, 0x84, 0, 0, 0, 0]   # jz near ????
    elif cur == "]":
        ad1 = begin.pop()
        ad2 = len(codes) + 5
        codes[ad1+5:ad1+9] = conv32(ad2 - (ad1 + 9))
        codes += [0xe9] + conv32(ad1 - ad2) # jmp near begin

codes += [0x5e]                             # pop esi
codes += [0xc3]                             # ret

#print map(lambda x: hex(x), codes)
buflen = len(codes)
VirtualAlloc.restype = POINTER(ARRAY(c_ubyte, buflen))
p = VirtualAlloc(0, buflen, MEM_COMMIT, PAGE_EXECUTE_READWRITE)[0]
p[:] = codes[:]
f = CFUNCTYPE(None, c_void_p, c_void_p, c_void_p)(getaddr(p))

f(mem, putchar, getchar)

VirtualFree(p, 0, MEM_RELEASE)
