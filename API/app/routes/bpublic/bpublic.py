from routes.routes import app, time, base, json, w3, chainId, account, nonce, private_key, jsonify

baseBlockchain = '/Public'

async def getNonce():
    return w3.eth.getTransactionCount(account)


async def signTransaction(transaccion):
    return w3.eth.account.sign_transaction(transaccion, private_key=private_key)


async def hashTransaction(signedTransaction):
    return w3.eth.send_raw_transaction(signedTransaction.rawTransaction)

import routes.bpublic.routesLED
import routes.bpublic.routesLOCK
import routes.bpublic.routesSML