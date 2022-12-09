from routes.bpublic.bpublic import app, time, base, json, w3, chainId, account, nonce, private_key, jsonify, getNonce, signTransaction, hashTransaction, baseBlockchain, psutil, serialcom

baseSML = "/smartLight"

contractAddressSML = "0x59488D5d49d5f00270E15F184566893Ef2bF0457"
contractAbiSML = json.loads(
    '[ 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "commandSML", 				"type": "string" 			} 		], 		"name": "manejarSML", 		"type": "event" 	}, 	{ 		"inputs": [], 		"name": "commandSML", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_commandSML", 				"type": "string" 			} 		], 		"name": "enviarcommandSML", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "getcommandSML", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	} ]'
)
contractSML = w3.eth.contract(address=contractAddressSML, abi=contractAbiSML)
async def buildTransactionSML(state, nonce):
    return contractSML.functions.enviarcommandSML(state).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": chainId,
            "from": account,
            "nonce": nonce,
        }
    )

def smlColor(color):
    serialcom.write(str(color).encode())
    
def smlOff():
	serialcom.write(str('0:0:0').encode())

def disconnect():
	serialcom.close()

async def validateChangeCommand(state):
    command = contractSML.functions.getcommandSML().call()
    if state == command:
        return True
    else:
        await validateChangeCommand(state)

@app.route(base + baseBlockchain + baseSML + "/sendState/<state>", methods=["POST"])
async def sendStateSMLPublic(state):
    nonce = await getNonce()
    
    timeStart = time.time()
    #-----------------------------------------------------------------------------
    transaccion = await buildTransactionSML(state, nonce)
    signedTransaction = await signTransaction(transaccion)
    hashedTransaction = await hashTransaction(signedTransaction)
    #-----------------------------------------------------------------------------    
    timeEnd = time.time()
    #Sacando el porcentaje init
    pcrData = psutil.cpu_percent(interval=0.5)
    print("El porcentaje es: ",pcrData)
    #Sacando el porcentaje end
    print("################################################################")
    print(signedTransaction)
    await validateChangeCommand(state)

    if state == 'Apagar':
        smlOff()
    if state != 'Apagar':
        smlColor(state)
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

@app.route(base + baseBlockchain + baseSML + "/getState")
async def getStateSMLPublic():
    command = contractSML.functions.getcommandSML().call()
    typeLight = "Apagado"
    if command == "Apagar":
        typeLight = "Apagado"
    else:
        typeLight = "Encendido"

    res = {}
    res["message"] = "Valor de SML obtenido!"
    res["success"] = True
    res["status"] = 200
    res["data"] = {"command": command, "typeLight": typeLight}

    return jsonify(res)