from routes.bpublic.bpublic import app, time, base, json, w3, chainId, account, nonce, private_key, jsonify, getNonce, signTransaction, hashTransaction, baseBlockchain, psutil, serialcom

baseLock = "/smartLock"

# BC PUBLICA
publicContractLOCK = "0x76508615457ceE3bb2EA93aE01bCF7C13EC16Af9"
publicAbiLock = json.loads(
    '[ 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "commandLOCK", 				"type": "string" 			} 		], 		"name": "manejarLOCK", 		"type": "event" 	}, 	{ 		"inputs": [], 		"name": "commandLOCK", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_commandLOCK", 				"type": "string" 			} 		], 		"name": "enviarcommandLOCK", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "getcommandLOCK", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	} ]'
)
contractLock = w3.eth.contract(address=publicContractLOCK, abi=publicAbiLock)


async def buildTransactionLOCK(state, nonce):
    return contractLock.functions.enviarcommandLOCK(state).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chainId,
            "from": account,
            "nonce": nonce,
        }
    )


def LockOpen():
    serialcom.write(str('0:10:0').encode())


def lockClose():
    serialcom.write(str('10:0:0').encode())


def disconnect():
    serialcom.close()


async def validateChangeCommand(state):
    command = contractLock.functions.getcommandLOCK().call()
    if state == command:
        return True
    else:
        await validateChangeCommand(state)


@app.route(base + baseBlockchain + baseLock + "/sendState/<state>", methods=["POST"])
async def sendStateLockPublic(state):
    nonce = await getNonce()

    timeStart = time.time()
    # -----------------------------------------------------------------------------
    transaccion = await buildTransactionLOCK(state, nonce)
    signedTransaction = await signTransaction(transaccion)
    hashedTransaction = await hashTransaction(signedTransaction)
    # -----------------------------------------------------------------------------
    timeEnd = time.time()
    # Sacando el porcentaje init
    pcrData = psutil.cpu_percent(interval=0.5)
    print("El porcentaje es: ", pcrData)
    # Sacando el porcentaje end
    print("################################################################")
    print(signedTransaction)
    await validateChangeCommand(state)

    if state == "open":
        LockOpen()

    if state == "close":
        lockClose()

    if state == '':
        disconnect()

    res = {}

    res["message"] = "command enviado satisfactoriamente!"
    res["status"] = 200
    res["data"] = {
        "success": True,
        "duration": timeEnd - timeStart,
        "pcr": pcrData
    }

    return jsonify(res)


@app.route(base + baseBlockchain + baseLock + "/getState")
async def getStateLOCKPublic():
    command = contractLock.functions.getcommandLOCK().call()
    print("Comando obtenido publica"+command)
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
