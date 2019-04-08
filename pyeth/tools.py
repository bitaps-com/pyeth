import math
import struct


ALL_BYTES = tuple(
    struct.pack('B', i)
    for i in range(256)
)

int_from_bytes = int.from_bytes

def is_numeric(x):
    return isinstance(x, int)


def ascii_chr(n):
    return ALL_BYTES[n]

def bytes_needed(n):
    """
    Calculate bytes needed to convert integer to bytes.
    :param n: integer.
    :return: integer.
    """
    if n == 0:
        return 1
    return math.ceil(n.bit_length()/8)

def int_to_bytes(i, byteorder='big'):
    """
    Convert integer to bytes.
    :param n: integer.
    :param byteorder: (optional) byte order 'big' or 'little', by default 'big'.
    :return: bytes.
    """
    return i.to_bytes(bytes_needed(i), byteorder=byteorder, signed=False)


def bytes_to_int(i, byteorder='big'):
    """
    Convert bytes to integer.
    :param i: bytes.
    :param byteorder: (optional) byte order 'big' or 'little', by default 'big'.
    :return: integer.
    """
    return int.from_bytes(i, byteorder=byteorder, signed=False)


def int_to_var_int(i):
    """
    Convert integer to variable integer
    :param i: integer.
    :return: bytes.
    """
    if i < 0xfd:
        return struct.pack('<B', i)
    if i <= 0xffff:
        return b'\xfd%s' % struct.pack('<H', i)
    if i <= 0xffffffff:
        return b'\xfe%s' % struct.pack('<L', i)
    return b'\xff%s' % struct.pack('<Q', i)


def var_int_to_int(data):
    """
    Convert variable integer to integer
    :param data: bytes variable integer.
    :return: integer.
    """
    if data[0] == 0xfd:
        return struct.unpack('<H', data[1:3])[0]
    elif data[0] == 0xfe:
        return struct.unpack('<L', data[1:5])[0]
    elif data[0] == 0xff:
        return struct.unpack('<Q', data[1:9])[0]
    return data[0]



def int_to_c_int(n, base_bytes=1):
    """
    Convert integer to compresed integer
    :param n: integer.
    :param base_bytes: len of bytes base from which start compression.
    :return: bytes.
    """
    if n == 0:
        return b'\x00' * base_bytes
    else:
        l = n.bit_length() + 1
    min_bits = base_bytes * 8 - 1
    if l <= min_bits + 1:
        return n.to_bytes(base_bytes, byteorder="big")
    prefix = 0
    payload_bytes = math.ceil((l)/8) - base_bytes
    a = payload_bytes
    while True:
        add_bytes = math.floor((a) / 8)
        a = add_bytes
        if add_bytes >= 1:
            add_bytes += math.floor((payload_bytes + add_bytes) / 8) - math.floor((payload_bytes) / 8)
            payload_bytes += add_bytes
        if a == 0: break
    extra_bytes = int(math.ceil((l+payload_bytes)/8) - base_bytes)
    for i in range(extra_bytes):
        prefix += 2 ** i
    if l < base_bytes * 8:
        l = base_bytes * 8
    prefix = prefix << l
    if prefix.bit_length() % 8:
        prefix = prefix << 8 - prefix.bit_length() % 8
    n ^= prefix
    return n.to_bytes(math.ceil(n.bit_length()/8), byteorder="big")


def c_int_to_int(b, base_bytes=1):
    """
    Convert compressed integer bytes to integer
    :param b: compressed integer bytes.
    :param base_bytes: len of bytes base from which start compression.
    :return: integer.
    """
    byte_length = 0
    f = 0
    while True:
        v = b[f]
        if v == 0xff:
            byte_length += 8
            f += 1
            continue
        while v & 0b10000000:
            byte_length += 1
            v = v << 1
        break
    n = int_from_bytes(b[:byte_length+base_bytes], byteorder="big")
    if byte_length:
        return n & ((1 << (byte_length+base_bytes) * 8 - byte_length) - 1)
    return n


def c_int_len(n, base_bytes=1):
    """
    Get length of compressed integer from integer value
    :param n: bytes.
    :param base_bytes: len of bytes base from which start compression.
    :return: integer.
    """
    if n == 0:
        return 1
    l = n.bit_length() + 1
    min_bits = base_bytes * 8 - 1
    if l <= min_bits + 1:
        return 1
    payload_bytes = math.ceil((l)/8) - base_bytes
    a = payload_bytes
    while True:
        add_bytes = math.floor((a) / 8)
        a = add_bytes
        if add_bytes >= 1:
            add_bytes += math.floor((payload_bytes + add_bytes) / 8) - math.floor((payload_bytes) / 8)
            payload_bytes += add_bytes
        if a == 0: break
    return int(math.ceil((l+payload_bytes)/8))