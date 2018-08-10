import coincurve
import rlp
import sha3
from py_ecc.secp256k1 import ecdsa_raw_sign

from pyeth.encode import *
from pyeth.tools import *


def ecsign(rawhash, key):
    if coincurve and hasattr(coincurve, 'PrivateKey'):
        pk = coincurve.PrivateKey(key)
        signature = pk.sign_recoverable(rawhash, hasher=None)
        v = safe_ord(signature[64]) + 27
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

def create_transaction(nonce, gasprice, gaslimit, to_address, value, data, private_key):
    gaslimit = int(gaslimit)
    gasprice = int(gasprice)
    value = int(value)
    nonce=int(nonce)
    tx = [nonce, gasprice, gaslimit, to_address, value, data]
    rawhash = sha3.keccak_256(rlp.encode(tx)).digest()
    (v, r, s) = ecsign(rawhash, private_key)
    tx.append(v)
    tx.append(r)
    tx.append(s)
    hash = "0x" + sha3.keccak_256(rlp.encode(tx)).hexdigest()
    raw_tx = "0x" + encode_hex(rlp.encode(tx))
    tx_data = {"raw": raw_tx, "hash": hash}
    return tx_data

async def contract_method_encode(method):
    method=method.encode('utf-8')
    method="0x%s" %sha3.keccak_256(method).hexdigest()
    return method[0:10]


def create_contract(nonce, gasprice, gaslimit, data, private_key):
    gaslimit = int(gaslimit)
    gasprice = int(gasprice)
    to=0
    value= 0
    tx = [nonce, gasprice, gaslimit,to,value, data]
    rawhash = sha3.keccak_256(rlp.encode(tx)).digest()
    (v, r, s) = ecsign(rawhash, private_key)
    tx.append(v)
    tx.append(r)
    tx.append(s)
    hash = "0x" + sha3.keccak_256(rlp.encode(tx)).hexdigest()
    raw_tx = "0x" + encode_hex(rlp.encode(tx))
    tx_data = {"raw": raw_tx, "hash": hash}
    return tx_data