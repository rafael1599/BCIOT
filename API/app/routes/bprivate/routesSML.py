from routes.bprivate.bprivate import app, time, base, json, jsonify, localhost, private_w3, private_chainId, private_account, private_nonce, getNoncePrivate, signTransactionPrivate, hashTransactionPrivate, baseBlockchain, serialcom, psutil

baseSML = "/smartLight"

contractAddressSML = "0x59488D5d49d5f00270E15F184566893Ef2bF0457"
contractAbiSML = json.loads(
    '[ 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "commandSML", 				"type": "string" 			} 		], 		"name": "manejarSML", 		"type": "event" 	}, 	{ 		"inputs": [], 		"name": "commandSML", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_commandSML", 				"type": "string" 			} 		], 		"name": "enviarcommandSML", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "getcommandSML", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	} ]'
)
contractSML = private_w3.eth.contract(address=contractAddressSML, abi=contractAbiSML)

async def buildTransactionSML(state, nonce):
    return contractSML.functions.enviarcommandSML(state).buildTransaction(
        {
            "gasPrice": private_w3.eth.gas_price,
            "chainId": private_chainId,
            "from": private_account,
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
async def sendStateSMLPrivate(state):
    res = {}
    
    nonce = await getNoncePrivate()
    
    timeStart = time.time()
    
    #Sacando el porcentaje init
    pcrData = psutil.virtual_memory()
    porcentaje1 = pcrData.percent
    print("=======================================================================")
    print("El porcentaje1 es: ",porcentaje1)
    #-----------------------------------------------------------------------------
    transaccion = await buildTransactionSML(state, nonce)
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

    if state == 'Apagar':
        smlOff()
    if state != 'Apagar':
        smlColor(state)
    if state == '':
        disconnect()

    res["message"] = "command enviado satisfactoriamente!"
    res["status"] = 200
    res["data"] = {
        "success": True,
        "duration": timeEnd - timeStart
    }

    return jsonify(res)

@app.route(base + baseBlockchain + baseSML + "/getState")
async def getStateSMLPrivate():
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