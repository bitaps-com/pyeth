from binascii import unhexlify, hexlify

from .tools import *

b58_digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def encode_base58(b):
    """Encode bytes to a base58-encoded string"""
    # Convert big-endian bytes to integer

    n= int('0x0' + b.hex(), 16)

    # Divide that integer into bas58
    res = []
    while n > 0:
        n, r = divmod(n, 58)
        res.append(b58_digits[r])
    res = ''.join(res[::-1])
    # Encode leading zeros as base58 zeros
    czero = 0
    pad = 0
    for c in b:
        if c == czero:
            pad += 1
        else:
            break
    return b58_digits[0] * pad + res


def decode_base58(s):
    """Decode a base58-encoding string, returning bytes"""
    if not s:
        return b''
    # Convert the string to an integer
    n = 0
    for c in s:
        n *= 58
        if c not in b58_digits:
            raise Exception('Character %r is not a valid base58 character' % c)
        digit = b58_digits.index(c)
        n += digit
    # Convert the integer to bytes
    h = '%x' % n
    if len(h) % 2:
        h = '0' + h
    res = bytes.fromhex(h)
    # Add padding back.
    pad = 0
    for c in s[:-1]:
        if c == b58_digits[0]:
            pad += 1
        else:
            break
    return b'\x00' * pad + res


def decode_hex(hex_type):
    byte_type=unhexlify(hex_type)
    return byte_type

def encode_hex(byte_type):
    hex_type=hexlify(byte_type).decode()
    return hex_type

def hex_to_bytes(hex_type):
    return decode_hex(hex_type[2:]) if hex_type.startswith("0x") else decode_hex(hex_type)

def bytes_to_hex(byte_type):
    return "0x%s" % encode_hex(byte_type)

def encode_int32(v):
    return zpad(int_to_bytes(v), 32)


def zpad(x, l):
    """ Left zero pad value `x` at least to length `l`.
    >>> zpad('', 1)
    '\x00'
    >>> zpad('\xca\xfe', 4)
    '\x00\x00\xca\xfe'
    >>> zpad('\xff', 1)
    '\xff'
    >>> zpad('\xca\xfe', 2)
    '\xca\xfe'
    """
    return b'\x00' * max(0, l - len(x)) + x

