import routes.bpublic.routesSML
import routes.bpublic.routesLOCK
import routes.bpublic.routesLED
from routes.routes import app, time, base, json, jsonify, psutil, serialcom
from web3 import Web3 as w3

baseBlockchain = '/Public'

# BC PUBLICA
infura_url = "https://sepolia.infura.io/v3/06fab9ba7d4840e4bda61a197b3f27df"
w3 = w3(w3.HTTPProvider(infura_url))
chainId = 11155111
account = "0xdc07AF52989E4ddA498918C9fa169d60134141f8"
nonce = w3.eth.getTransactionCount(account)
private_key = "6aa764ea368f0d774061518b15866c3453a4ade37171ac9f2561109b3bc4823b"


async def getNonce():
    return w3.eth.getTransactionCount(account)


async def signTransaction(transaccion):
    return w3.eth.account.sign_transaction(transaccion, private_key=private_key)


async def hashTransaction(signedTransaction):
    return w3.eth.send_raw_transaction(signedTransaction.rawTransaction)
