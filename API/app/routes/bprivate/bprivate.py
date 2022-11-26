from routes.routes import app, time, base, json, jsonify, serialcom, psutil
from web3 import Web3 as private_w3

baseBlockchain = '/Private'

# BC PRIVADA
localhost =  'http://127.0.0.1:8502'
private_w3 = private_w3(private_w3.HTTPProvider(localhost))
private_chainId = 1337
private_address = "0xdd1b5777d25a19bacf9d58a50445c7bed9cda232"
private_account = private_w3.toChecksumAddress(private_address)
private_nonce = private_w3.eth.getTransactionCount(private_account)
private_key = "864b1b31aa42750689194b53a99cdd64d1c49435ae0162671a14cf9b8baa4799"

async def getNoncePrivate():
    return private_w3.eth.getTransactionCount(private_account)

async def signTransactionPrivate(transaccion):
    return private_w3.eth.account.sign_transaction(transaccion, private_key=private_key)

async def hashTransactionPrivate(signedTransaction):
    return private_w3.eth.send_raw_transaction(signedTransaction.rawTransaction)

import routes.bprivate.routesLED
import routes.bprivate.routesLOCK
import routes.bprivate.routesSML