#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os.path

__mem = [0]
__pointer = 0
__result = ""

def interpreter(src, recursive=False):
    #print src
    cmds = list(src)
    global __mem
    global __pointer
    global __result
    cnt = 0
    for (i,cmd) in zip(range(0, len(cmds)), cmds):
        #print str(cmd) + ":" + str(cnt)
        if cnt == 0:
            if cmd == '+':
                __mem[__pointer] += 1
            elif cmd == '-':
                __mem[__pointer] -= 1
            elif cmd == '>':
                __pointer += 1
                if len(__mem) < __pointer + 1:
                    __mem.append(0)
            elif cmd == '<':
                __pointer -= 1
            elif cmd == '.':
                __result += chr(__mem[__pointer])
            elif cmd == ',':
                __result += str(raw_input())

        if cmd == '[':
            cnt += 1
            if cnt == 1:
                while __mem[__pointer] > 0:
                    #print "recursive"
                    interpreter(src[ i + 1 : ], True)
        elif cmd == ']':
            if cnt > 0:
                cnt -= 1
            elif cnt == 0:
                if recursive:
                    break

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

# インタープリタ実行
interpreter(bf_src)

# 結果
print __result
