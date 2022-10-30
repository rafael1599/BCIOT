import json
import asyncio
import serial
import warnings
import time
from web3 import Web3 as w3

from flask import Flask, jsonify

warnings.filterwarnings("ignore", category=DeprecationWarning)

# =========================
# VARIABLES COMUNES       ||
# =========================
infura_url = "https://goerli.infura.io/v3/f1ee978b04d04b4e8bb83d51b731c973"
w3 = w3(w3.HTTPProvider(infura_url))
actualEvent = ""
chainId = 5
account = "0xc8f39fC331f0799F655490Bb7dc2D0d484018Bc0"
nonce = w3.eth.getTransactionCount(account)
private_key = "abff363e849b97ba975265f8d28eafb56f0851011fcd37b211c78f0febd0b55a"

# ARDUINO
serialcom = serial.Serial('COM3', 9600)
serialcom.timeout = 1

app = Flask(__name__)
# _______________________________________________________________________________

# =================================================
# FUNCIONES PARA CONTROLAR LOS DISPOSITIVOS       ||
# =================================================
def enviar_command(command):
    command = command + "\r"
    print("Se esta enviando el command <<" + command + ">> al arduino")
    serialcom.write(command.encode())


# ========================================
# FUNCIONES PARA CREAR EL CONTRATO       ||
# ========================================
async def getNonce():
    return w3.eth.getTransactionCount(account)


async def signTransaction(transaccion):
    return w3.eth.account.sign_transaction(transaccion, private_key=private_key)


async def hashTransaction(signedTransaction):
    return w3.eth.send_raw_transaction(signedTransaction.rawTransaction)

def disconnect():
	serialcom.close()

# ______________________________________________________________________________


# ======================================================
# DEFINIENDO CLAVES PUBLICAS DE LOS CONTRATOS EN LA BC ||
# ======================================================

# contractAddressSML = "0x4D6CC2C750A8213E4e702231a525e44d2Ac0abc8"
contractAddressLED = "0x4c79072Fb97c479C580004A090271494bcE6dD71"
# contractAddressLOCK = "0x4D6CC2C750A8213E4e702231a525e44d2Ac0abc8"
# ___________________________________________________________________

# ================================
# DEFINIENDO EL ABI DEL CONTRATO ||
# ================================

# contractAbiSML = json.loads(
#     '[{"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "commandLED","type": "string"}],"name": "manejarLED","type": "event"},{"inputs": [],"name": "commandLED","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "string","name": "_commandLED","type": "string"}],"name": "enviarcommandLED","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "getcommandLED","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"} ]'
# )
contractAbiLED = json.loads(
    '[ 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "commandLED", 				"type": "string" 			} 		], 		"name": "manejarLED", 		"type": "event" 	}, 	{ 		"inputs": [], 		"name": "commandLED", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_commandLED", 				"type": "string" 			} 		], 		"name": "enviarcommandLED", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "getcommandLED", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	} ]'
)
# contractAbiLOCK = json.loads(
#         '[{"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "commandLock","type": "string"}],"name": "manejarLock","type": "event"},{"inputs": [],"name": "commandLock","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "string","name": "_commandLock","type": "string"}],"name": "enviarcommandLock","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "getcommandLock","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"} ]'
#     )
# __________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

# =========================
# OBTENIENDO LOS CONTRATOS ||
# =========================

# contractLOCK = w3.eth.contract(address=contractAddressLOCK, abi=contractAbiLOCK)
contractLED = w3.eth.contract(address=contractAddressLED, abi=contractAbiLED)
# contractSML = w3.eth.contract(address=contractAddressSML, abi=contractAbiSML)
# _____________________________________________________________________________________

# ========================
# CREANDO TRANSACCIONES ||
# ========================

# async def buildTransactionSML(state, nonce):
#     return contractSML.functions.enviarcommandSML(state).buildTransaction(
#         {
#             "gasPrice": w3.eth.gas_price,
#             "chainId": chainId,
#             "from": account,
#             "nonce": nonce,
#         }
#     )


async def buildTransactionLED(state, nonce):
    return contractLED.functions.enviarcommandLED(state).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chainId,
            "from": account,
            "nonce": nonce,
        }
    )


# async def buildTransactionLOCK(state, nonce):
#     return contractLOCK.functions.enviarcommandLOCK(state).buildTransaction(
#         {
#             "gasPrice": w3.eth.gas_price,
#             "chainId": chainId,
#             "from": account,
#             "nonce": nonce,
#         }
#     )
# ________________________________________________________________________________

# =======
# BASES ||
# =======

base = "/api"
# baseSML = "/SML"
baseLED = "/LED"
# baseSmartLock = "/smartLock"
# _____________________________

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# **************************************************** #
# **************************************************** #
# **************************************************** #
# *********************SML**************************** #
# **************************************************** #
# **************************************************** #
# **************************************************** #


# @app.route(base + baseSML + "/sendState/<state>", methods=["POST"])
# async def sendStateSML(state):
#     # Esperar que la transaccion se mine
#     nonce = await getNonce()
#     transaccion = await buildTransactionSML(state, nonce)
#     signedTransaction = await signTransaction(transaccion)
#     hashedTransaction = await hashTransaction(signedTransaction)
#     res = {}

#     res["message"] = "API - /sendState - Ejecutada satisfactoriamente!"
#     res["status"] = 200
#     res["orden"] = {}

#     return jsonify(res)


# @app.route(base + baseSML + "/getState")
# async def getStateSML():
#     orden = contractSML.functions.getcommandSML().call()
#     Apagar = "0:0:0"
#     if orden == colorElegido:
#         enviar_command(orden)
#         typeLight = "Custom color"
#     elif orden == "Apagar":
#         enviar_command(Apagar)
#     else:
#         print("<<ERROR GRAVE>> El color elegido no existe")
#         disconnect()

#     res = {}
#     res["message"] = "Valor de SML obtenido!"
#     res["success"] = True
#     res["status"] = 200
#     res["orden"] = {"command": orden, "typeLight": typeLight}

#     return jsonify(res)
# _____________________________________________________________________


# **************************************************** #
# **************************************************** #
# **************************************************** #
# *********************LED**************************** #
# **************************************************** #
# **************************************************** #
# **************************************************** #
@app.route(base + baseLED + "/sendState/<state>", methods=["POST"])
async def sendStateLED(state):
    # Esperar que la transaccion se mine
    nonce = await getNonce()
    transaccion = await buildTransactionLED(state, nonce)
    signedTransaction = await signTransaction(transaccion)
    hashedTransaction = await hashTransaction(signedTransaction)
    await enviar_command(state)

    #### PARA VER EL HASH CON EL QUE VEMOS LAS TRANSACCIONES EN EL ETHERSCAN ####
    print("#####################################################\n", signedTransaction)
    res = {}

    res["message"] = "command enviado satisfactoriamente!"
    res["status"] = 200
    res["data"] = {
        "hashedTransaction": hashedTransaction
    }
    if state == '':
        disconnect()

    return jsonify(res)


@app.route(base + baseLED + "/getState")
async def getStateLED():
    command = contractLED.functions.getcommandLED().call()
    typeLight = "Encendido"
    if command == "Apagar":
        typeLight = "Apagado"
    elif command == "Encender":
        typeLight = "Encendido"
    else:
        typeLight = "Error al intentar ejecutar el command"
        print("El LED no puede realizar esta peticion")

    res = {}
    res["message"] = "Valor de LED obtenido!"
    res["success"] = True
    res["status"] = 200
    res["data"] = {"command": command, "typeLight": typeLight}

    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)