import coincurve
import rlp
import sha3
from py_ecc.secp256k1 import ecdsa_raw_sign

from .encode import *
from .tools import *

EIP155_CHAIN_ID_OFFSET = 35
V_OFFSET = 27

def ecsign(rawhash, key, chain_id=None):
    if coincurve and hasattr(coincurve, 'PrivateKey'):
        pk = coincurve.PrivateKey(key)
        signature = pk.sign_recoverable(rawhash, hasher=None)
        if chain_id:
            v = safe_ord(signature[64:65]) + chain_id * 2 + EIP155_CHAIN_ID_OFFSET
        else:
            v = safe_ord(signature[64]) + V_OFFSET
        r = bytes_to_int(signature[0:32])
        s = bytes_to_int(signature[32:64])
    else:
        v, r, s = ecdsa_raw_sign(rawhash, key)
    return v, r, s

def safe_ord(value):
    if isinstance(value, int):
        return value
    else:
        return ord(value)


def create_transaction(nonce, gasprice, gaslimit, to_address, value, data, private_key, chain_id=None):
    tx = [int(nonce), int(gasprice), int(gaslimit), to_address, int(value), data]
    if chain_id:
        rawhash = sha3.keccak_256(rlp.encode(tx + [int_to_bytes(chain_id), b'', b''])).digest()
    else:
        rawhash = sha3.keccak_256(rlp.encode(tx)).digest()
    (v, r, s) = ecsign(rawhash, private_key, chain_id=chain_id)
    tx.append(v)
    tx.append(r)
    tx.append(s)
    tx_data = {"raw": "0x" + encode_hex(rlp.encode(tx)),
               "hash": "0x" + sha3.keccak_256(rlp.encode(tx)).hexdigest()}
    return tx_data

async def contract_method_encode(method):
    method=method.encode('utf-8')
    method="0x%s" %sha3.keccak_256(method).hexdigest()
    return method[0:10]


def create_contract(nonce, gasprice, gaslimit, data, private_key, chain_id=None):
    tx = [nonce, int(gasprice), int(gaslimit), 0, 0, data]
    if chain_id:
        rawhash = sha3.keccak_256(rlp.encode(tx + [int_to_big_endian(chain_id), b'', b''])).digest()
    else:
        rawhash = sha3.keccak_256(rlp.encode(tx)).digest()
    (v, r, s) = ecsign(rawhash, private_key, chain_id=chain_id)
    tx.append(v)
    tx.append(r)
    tx.append(s)
    tx_data = {"raw": "0x" + encode_hex(rlp.encode(tx)),
               "hash": "0x" + sha3.keccak_256(rlp.encode(tx)).hexdigest()}
    return tx_data