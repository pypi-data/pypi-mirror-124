
def shex(s):
    if type(s) == type(0):    return ('0' if (len(hex(s)[2:]) % 2) else '') + hex(s)[2:]
    if type(s) == type(b'0'): return s.hex()
    if type(s) == type('0'):  return s.encode().hex()

def long_to_bytes(x):
    return bytes.fromhex(shex(x))

def bytes_to_long(x):
    return int.from_bytes(x, 'big')

def sxor(a, b):
    ''' return bytes type of a xor b
    '''
    assert type(a) == type(b), "a and b must be the same type"
    if type(a) == type(0): return long_to_bytes(a ^ b)
    assert len(a) == len(b), "a and b must be the same length"
    if type(a) == type('0'): a, b = a.encode(), b.encode()
    return b''.join([long_to_bytes(a[i] ^ b[i]) for i in range(len(a))])

