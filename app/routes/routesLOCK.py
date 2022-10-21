from __main__ import app, time, base, json, w3, chainId, account, nonce, private_key, serialcom, jsonify, getNonce, signTransaction, hashTransaction
import string

baseLock = "/smartLock"
contractAddressLOCK = "0x4D6CC2C750A8213E4e702231a525e44d2Ac0abc8"
contractAbiLOCK = json.loads(
        '[{"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "comandoLock","type": "string"}],"name": "manejarLock","type": "event"},{"inputs": [],"name": "comandoLock","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "string","name": "_comandoLock","type": "string"}],"name": "enviarComandoLock","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "getComandoLock","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"} ]'
    )
contractLock = w3.eth.contract(address=contractAddressLOCK, abi=contractAbiLOCK)

async def buildTransactionLOCK(state, nonce):
    return contractLock.functions.enviarComandoLOCK(state).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chainId,
            "from": account,
            "nonce": nonce,
        }
    )

open = "0:10:0"
close = "10:0:0"
ledOff = "0:0:0"

def LockOpen():
    serialcom.write(str(open).encode())
    
def lockClose():
	serialcom.write(str(close).encode())

#pasar a modo hibernacion, HM: Hibernation mode
def lockHM():
    serialcom.write(str(ledOff).encode())

def disconnect():
	serialcom.close()

############################################################## ESTUDIAR #
async def validateChangeCommand(state):
    command = contractLock.functions.getComandoLock().call()
    if state == command:
        return True
    else:
        await validateChangeCommand(state)


@app.route(base + baseLock + "/sendState/<state>", methods=["POST"])

async def sendStateLock(state):
    nonce = await getNonce()
    
    timeStart = time.time()
    
    transaccion = await buildTransactionLOCK(state, nonce)
    signedTransaction = await signTransaction(transaccion)
    hashedTransaction = await hashTransaction(signedTransaction)
    await validateChangeCommand(state)
    
    timeEnd = time.time()

    if state == open:
        LockOpen()

    if state == close:
        lockClose()

    # Hibernation mode
    if state == ledOff:
        lockHM()

    if state == '':
        disconnect()

    res = {}

    res["message"] = "Comando enviado satisfactoriamente!"
    res["status"] = 200
    res["data"] = {
        "success": True,
        "duration": timeEnd - timeStart
    }

    return jsonify(res)

@app.route(base + baseLock + "/getState")
async def getStateLOCK():
    command = contractLock.functions.getComandoLOCK().call()
    typeLight = "Cerradura bloqueada"
    if command == close:
        typeLight = "Cerradura bloqueada"
    elif command == open:
        typeLight = "Cerradura desbloqueada"
    elif command == ledOff:
        typeLight = "Cerradura en modo hibernación"
    else:
        typeLight = "Error al intentar ejecutar el comando"
        print("El LOCK no puede realizar esta peticion")

    res = {}
    res["message"] = "Valor de LOCK obtenido!"
    res["success"] = True
    res["status"] = 200
    res["data"] = {"comando": command, "typeLight": typeLight}

    return jsonify(res)