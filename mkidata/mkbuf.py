import ctypes

def conv32(address):
    result = []
    print hex(address)
    result.append( address & 0xff)
    result.append( (address >> 8) & 0xff)
    result.append( (address >> 16) & 0xff)
    result.append( (address >> 24) & 0xff)
    return result


def makebuf(args):
    i = 0
    strlen = 0
    indexlen = len(args) * 4
    for arg in args:
        strlen += len(arg+"\0")
    buf = (ctypes.c_ubyte * (indexlen + strlen))()

    strlen = 0
    for arg in args:
        buf[i: i+4] = conv32(ctypes.addressof(buf) + indexlen + strlen)
        strlen += len(arg+"\0")
        i += 4

    for arg in args:
        for str in arg+"\0":
            buf[i] = (ord(str))
            i += 1
    return buf

strs = ["msvcrt.dll", "getchar", "putchar"]
buf = makebuf(strs)

print "addressof(buf) = " + hex(ctypes.addressof(buf))
print map(lambda x: hex(x), buf)
