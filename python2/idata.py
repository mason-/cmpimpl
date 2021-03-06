#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import ctypes, sys

def dumpHexAscii(data, start=0):
    i = 0
    while i < len(data):
        sys.stdout.write("%08X " % (start + i))
        sb = "  "
        for j in range(16):
            if j == 8: sys.stdout.write(" ")
            if i + j < len(data):
                b = data[i + j]
                sys.stdout.write(" %02X" % b)
                sb += "." if b < 32 or b >= 127 else chr(b)
            else:
                sys.stdout.write("   ")
        print sb
        i += 16

def conv32(address):
    result = []
    #print hex(address)
    result.append( address & 0xff)
    result.append( (address >> 8) & 0xff)
    result.append( (address >> 16) & 0xff)
    result.append( (address >> 24) & 0xff)
    return result


def makeidata(dlls, rva):
    idtlen = 20 * (len(dlls) + 1)
    iltlen = 0
    tablelen = 0
    namelen = 0
    for dll, funcs in dlls.iteritems():
        # import lookup table
        iltlen += 4 * (len(funcs) + 1)
        # dll name
        namelen += len(dll) + 1
        for f in funcs:
            # hint/name table
            tablelen += 2 + len(f) + 1
            #if tablelen % 2 == 1:
            if tablelen & 1 == 1:
                tablelen += 1
    idatalen = idtlen + iltlen * 2 + tablelen + namelen

    # idataのメモリを確保
    buf = (ctypes.c_ubyte * idatalen)()

    # IDTにName へのアドレスを埋め込む
    ptr = 0
    dllnameptr = rva + idtlen + iltlen * 2 + tablelen
    for dll in dlls:
        buf[ptr+12:ptr+16] = conv32( dllnameptr )
        dllnameptr += len(dll) + 1
        # IMAGE_IMPORT_DESCRIPTOR のサイズ分インクリメント
        ptr += 20

    # Name を埋め込む
    ptr = idtlen + iltlen * 2 + tablelen
    for dll in dlls.keys():
        for ch in dll+"\0":
            buf[ptr] = ord(ch)
            ptr += 1

    # IDTにILT(import lookup table) へのアドレスを埋め込む
    ptr = 0
    iltptr = rva + idtlen
    for dll, funcs in dlls.iteritems():
        # import lookup table
        buf[ptr:ptr+4] = conv32(iltptr)
        iltptr += 4 * (len(funcs) + 1)
        # IMAGE_IMPORT_DESCRIPTOR のサイズ分インクリメント
        ptr += 20

    # IDTにIAT(import address table) へのアドレスを埋め込む
    ptr = 0
    iatptr = rva + idtlen + iltlen
    for dll, funcs in dlls.iteritems():
        # import lookup table
        buf[ptr+16:ptr+20] = conv32(iatptr)
        iatptr += 4 * (len(funcs) + 1)
        # IMAGE_IMPORT_DESCRIPTOR のサイズ分インクリメント
        ptr += 20

    # ILTにヒント/名前テーブルへのアドレスを埋め込む
    ptr = idtlen
    hintnameptr = rva + idtlen + iltlen * 2
    for dll, funcs in dlls.iteritems():
        for f in funcs:
            buf[ptr:ptr+4] = conv32( hintnameptr )
            funcnamelen = len(f) + 1
            # 序数の2bytes + 関数名+Null終端 + パディング（funcnamelenが奇数の場合に1足している）
            hintnameptr += 2 + funcnamelen + (funcnamelen & 1)
            ptr += 4
        # ILT のNull終端分インクリメント
        ptr += 4

    # IATにヒント/名前テーブルへのアドレスを埋め込む
    ptr = idtlen + iltlen
    hintnameptr = rva + idtlen + iltlen * 2
    for dll, funcs in dlls.iteritems():
        for f in funcs:
            buf[ptr:ptr+4] = conv32( hintnameptr )
            funcnamelen = len(f) + 1
            # 序数の2bytes + 関数名+Null終端 + パディング（funcnamelenが奇数の場合に1足している）
            hintnameptr += 2 + funcnamelen + (funcnamelen & 1)
            ptr += 4
        # IAT のNull終端分インクリメント
        ptr += 4

    # ヒント/名前テーブルを作成する
    ptr = idtlen + iltlen * 2
    for dll, funcs in dlls.iteritems():
        for f in funcs:
            # 序数2bytes分加算
            ptr += 2
            # シンボル名
            for ch in f:
                buf[ptr] = ord(ch)
                ptr += 1
            # Null終端分1byte加算
            ptr += 1
            # align2なので、シンボル名+Null終端に文字数が奇数の場合、0埋めします。
            #if (len(f) + 1) & 1 == 1: ptr += 1
            if ptr & 1 == 1 : ptr += 1

    return buf

if __name__ == "__main__":
    dlls = {"test1.dll": ["func1a", "func1b"], "test2.dll": ["func2a", "func2b"]}
    rva = 0x2000
    buf = makeidata(dlls, rva)
    dumpHexAscii(buf, rva)

