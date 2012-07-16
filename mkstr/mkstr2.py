from mkstr1 import *

def makebuf(args):
    ptrlen = len(args) * 4
    #strlen = reduce(lambda x, y: x + len(y) + 1, args, 0)
    strlen = 0
    for arg in args:
        strlen += len(arg) + 1
    buf = (c_ubyte * (ptrlen + strlen))()
    iptr = 0
    istr = ptrlen
    for arg in args:
        buf[iptr:iptr+4] = conv32(addressof(buf) + istr)
        #arglen = len(arg)
        #buf[istr:istr+arglen] = map(lambda ch: ord(ch), arg)
        for ch in arg:
            buf[istr] = ord(ch)
            istr += 1
        iptr += 4
        #istr += arglen + 1
        istr += 1
    return buf

strs = ["msvcrt.dll", "getchar", "putchar"]
buf = makebuf(strs)

print "addressof(buf) = " + hex(addressof(buf))
print map(lambda x: hex(x), buf)

f.argtypes = [c_void_p, c_void_p, c_int, c_void_p]
f(printf, putchar, len(strs), buf)

VirtualFree(p, 0, MEM_RELEASE)

