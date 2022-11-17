from flask import Flask, Response, request, jsonify
import asyncio
import warnings
import time
from web3 import Web3 as w3
import json
import sys
sys.setrecursionlimit(5000)

warnings.filterwarnings("ignore", category=DeprecationWarning)
# BC PUBLICA
infura_url = "https://sepolia.infura.io/v3/06fab9ba7d4840e4bda61a197b3f27df"
w3 = w3(w3.HTTPProvider(infura_url))
chainId = 11155111
account = "0xdc07AF52989E4ddA498918C9fa169d60134141f8"
nonce = w3.eth.getTransactionCount(account)
private_key = "6aa764ea368f0d774061518b15866c3453a4ade37171ac9f2561109b3bc4823b"

# BC PRIVADA
localhost =  'http://127.0.0.1:8545'
w3 = w3(w3.HTTPProvider(localhost))
private_chainId = 1337
# account = "0xdc07AF52989E4ddA498918C9fa169d60134141f8"
# nonce = w3.eth.getTransactionCount(account)
# private_key = "6aa764ea368f0d774061518b15866c3453a4ade37171ac9f2561109b3bc4823b"

app = Flask(__name__)

base = "/api"

import errors.errors
import routes.routes

if __name__ == "__main__":
    app.run()

