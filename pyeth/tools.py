import math
from rlp.utils import ALL_BYTES


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