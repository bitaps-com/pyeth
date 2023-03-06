import coincurve
import rlp
import sha3

from rlp.sedes import CountableList
from .encode import *
from .tools import *

EIP155_CHAIN_ID_OFFSET = 35
V_OFFSET = 27
DYNAMIC_FEE_TRANSACTION_TYPE = b'\x02'

def ecsign(rawhash, key):
    pk = coincurve.PrivateKey(key)
    signature = pk.sign_recoverable(rawhash, hasher=None)
    v = safe_ord(signature[64:])
    r = bytes_to_int(signature[0:32])
    s = bytes_to_int(signature[32:64])
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
    (v, r, s) = ecsign(rawhash, private_key)
    if chain_id:
        v = v + chain_id * 2 + EIP155_CHAIN_ID_OFFSET
    else:
        v = v + V_OFFSET
    tx.append(v)
    tx.append(r)
    tx.append(s)
    tx_data = {"raw": "0x" + encode_hex(rlp.encode(tx)),
               "hash": "0x" + sha3.keccak_256(rlp.encode(tx)).hexdigest()}
    return tx_data

def create_dynamic_fee_transaction(chain_id, nonce, max_priority_fee_per_gas, max_fee_per_gas, gaslimit, to_address, value, data,  access_list, private_key):
    tx = [int(chain_id), int(nonce), int(max_priority_fee_per_gas),int(max_fee_per_gas), int(gaslimit), to_address, int(value), data, access_list]
    rawhash = sha3.keccak_256(DYNAMIC_FEE_TRANSACTION_TYPE + rlp.encode(tx)).digest()
    (v, r, s) = ecsign(rawhash, private_key)
    tx.append(v)
    tx.append(r)
    tx.append(s)
    tx_data = {"raw": "0x" + encode_hex(DYNAMIC_FEE_TRANSACTION_TYPE + rlp.encode(tx)),
               "hash": "0x" + sha3.keccak_256(DYNAMIC_FEE_TRANSACTION_TYPE + rlp.encode(tx)).hexdigest()}
    return tx_data

async def contract_method_encode(method):
    method=method.encode('utf-8')
    method="0x%s" %sha3.keccak_256(method).hexdigest()
    return method[0:10]


def create_contract(nonce, gasprice, gaslimit, data, private_key, chain_id=None):
    return create_transaction(nonce, gasprice, gaslimit, 0, 0, data, private_key, chain_id=chain_id)