from routes.routes import app, time, base, json, jsonify, localhost, private_w3, private_chainId, private_account, private_nonce

baseBlockchain = '/Private'

async def getNoncePrivate():
    return private_w3.eth.getTransactionCount(private_account)

import routes.bprivate.routesLED
import routes.bprivate.routesLOCK
import routes.bprivate.routesSML