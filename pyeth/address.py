from pyeth.key import *
import sha3
from py_ecc.secp256k1 import privtopub





def private_key_to_address(privkey):
    k = normalize_key(privkey)
    x, y = privtopub(k)
    return sha3.keccak_256(encode_int32(x) + encode_int32(y)).digest()[12:]

def normalize_address(x, allow_blank=False):
    if is_numeric(x):
        return int_to_addr(x)
    if allow_blank and x in {'', b''}:
        return b''
    if len(x) in (42, 50) and x[:2] in {'0x', b'0x'}:
        x = x[2:]
    if len(x) in (40, 48):
        x = decode_hex(x)
    if len(x) == 24:
        assert len(x) == 24 and sha3.keccak_256(x[:20]).digest()[:4] == x[-4:]
        x = x[:20]
    if len(x) != 20:
        raise Exception("Invalid address format: %r" % x)
    return x


def int_to_addr(x):
    o = [b''] * 20
    for i in range(20):
        o[19 - i] = ascii_chr(x & 0xff)
        x >>= 8
    return b''.join(o)



def is_address_valid(address):
    """
    Check is address valid.
    :param address: address in base58 or bech32 format.
    :return: boolean.
    """
    return checksum_encode(normalize_address(address)) == address

def checksum_encode(address):  # Takes a 20-byte binary address as input
    address = normalize_address(address)
    o = ''
    encode_adrr=encode_hex(address)
    _sha3=sha3.keccak_256(encode_adrr.encode('utf-8')).digest()
    v = bytes_to_int(_sha3)
    for i, c in enumerate(encode_hex(address)):
        if c in '0123456789':
            o += c
        else:
            o += c.upper() if (v & (2**(255 - 4 * i))) else c.lower()
    return '0x' + o