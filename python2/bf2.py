#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

f = open(sys.argv[1])
bf = f.read()
f.close()

cur = 0
reg = 0
mem = [0] * 30000
begin = []

while cur < len(bf):

    if bf[cur] == "+":
        mem[reg] += 1
    elif bf[cur] == "-":
        mem[reg] -= 1
    elif bf[cur] == ">":
        reg += 1
    elif bf[cur] == "<":
        reg -= 1
    elif bf[cur] == ".":
        sys.stdout.write(chr(mem[reg]))
    elif bf[cur] == ",":
        mem[reg] = ord(sys.stdin.read(1))
    elif bf[cur] == "[":
        if mem[reg] != 0:
            begin += [cur]
        else:
            nest = 0
            while cur < len(bf):
                if bf[cur] == "[":
                    nest += 1
                elif bf[cur] == "]":
                    nest -= 1
                    if nest == 0:
                        break
                cur += 1
    elif bf[cur] == "]":
        cur = begin.pop() - 1

    cur += 1
