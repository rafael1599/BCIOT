import json
import asyncio
import serial as s  # para cominicarse con arduino
import warnings
from web3 import Web3 as w3

from flask import Flask, jsonify
from flask_cors import CORS

warnings.filterwarnings("ignore", category=DeprecationWarning)

# =========================
# VARIABLES COMUNES       ||
# =========================
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})
infura_url = "https://goerli.infura.io/v3/f1ee978b04d04b4e8bb83d51b731c973"
w3 = w3(w3.HTTPProvider(infura_url))
conexion = s.Serial("COM1", 9600)
actualEvent = ""
chainId = 5
account = "0xc8f39fC331f0799F655490Bb7dc2D0d484018Bc0"
nonce = w3.eth.getTransactionCount(account)
private_key = "abff363e849b97ba975265f8d28eafb56f0851011fcd37b211c78f0febd0b55a"
# _______________________________________________________________________________

# =================================================
# FUNCIONES PARA CONTROLAR LOS DISPOSITIVOS       ||
# =================================================
def enviar_comando(comando):
    comando = comando + "\r"
    print("Se esta enviando el comando <<" + comando + ">> al arduino")
    conexion.write(comando.encode())


# ========================================
# FUNCIONES PARA CREAR EL CONTRATO       ||
# ========================================
async def getNonce():
    return w3.eth.getTransactionCount(account)


async def signTransaction(transaccion):
    return w3.eth.account.sign_transaction(transaccion, private_key=private_key)


async def hashTransaction(signedTransaction):
    return w3.eth.send_raw_transaction(signedTransaction.rawTransaction)


# ______________________________________________________________________________


# ======================================================
# DEFINIENDO CLAVES PUBLICAS DE LOS CONTRATOS EN LA BC ||
# ======================================================

# contractAddressSML = "0x4D6CC2C750A8213E4e702231a525e44d2Ac0abc8"
contractAddressLED = "0x71B68430Bc65a43d6AcdFf61c444b060b29E5Ca6"
# contractAddressLOCK = "0x4D6CC2C750A8213E4e702231a525e44d2Ac0abc8"
# ___________________________________________________________________

# ================================
# DEFINIENDO EL ABI DEL CONTRATO ||
# ================================

# contractAbiSML = json.loads(
#     '[{"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "comandoLED","type": "string"}],"name": "manejarLED","type": "event"},{"inputs": [],"name": "comandoLED","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "string","name": "_comandoLED","type": "string"}],"name": "enviarComandoLED","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "getComandoLED","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"} ]'
# )
contractAbiLED = json.loads(
    '[{"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "comandoLED","type": "string"}],"name": "manejarLED","type": "event"},{"inputs": [],"name": "comandoLED","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "string","name": "_comandoLED","type": "string"}],"name": "enviarComandoLED","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "getComandoLED","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"} ]'
)
# contractAbiLOCK = json.loads(
#         '[{"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "comandoLock","type": "string"}],"name": "manejarLock","type": "event"},{"inputs": [],"name": "comandoLock","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "string","name": "_comandoLock","type": "string"}],"name": "enviarComandoLock","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "getComandoLock","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"} ]'
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
#     return contractSML.functions.enviarComandoSML(state).buildTransaction(
#         {
#             "gasPrice": w3.eth.gas_price,
#             "chainId": chainId,
#             "from": account,
#             "nonce": nonce,
#         }
#     )


async def buildTransactionLED(state, nonce):
    return contractLED.functions.enviarComandoLED(state).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chainId,
            "from": account,
            "nonce": nonce,
        }
    )


# async def buildTransactionLOCK(state, nonce):
#     return contractLOCK.functions.enviarComandoLOCK(state).buildTransaction(
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
#     orden = contractSML.functions.getComandoSML().call()
#     Apagar = "0:0:0"
#     if orden == colorElegido:
#         enviar_comando(orden)
#         typeLight = "Custom color"
#     elif orden == "Apagar":
#         enviar_comando(Apagar)
#     else:
#         print("El color elegido no existe")

#     res = {}
#     res["message"] = "Valor de SML obtenido!"
#     res["success"] = True
#     res["status"] = 200
#     res["orden"] = {"comando": orden, "typeLight": typeLight}

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

    #### PARA VER EL HASH CON EL QUE VEMOS LAS TRANSACCIONES EN EL ETHERSCAN ####
    print("#####################################################\n", signedTransaction)
    res = {}

    res["message"] = "API - /sendState - Ejecutada satisfactoriamente!"
    res["status"] = 200
    res["orden"] = {}

    return jsonify(res)


@app.route(base + baseLED + "/getState")
async def getStateLED():
    orden = contractLED.functions.getComandoLED().call()
    typeLight = "Encendido"
    if orden == "Apagar":
        enviar_comando(orden)
        typeLight = "Apagado"
    elif orden == "Encender":
        enviar_comando(orden)
        typeLight = "Encendido"
    else:
        typeLight = "Error al intentar ejecutar el comando"
        print("El LED no puede realizar esta peticion")

    res = {}
    res["message"] = "Valor de LED obtenido!"
    res["success"] = True
    res["status"] = 200
    res["orden"] = {"comando": orden, "typeLight": typeLight}

    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)