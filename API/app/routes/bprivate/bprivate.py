import routes.bprivate.routesSML
import routes.bprivate.routesLOCK
import routes.bprivate.routesLED
from routes.routes import app, time, base, json, jsonify, psutil, serialcom
from web3 import Web3 as private_w3

baseBlockchain = '/Private'

# BC PRIVADA
localhost = 'http://localhost:8545'
private_w3 = private_w3(private_w3.HTTPProvider(localhost))
private_chainId = 1337
private_address = "0xb27aa5bf2e19e5b3660de782403bbc2c2d020cd9"
private_account = private_w3.toChecksumAddress(private_address)
private_nonce = private_w3.eth.getTransactionCount(private_account)
private_key = "72e5a8374030ccbec31fccd59e39f7beb53221fa4125508fc35558018ba62416"


async def getNoncePrivate():
    return private_w3.eth.getTransactionCount(private_account)


async def signTransactionPrivate(transaccion):
    return private_w3.eth.account.sign_transaction(transaccion, private_key=private_key)


async def hashTransactionPrivate(signedTransaction):
    return private_w3.eth.send_raw_transaction(signedTransaction.rawTransaction)
