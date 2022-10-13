import json
from flask import Flask, jsonify
from flask_cors import CORS
from web3 import Web3 as w3
import asyncio

infura_url = "https://goerli.infura.io/v3/f1ee978b04d04b4e8bb83d51b731c973"
web3 = w3(w3.HTTPProvider(infura_url))
chainId = 5

account = "0xc8f39fC331f0799F655490Bb7dc2D0d484018Bc0"
private_key = "abff363e849b97ba975265f8d28eafb56f0851011fcd37b211c78f0febd0b55a"

# Direccion del contrato y su ABI
contratoDir = "0x20407b46FbB470857bA10267E6A56A6d035aD2DD"
contractABI = json.loads(
    '[ 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "comando", 				"type": "string" 			} 		], 		"name": "manejarLED", 		"type": "event" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_comando", 				"type": "string" 			} 		], 		"name": "enviarComando", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	} ]'
)
contrato = web3.eth.contract(address=contratoDir, abi=contractABI)

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})


async def buildTransaction(state, nonce):
    return contrato.functions.enviarComando(state).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            "chainId": chainId,
            "from": account,
            "nonce": nonce,
        }
    )


async def signTransaction(transaccion):
    return web3.eth.account.sign_transaction(transaccion, private_key=private_key)


async def hashTransaction(signedTransaction):
    return web3.eth.send_raw_transaction(signedTransaction.rawTransaction)


async def getNonce():
    return web3.eth.getTransactionCount(account)


@app.route("/sendState/<state>", methods=["POST"])
async def sendState(state):
    # Esperar que la transaccion se mine
    nonce = await getNonce()
    transaccion = await buildTransaction(state, nonce)
    signedTransaction = await signTransaction(transaccion)
    print(signedTransaction)
    print("\n")
    hashedTransaction = await hashTransaction(signedTransaction)
    print(hashedTransaction)
    res = {}

    res["message"] = "API - /sendState - Ejecutada satisfactoriamente!"
    res["status"] = 200
    res["data"] = {}

    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
