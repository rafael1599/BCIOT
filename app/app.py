from flask import Flask, Response, request, jsonify
import asyncio
import serial
import warnings
import time
from web3 import Web3 as w3
import json
import sys
sys.setrecursionlimit(5000)

warnings.filterwarnings("ignore", category=DeprecationWarning)

serialcom = serial.Serial('COM5', 9600)
# PONER COM COMO VARIABLE PARA HACERLO AUTOMATICO, SEGUN EL DISPOSITIVO (LED = COM3, CERRADURA = COM4, FOCO INTELIGENTE = COM5)
serialcom.timeout = 1

infura_url = "https://goerli.infura.io/v3/f1ee978b04d04b4e8bb83d51b731c973"
w3 = w3(w3.HTTPProvider(infura_url))
chainId = 5
account = "0xc8f39fC331f0799F655490Bb7dc2D0d484018Bc0"
nonce = w3.eth.getTransactionCount(account)
private_key = "abff363e849b97ba975265f8d28eafb56f0851011fcd37b211c78f0febd0b55a"

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
    app.run(debug=True)

