#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path

#__mem = [0]
#__pointer = 0
#__result = ""
__f = open('bf.s', 'w')

#buffersize = 30000
indent = 0

def translator(src):
    #print src
    cmds = list(src)
    #global __mem
    #global __pointer
    #global __result
    global __f
    global indent
    for (i,cmd) in zip(range(0, len(cmds)), cmds):
        if cmd == '+':
            #__f.writelines("mem[ptr]++;\n");
            __f.writelines("inc byte ptr[esi]\n");
        elif cmd == '-':
            __f.writelines("dec byte ptr[esi]\n");
        elif cmd == '>':
            __f.writelines("inc esi\n");
        elif cmd == '<':
            __f.writelines("dec esi\n");
        elif cmd == '.':
            __f.writelines("movzx eax, byte ptr [esi]\n");
            __f.writelines("push eax\n");
            __f.writelines("call _putchar\n");
            __f.writelines("add esp, 4\n");
        #elif cmd == ',':
            #__f.writelines("mem[ptr]=getchar();\n");
        elif cmd == '[':
            __f.writelines(str(indent)+":\n");
            __f.writelines("test byte ptr [esi],0\n");
            __f.writelines("jz "+str(indent)+"f\n");
            indent = indent + 1
        elif cmd == ']':
            indent = indent - 1
            __f.writelines("jmp "+str(indent)+"b\n");
            __f.writelines(str(indent)+":\n");

if len(sys.argv) <= 1:
    print 'brain fuck src required.'
    exit()

if os.path.isfile(sys.argv[1]):
    f = open(sys.argv[1])
    args = f.readline()
else:
    print 'brain fuck src not found.'
    args = sys.argv[1]

# 以下の文字を削除
# \t \n \r \v \f
bf_src = ""
for arg in args:
    bf_src += str(arg.rstrip())

__f.writelines( ".intel_syntax noprefix\n" )
__f.writelines( ".comm mem, 30000\n" )
__f.writelines( ".global _main\n" )
__f.writelines( "_main:\n" )
__f.writelines( "lea esi, mem\n" )
# トランスレータ実行
translator(bf_src)
__f.writelines( "push 0\n")
__f.writelines( "call _exit\n")
#for r in range(indent):
#    __f.writelines("}\n");

#__f.writelines( "}\n")
__f.close()

# 結果
#print __result
