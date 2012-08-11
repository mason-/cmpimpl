#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

# 使い方
# python exe.py
# wine bf.exe
# echo $?

from struct import *
from ctypes import *

def conv16(v):
    return map(lambda x: ord(x), pack("<H", v))

def conv32(v):
    return map(lambda x: ord(x), pack("<L", v))

def convstr(v):
    return map(lambda x: ord(x), v)

def write16(p, values):
    for v in values:
        buf[p:p+2] = conv16(v)
        p += 2

# IMAGE_DOS_HEADER
buf = (c_ubyte * 0x400)()
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
buf[0x86:0x88] = conv16(0x0001)
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
buf[0xd0:0xd4] = conv32(0x2000)
buf[0xd4:0xd8] = conv32(0x200)
buf[0xdc:0xde] = conv16(0x3)
buf[0xe0:0xe4] = conv32(0x100000)
buf[0xe4:0xe8] = conv32(0x1000)
buf[0xe8:0xec] = conv32(0x100000)
buf[0xec:0xf0] = conv32(0x1000)
buf[0xf4:0xf8] = conv32(0x10)
# IMAGE_DATA_DIRECTORY
# IMAGE_SECTION_HEADER
buf[0x178:0x17d] = convstr(".text")
buf[0x180:0x184] = conv32(0x1)
buf[0x184:0x188] = conv32(0x1000)
buf[0x188:0x18c] = conv32(0x200)
buf[0x18c:0x190] = conv32(0x00000200)
buf[0x19c:0x1a0] = conv32(0x60000020)

# .text
buf[0x200] = 0xc3
"""
#b8 03 00 00 00          mov    $0x3,%eax
buf[0x200] = 0xb8
buf[0x201:0x205] = conv32(3)
#83 c0 02                add    $0x2,%eax
buf[0x205:0x207] = conv16(0xc083)
buf[0x207] = 0x02
#83 e8 01                sub    $0x1,%eax
buf[0x208:0x20a] = conv16(0xe883)
buf[0x20a] = 0x01
buf[0x20b] = 0xc3
"""

f = open("bf.exe", "wb")
f.write(buf)
f.close()


