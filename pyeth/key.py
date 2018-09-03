from pyeth.tools import *
from .bip39_mnemonic import generate_entropy
from .encode import *


def create_private_key():
    """
        Create private key
    """
    key=generate_entropy()
    return key



def is_private_key_valid(key):
    """
    Check public key is valid.
    :param key: public key in HEX or bytes string format.
    :return: boolean.
    """
    if isinstance(key, str):
        key = bytes.fromhex(key)
    if len(key) < 33:
        return False
    elif key[0] == 0x04 and len(key) != 65:
        return False
    elif key[0] == 0x02 or key[0] == 0x03:
        if len(key) != 33:
            return False
    return True


def normalize_key(key):
    if is_numeric(key):
        o = encode_int32(key)
    elif len(key) == 32:
        o = key
    elif len(key) == 64:
        o = decode_hex(key)
    elif len(key) == 66 and key[:2] == '0x':
        o = decode_hex(key[2:])
    else:
        raise Exception("Invalid key format: %r" % key)
    if o == b'\x00' * 32:
        raise Exception("Zero privkey invalid")
    return o



