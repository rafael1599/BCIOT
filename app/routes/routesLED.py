from routes.routes import app, time, base, json, w3, chainId, account, nonce, private_key, serialcom, jsonify, getNonce, signTransaction, hashTransaction

baseLED = "/LED"

contractAddressLED = "0x4c79072Fb97c479C580004A090271494bcE6dD71"
contractAbiLED = json.loads(
    '[ 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "comandoLED", 				"type": "string" 			} 		], 		"name": "manejarLED", 		"type": "event" 	}, 	{ 		"inputs": [], 		"name": "comandoLED", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_comandoLED", 				"type": "string" 			} 		], 		"name": "enviarComandoLED", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "getComandoLED", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	} ]'
)
contractLED = w3.eth.contract(address=contractAddressLED, abi=contractAbiLED)

async def buildTransactionLED(state, nonce):
    return contractLED.functions.enviarComandoLED(state).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chainId,
            "from": account,
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
    command = contractLED.functions.getComandoLED().call()
    if state == command:
        return True
    else:
        await validateChangeCommand(state)

@app.route(base + baseLED + "/sendState/<state>", methods=["POST"])
async def sendStateLED(state):
    res = {}
    nonce = await getNonce()
    
    timeStart = time.time()
    
    transaccion = await buildTransactionLED(state, nonce)
    signedTransaction = await signTransaction(transaccion)
    hashedTransaction = await hashTransaction(signedTransaction)
    print(signedTransaction)
    await validateChangeCommand(state)
    
    
    timeEnd = time.time()

    if state == 'Encender':
        print(signedTransaction)
        ledOn()
    if state == 'Apagar':
        ledOff()
    if state == '':
        disconnect()

    res["message"] = "Comando enviado satisfactoriamente!"
    res["status"] = 200
    res["data"] = {
        "success": True,
        "duration": timeEnd - timeStart
    }
    return jsonify(res), 200

@app.route(base + baseLED + "/getState")
async def getStateLED():
    command = contractLED.functions.getComandoLED().call()
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