from routes.bprivate.bprivate import app, time, base, json, jsonify, localhost, private_w3, private_chainId, private_account, private_nonce, getNoncePrivate, signTransactionPrivate, hashTransactionPrivate, baseBlockchain, serialcom, psutil
baseLED = "/LED"

contractAddressLED = "0x23B81b7c5c0f1368f1Add8F21E066BCF72AD8670"
contractAbiLED = json.loads(
    '[ 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_commandLED", 				"type": "string" 			} 		], 		"name": "enviarcommandLED", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "commandLED", 				"type": "string" 			} 		], 		"name": "manejarLED", 		"type": "event" 	}, 	{ 		"inputs": [], 		"name": "commandLED", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "getcommandLED", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	} ]'
)
contractLED = private_w3.eth.contract(address=contractAddressLED, abi=contractAbiLED)

async def buildTransactionLED(state, nonce):
    return contractLED.functions.enviarcommandLED(state).buildTransaction(
        {
            "gasPrice": private_w3.eth.gas_price,
            "chainId": private_chainId,
            "from": private_account,
            "nonce": nonce,
        }
    )

def ledOn():
    serialcom.write(str('1').encode())
    
def ledOff():
	serialcom.write(str('0').encode())

def disconnect():
	serialcom.close()

async def validateChangeCommand(state):
    command = contractLED.functions.getcommandLED().call()
    if state == command:
        return True
    else:
        await validateChangeCommand(state)

@app.route(base + baseBlockchain + baseLED + "/sendState/<state>", methods=["POST"])
async def sendStateLEDPrivate(state):
    res = {}
    
    nonce = await getNoncePrivate()
    
    timeStart = time.time()
    #Sacando el porcentaje init
    pcrData = psutil.virtual_memory()
    porcentaje1 = pcrData.percent
    print("=======================================================================")
    print("El porcentaje1 es: ",porcentaje1)
    #-----------------------------------------------------------------------------
    transaccion = await buildTransactionLED(state, nonce)
    signedTransaction = await signTransactionPrivate(transaccion)
    hashedTransaction = await hashTransactionPrivate(signedTransaction)
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
    
    if state == 'Encender':
        ledOn()
    if state == 'Apagar':
        ledOff()
    if state == '':
        disconnect()

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