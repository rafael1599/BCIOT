from routes.routes import app, time, base, json, jsonify
from web3 import Web3 as private_w3

baseBlockchain = '/Private'

# BC PRIVADA
localhost =  'http://127.0.0.1:8502'
private_w3 = private_w3(private_w3.HTTPProvider(localhost))
private_chainId = 1337
private_address = "0x3442e2f6447be971cab4d4fd5f820d14a14c3ef9"
private_account = private_w3.toChecksumAddress(private_address)
private_nonce = private_w3.eth.getTransactionCount(private_account)
private_key = "52d04451994c912795b149b29492210f52c8ceadff898dcc0bdf0c76ea0aac07"

async def getNoncePrivate():
    return private_w3.eth.getTransactionCount(private_account)

async def signTransactionPrivate(transaccion):
    return private_w3.eth.account.sign_transaction(transaccion, private_key=private_key)

async def hashTransactionPrivate(signedTransaction):
    return private_w3.eth.send_raw_transaction(signedTransaction.rawTransaction)

import routes.bprivate.routesLED
import routes.bprivate.routesLOCK
import routes.bprivate.routesSML