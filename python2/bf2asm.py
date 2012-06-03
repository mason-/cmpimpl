#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

bf = ""
arg = sys.argv[1]
if os.path.isfile(arg):
    f = open(arg)
    bf += f.read()
    f.close()

cur = 0
reg = 0
mem = [0] * 30000
begin = []

print ".intel_syntax noprefix"
print ".comm mem, 30000"
print ".global _main"
print "_main:"
print " lea esi, mem"

nest = 0
while cur < len(bf):

    if bf[cur] == "+":
        print "inc byte ptr[esi]"
    elif bf[cur] == "-":
        print "dec byte ptr[esi]"
    elif bf[cur] == ">":
        print "inc esi"
    elif bf[cur] == "<":
        print "dec esi"
    elif bf[cur] == ".":
        print "movzx eax, byte ptr[esi]"
        print "push eax"
        print "call _putchar"
        print "add esp, 4"
    elif bf[cur] == ",":
        print "call _getchar"
        print "mov byte ptr[esi], al"
    elif bf[cur] == "[":
        print "%d:" % nest
        print "cmp byte ptr[esi], 0"
        print "jz %df" % nest
        nest += 1
    elif bf[cur] == "]":
        nest -= 1
        print "jmp %db" % nest
        print "%d:" % nest
    cur += 1

print "push 0"
print "call _exit"

