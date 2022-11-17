from routes.bprivate.bprivate import app, time, base, json, jsonify, baseBlockchain, localhost, private_w3, private_chainId, private_account, private_nonce
baseLED = "/LED"

contractAddressLED = "0x025F226BDBc52aA60B2C32B8d028cdcb801A0F02"
contractAbiLED = json.loads(
    '[ 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_commandLED", 				"type": "string" 			} 		], 		"name": "enviarcommandLED", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "commandLED", 				"type": "string" 			} 		], 		"name": "manejarLED", 		"type": "event" 	}, 	{ 		"inputs": [], 		"name": "commandLED", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "getcommandLED", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	} ]'
)
contractLED = w3.eth.contract(address=contractAddressLED, abi=contractAbiLED)

async def buildTransactionLED(state, nonce):
    return contractLED.functions.enviarcommandLED(state).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chainId,
            "from": account,
            "nonce": nonce,
        }
    )

async def validateChangeCommand(state):
    command = contractLED.functions.getcommandLED().call()
    if state == command:
        return True
    else:
        await validateChangeCommand(state)

@app.route(base + baseBlockchain + baseLED + "/sendState/<state>", methods=["POST"])
async def sendStateLEDPrivate(state):
    res = {}
    # nonce = await getNonce()
    
    timeStart = time.time()
    
    transaccion = await buildTransactionLED(state, nonce)
    # signedTransaction = await signTransaction(transaccion)
    # hashedTransaction = await hashTransaction(signedTransaction)
    # print("################################################################")
    # print(signedTransaction)
    await validateChangeCommand(state)
    
    timeEnd = time.time()

    res["message"] = "command enviado satisfactoriamente!"
    res["status"] = 200
    res["data"] = {
        "success": True,
        "duration": timeEnd - timeStart
    }
    return jsonify(res), 200

@app.route(base + baseBlockchain + baseLED + "/getState")
async def getStateLEDPrivate():
    command = contractLED.functions.getcommandLED().call()
    print("Comando obtenido privada"+command)
    typeLight = "Apagado"
    if command == "Encender":
        typeLight = "Encendido"
    else:
        command = "Apagar"
        typeLight = "Apagado"

    res = {}
    res["message"] = "Valor de LED obtenido!"
    res["success"] = True
    res["status"] = 200
    res["data"] = {"command": command, "typeLight": typeLight}

    return jsonify(res)