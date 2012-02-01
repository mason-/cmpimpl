#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path

__mem = [0]
__pointer = 0
__result = ""
__f = open('bf.c', 'w')

buffersize = 30000
indent = 0

def translator(src):
    #print src
    cmds = list(src)
    global __mem
    global __pointer
    global __result
    global __f
    global indent
    for (i,cmd) in zip(range(0, len(cmds)), cmds):
        if cmd == '+':
            __f.writelines("mem[ptr]++;\n");
        elif cmd == '-':
            __f.writelines("mem[ptr]--;\n");
        elif cmd == '>':
            __f.writelines("ptr++;if(ptr >= "+str(buffersize)+") ptr=0;\n");
            if len(__mem) < __pointer + 1:
                f.writelines("ptr--;if(ptr < 0) ptr = "+str(buffersize - 1)+";\n");
        elif cmd == '<':
            __f.writelines("ptr--;\n");
        elif cmd == '.':
            __f.writelines("putchar(mem[ptr]);\n");
        elif cmd == ',':
            __f.writelines("mem[ptr]=getchar();\n");
        elif cmd == '[':
            __f.writelines("while(mem[ptr]){\n");
            indent = indent + 1
        elif cmd == ']':
            __f.writelines("}\n");
            indent = indent - 1

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

__f.writelines( "#include<stdio.h>\n" )
__f.writelines( "#include<string.h>\n" )
__f.writelines( "char mem["+str(buffersize)+"];\n" )
__f.writelines( "int main()\n" )
__f.writelines( "{\n" )
__f.writelines( "memset(mem,0,sizeof(mem));\n");
__f.writelines( "int ptr = 0;" )
# トランスレータ実行
translator(bf_src)
__f.writelines( "return 0;\n")
for r in range(indent):
    __f.writelines("}\n");

__f.writelines( "}\n")
__f.close()

# 結果
print __result
