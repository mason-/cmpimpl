#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path

mem = []
ptr = 0
indent = 0
tgt = ""
tgt_is_x86  = False
tgt_is_x86i = False
tgt_is_elf  = False

def translate(src):
    #print src
    cmds = list(src)
    global mem, ptr, indent
    i = 0
    start = []
    while i < len(src):
        cmd = src[i]
        if cmd == '+':
            if tgt == "": mem[ptr] += 1
            elif tgt == "c"    : write("(*ptr)++;")
            elif tgt == "mac64": write("incb (%r12)")
            elif tgt_is_x86    : write("incb (%esi)")
            elif tgt_is_x86i   : write("inc byte ptr[esi]")
        elif cmd == '-':
            if tgt == "": mem[ptr] -= 1
            elif tgt == "c"    : write("(*ptr)--;")
            elif tgt == "mac64": write("decb (%r12)")
            elif tgt_is_x86    : write("decb (%esi)")
            elif tgt_is_x86i   : write("dec byte ptr[esi]")
        elif cmd == '>':
            if tgt == "": ptr += 1
            elif tgt == "c"    : write("ptr++;")
            elif tgt == "mac64": write("incq %r12")
            elif tgt_is_x86    : write("incl %esi")
            elif tgt_is_x86i   : write("inc esi")
        elif cmd == '<':
            if tgt == "": ptr -= 1
            elif tgt == "c"    : write("ptr--;")
            elif tgt == "mac64": write("decq %r12")
            elif tgt_is_x86    : write("decl %esi")
            elif tgt_is_x86i   : write("dec esi")
        elif cmd == '.':
            if tgt == "":
               sys.stdout.write(chr(mem[ptr]))
            elif tgt == "c":
                write("putchar(*ptr);")
            elif tgt == "mac64":
                write("movzbl (%r12), %edi")
                write("callq _putchar")
            else:
                if tgt_is_x86:
                    write("movzbl (%esi), %eax")
                    write("movl %eax, (%esp)")
                elif tgt_is_x86i:
                    write("movzx eax, byte ptr[esi]")
                    write("mov [esp], eax")
                if tgt_is_elf: write("call putchar")
                else         : write("call _putchar")
        elif cmd == ',':
            if tgt == "":
                mem[ptr] = sys.stdin.read(1)
            elif tgt == "c":
                write("*ptr = getchar();")
            elif tgt == "mac64":
                write("callq _getchar")
                write("movb %al, (%r12)")
            else:
                if tgt_is_elf: write("call getchar")
                else         : write("call _getchar")
                if tgt_is_x86: write("movb %al, (%esi)")
                else         : write("mov byte ptr[esi], al")
        elif cmd == '[':
            if tgt == "":
                start.append(i)
                if mem[ptr] == 0:
                    ind = 0
                    while i < len(src):
                        cmd = src[i]
                        if cmd == '[':
                            ind += 1
                        elif cmd == ']':
                            ind -= 1
                            if ind == 0: break
                        i += 1
                    if ind > 0:
                        print "block end required."
                        exit(1)
                    indent -= 1
            elif tgt == "c":
                write("while (*ptr) {")
            else:
                write("%d:" % indent, False);
                if   tgt == "mac64": write("cmpb $0, (%r12)")
                elif tgt_is_x86    : write("cmpb $0, (%esi)")
                elif tgt_is_x86i   : write("cmp byte ptr[esi], 0")
                write("jz %df" % indent)
            indent += 1
        elif cmd == ']':
            if indent == 0:
                print "block start required."
                exit(1)
            indent -= 1
            if tgt == "":
                i = start.pop() - 1
            elif tgt == "c":
                write("}")
            else:
                write("jmp %db" % indent)
                write("%d:" % indent, False)
        i += 1

bf_src = ""
dest = ""
srcs = []

for arg in sys.argv[1:]:
    if arg == "-c":
        tgt = "c"
        dest = "bf.c"
    elif arg == "-mac64":
        tgt = arg[1:]
        dest = "bf.s"
    elif arg == "-mac32" or arg == "-elf32" or arg == "-win32":
        tgt = arg[1:]
        dest = "bf.s"
        tgt_is_x86 = True
    elif arg == "-elf32i" or arg == "-win32i":
        tgt = arg[1:]
        dest = "bf.s"
        tgt_is_x86i = True
    else:
        if os.path.isfile(arg):
            srcs.append(arg)
            f = open(arg)
            bf_src += f.read()
            f.close()
        else:
            print "brainf*ck src not found: " + arg
            exit(1)

if len(srcs) == 0:
    print "usage: " + sys.argv[0] + " [-c|-mac64|-mac32|-elf32[i]|-win32[i]] source.bf"
    exit(1)

if tgt != "": __f = open(dest, "w")
tgt_is_elf = tgt[:3] == "elf"

def write(line, is_indent = True):
    global __f, indent
    if is_indent: __f.write(" " * (indent * 4 + 4))
    __f.write(line + "\n")

indent = -1
if tgt == "":
    mem = [0] * 30000
elif tgt == "c":
    write("#include <stdio.h>")
    write("#include <stdlib.h>")
    write("char mem[30000];")
    write("int main(void) {")
else:
    write("# " + tgt)
    if tgt_is_x86i: write(".intel_syntax noprefix")
    write(".comm mem, 30000")
    if tgt == "mac32":
        write(".section __IMPORT,__pointers,non_lazy_symbol_pointers")
        write("_mem: .indirect_symbol mem")
        write(".long 0")
    write(".text")
    if tgt_is_elf:
        write(".globl main")
        write("main:")
    else:
        write(".globl _main")
        write("_main:")

indent = 0
if tgt == "c":
    write("char *ptr = mem;")
elif tgt == "mac64":
    write("pushq %r12")
    write("movq mem@GOTPCREL(%rip), %r12")
elif tgt == "mac32":
    write("pushl %esi")
    write("call L0")
    write("L0:", False)
    write("popl %eax")
    write("movl _mem-L0(%eax), %esi")
    write("subl $8, %esp")
elif tgt_is_x86:
    write("pushl %esi")
    write("subl $4, %esp")
    write("leal mem, %esi")
elif tgt_is_x86i:
    write("push esi")
    write("sub esp, 4")
    write("lea esi, mem")

# トランスレータ実行
translate(bf_src)

if tgt == "c":
    write("return 0;")
    write("}", False)
elif tgt == "mac64":
    write("popq %r12")
    write("movq $0, %rax")
    write("ret")
elif tgt_is_x86:
    write("addl $%d, %%esp" % (8 if tgt == "mac32" else 4))
    write("popl %esi")
    write("movl $0, %eax")
    write("ret")
elif tgt_is_x86i:
    write("add esp, 4")
    write("pop esi")
    write("mov eax, 0")
    write("ret")

if tgt != "": __f.close()

if indent != 0:
    print "block end required."
    exit(1)

# 結果
#print __result
