from __main__ import app, time, base, json, w3, chainId, account, nonce, private_key, serialcom, jsonify, getNonce, signTransaction, hashTransaction

baseLock = "/smartLock"

contractAddressLOCK = "0x564154eF75B7833d5DA2B08E9344591a944a0c8E"
contractAbiLOCK = json.loads(
        '[ 	{"anonymous": false,"inputs": [	{"indexed": false,"internalType": "string","name": "comandoLOCK","type": "string"	}],"name": "manejarLOCK","type": "event" 	}, 	{"inputs": [],"name": "comandoLOCK","outputs": [	{"internalType": "string","name": "","type": "string"	}],"stateMutability": "view","type": "function" 	}, 	{"inputs": [	{"internalType": "string","name": "_comandoLOCK","type": "string"	}],"name": "enviarComandoLOCK","outputs": [],"stateMutability": "nonpayable","type": "function" 	}, 	{"inputs": [],"name": "getComandoLOCK","outputs": [	{"internalType": "string","name": "","type": "string"	}],"stateMutability": "view","type": "function" 	} ]'
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

def LockOpen():
    serialcom.write(str('1').encode())
    
def lockClose():
	serialcom.write(str('0').encode())

def disconnect():
	serialcom.close()

############################################################## ESTUDIAR #
async def validateChangeCommand(state):
    command = contractLock.functions.getComandoLOCK().call()
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
    print("signedTransaction", signedTransaction)
    hashedTransaction = await hashTransaction(signedTransaction)
    await validateChangeCommand(state)
    
    timeEnd = time.time()

    if state == "open":
        LockOpen()

    if state == "close":
        lockClose()

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
    typeLock = "Cerradura bloqueada"
    if command == "open":
        typeLock = "Cerradura desbloqueada"
    else:
        command = "close"
        typeLock = "Cerradura bloqueada"

    res = {}
    res["message"] = "Valor de LOCK obtenido!"
    res["success"] = True
    res["status"] = 200
    res["data"] = {"command": command, "typeLock": typeLock}

    return jsonify(res)