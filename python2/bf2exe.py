#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, struct, ctypes
import idata

def convstr(v):
    return map(lambda x: ord(x), v)

def write16(p, values):
    for v in values:
        buf[p:p+2] = conv16(v)
        p += 2

def conv32(v): return map(ord, struct.pack("<l" if v < 0 else "<L", v))
def conv16(v): return map(ord, struct.pack("<H", v))

f = open(sys.argv[1])
bf = f.read()
f.close()

codes = []
begin = []

codes += [0x56]                             # push esi
#codes += [0x8b, 0x74, 0x24, 0x08]          # mov esi, [esp+8]
# TODO: サイズが変わったときに対応
codes += [0xbe, 0x00, 0x30, 0x40, 0x00]     # mov esi, 0x403000

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
        # call
        codes += [0xff, 0x15]
        # address
        codes += conv32(0x00402038)         # TODO: 暫定で決めうちのアドレスになってるので、直す必要有り。
        codes += [0x83, 0xc4, 0x04]         # add esp, 4
    elif cur == ",":
        # call
        codes += [0xff, 0x15]
        # address
        codes += conv32(0x00402034)         # TODO: 暫定で決めうちのアドレスになってるので、直す必要有り。
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
codes += [0xb8, 0, 0, 0, 0]                 # mov eax, 0
codes += [0xc3]                             # ret

# IMAGE_DOS_HEADER
buf = (ctypes.c_ubyte * 0x1400)()
buf[0:2] = convstr("MZ")
write16(2, [0x90, 3, 0, 4, 0, 0xffff])
buf[0x10] = 0xb8
buf[0x18] = 0x40
buf[0x3c:0x40] = conv32(0x80)
# DOS_BINARY
buf[0x40:0x45] = [0xb8, 0x01, 0x4c, 0xcd, 0x21]

# IMAGE_NT_HEADERS32
buf[0x80:0x82] = convstr("PE")
buf[0x84:0x86] = conv16(0x014c)
buf[0x86:0x88] = conv16(0x0003) # NumberOfSections
#buf[0x88:0x8c] = conv32(0x4da65f9b)
buf[0x94:0x96] = conv16(0x00e0)
buf[0x96:0x98] = conv16(0x0102)

# IMAGE_OPTIONAL_HEADER32
buf[0x98:0x9a] = conv16(0x010b)
buf[0x9a] = 0x0a
buf[0x9c:0xa0] = conv32(0x200)
buf[0xa8:0xac] = conv32(0x1000)
buf[0xac:0xb0] = conv32(0x1000)
buf[0xb0:0xb4] = conv32(0x2000)
buf[0xb4:0xb8] = conv32(0x400000)
buf[0xb8:0xbc] = conv32(0x1000)
buf[0xbc:0xc0] = conv32(0x200)
buf[0xc0:0xc2] = conv16(0x5)
buf[0xc2:0xc4] = conv16(0x1)
buf[0xc8:0xca] = conv16(0x5)
buf[0xca:0xcc] = conv16(0x1)
buf[0xd0:0xd4] = conv32(0xb000)         # SizeOfImage
buf[0xd4:0xd8] = conv32(0x200)
buf[0xdc:0xde] = conv16(0x3)            # Subsystem
buf[0xe0:0xe4] = conv32(0x100000)
buf[0xe4:0xe8] = conv32(0x1000)
buf[0xe8:0xec] = conv32(0x100000)
buf[0xec:0xf0] = conv32(0x1000)
buf[0xf4:0xf8] = conv32(0x10)

rva = 0x2000
dlls = {"msvcrt.dll": ["getchar", "putchar"]}
ibuf = idata.makeidata(dlls, rva)

# IMAGE_DATA_DIRECTORY
buf[0x100:0x104] = conv32(rva)          #VirtualAddress
buf[0x104:0x108] = conv32(0x1000)       #Size

# IMAGE_SECTION_HEADER
buf[0x178:0x17d] = convstr(".text")
buf[0x180:0x184] = conv32(0x1000)       # メモリ上のサイズ
buf[0x184:0x188] = conv32(0x1000)       # rva
buf[0x188:0x18c] = conv32(0x1000)       # ファイル上のサイズ 
buf[0x18c:0x190] = conv32(0x00000200)   # ファイル上の位置
buf[0x19c:0x1a0] = conv32(0x60000020)   # 属性

# IMAGE_SECTION_HEADER
buf[0x1a0:0x1a6] = convstr(".idata")
buf[0x1a8:0x1ac] = conv32(len(ibuf))    # idata のサイズを入れる
buf[0x1ac:0x1b0] = conv32(rva)
buf[0x1b0:0x1b4] = conv32(0x200)        # ファイル上のサイズ
buf[0x1b4:0x1b8] = conv32(0x00001200)   # ファイル上の位置
buf[0x1c4:0x1c8] = conv32(0xC0300040)   # dllの場合

# IMAGE_SECTION_HEADER
buf[0x1c8:0x1cc] = convstr(".bss")
buf[0x1d0:0x1d4] = conv32(30000)        # メモリ上のサイズ bfのメモリは30000
buf[0x1d4:0x1d8] = conv32(0x3000)       # rva
buf[0x1d8:0x1dc] = conv32(0)            # ファイル上のサイズ 
buf[0x1dc:0x1e0] = conv32(0)            # ファイル上の位置
buf[0x1ec:0x1f0] = conv32(0xc0600080)   # 属性

# .text
buf[0x200:0x200+len(codes)] = codes

# .idata
buf[0x1200:0x1200+len(ibuf)] = ibuf

f = open("bf.exe", "wb")
f.write(buf)
f.close()


