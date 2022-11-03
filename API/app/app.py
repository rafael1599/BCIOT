from flask import Flask, Response, request, jsonify
import asyncio
import warnings
import time
from web3 import Web3 as w3
import json
import sys
import serial
sys.setrecursionlimit(5000)

warnings.filterwarnings("ignore", category=DeprecationWarning)

serialcom = serial.Serial('COM5', 9600)
serialcom.timeout = 1
# BC PUBLICA
infura_url = "https://sepolia.infura.io/v3/06fab9ba7d4840e4bda61a197b3f27df"
w3 = w3(w3.HTTPProvider(infura_url))
chainId = 11155111
account = "0xdc07AF52989E4ddA498918C9fa169d60134141f8"
nonce = w3.eth.getTransactionCount(account)
private_key = "6aa764ea368f0d774061518b15866c3453a4ade37171ac9f2561109b3bc4823b"

# BC PRIVADA
# infura_url = "https://sepolia.infura.io/v3/06fab9ba7d4840e4bda61a197b3f27df"
# w3 = w3(w3.HTTPProvider(infura_url))
# chainId = 11155111
# account = "0xdc07AF52989E4ddA498918C9fa169d60134141f8"
# nonce = w3.eth.getTransactionCount(account)
# private_key = "6aa764ea368f0d774061518b15866c3453a4ade37171ac9f2561109b3bc4823b"

app = Flask(__name__)

async def getNonce():
    return w3.eth.getTransactionCount(account)


async def signTransaction(transaccion):
    return w3.eth.account.sign_transaction(transaccion, private_key=private_key)


async def hashTransaction(signedTransaction):
    return w3.eth.send_raw_transaction(signedTransaction.rawTransaction)

base = "/api"

import errors.errors
import routes.routes

if __name__ == "__main__":
    app.run()

