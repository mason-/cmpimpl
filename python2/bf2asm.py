#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

f = open(sys.argv[1])
bf = f.read()
f.close()

nest = 0

print ".intel_syntax noprefix"
print ".comm mem, 30000"
print ".global _main"
print "_main:"
print "    lea esi, mem"

for cur in bf:
    if cur == "+":
        print "    inc byte ptr[esi]"
    elif cur == "-":
        print "    dec byte ptr[esi]"
    elif cur == ">":
        print "    inc esi"
    elif cur == "<":
        print "    dec esi"
    elif cur == ".":
        print "    movzx eax, byte ptr[esi]"
        print "    push eax"
        print "    call _putchar"
        print "    add esp, 4"
    elif cur == ",":
        print "    call _getchar"
        print "    mov byte ptr[esi], al"
    elif cur == "[":
        print "%d:" % nest
        print "    cmp byte ptr[esi], 0"
        print "    jz %df" % nest
        nest += 1
    elif cur == "]":
        nest -= 1
        print "    jmp %db" % nest
        print "%d:" % nest

print "    push 0"
print "    call _exit"

