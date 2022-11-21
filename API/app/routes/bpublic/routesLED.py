from routes.bpublic.bpublic import app, time, base, json, w3, chainId, account, nonce, private_key, jsonify, getNonce, signTransaction, hashTransaction, baseBlockchain, psutil
baseLED = "/LED"

contractAddressLED = "0x181Ebcb99c15d23eC0670E6Afdd9EBc46eA855eA"
contractAbiLED = json.loads(
    '[ 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "commandLED", 				"type": "string" 			} 		], 		"name": "manejarLED", 		"type": "event" 	}, 	{ 		"inputs": [], 		"name": "commandLED", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_commandLED", 				"type": "string" 			} 		], 		"name": "enviarcommandLED", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "getcommandLED", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	} ]'
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
async def sendStateLEDPublic(state):
    res = {}
    nonce = await getNonce()
    
    timeStart = time.time()
    
    #Sacando el porcentaje init
    pcrData = psutil.virtual_memory()
    porcentaje1 = pcrData.percent
    print("=======================================================================")
    print("El porcentaje1 es: ",porcentaje1)
    #-----------------------------------------------------------------------------
    transaccion = await buildTransactionLED(state, nonce)
    signedTransaction = await signTransaction(transaccion)
    hashedTransaction = await hashTransaction(signedTransaction)
    #-----------------------------------------------------------------------------
    porcentaje2 = pcrData.percent
    print("=======================================================================")
    print("El porcentaje2 es: ",porcentaje2)
    promPercent = (porcentaje1+porcentaje2)/2
    print("=======================================================================")
    print("El porcentaje promedio es: ",promPercent)
    #Sacando el porcentaje end
    print("################################################################")
    print(signedTransaction)
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
async def getStateLEDPublic():
    command = contractLED.functions.getcommandLED().call()
    print("Comando obtenido publica"+command)
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