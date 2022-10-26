from routes import app, time, base, json, w3, chainId, account, nonce, private_key, serialcom, jsonify, getNonce, signTransaction, hashTransaction

baseSML = "/smartLight"

contractAddressSML = "0xBbb2685eEAd6699Cfdc804578305B530d9a69EF1"
contractAbiSML = json.loads(
    '[ {"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "comandoSML","type": "string"}],"name": "manejarSML","type": "event" }, {"inputs": [],"name": "comandoSML","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function" }, {"inputs": [{"internalType": "string","name": "_comandoSML","type": "string"}],"name": "enviarComandoSML","outputs": [],"stateMutability": "nonpayable","type": "function" }, {"inputs": [],"name": "getComandoSML","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function" } ]'
)
contractSML = w3.eth.contract(address=contractAddressSML, abi=contractAbiSML)

async def buildTransactionSML(state, nonce):
    return contractSML.functions.enviarComandoSML(state).buildTransaction(
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
    command = contractSML.functions.getComandoSML().call()
    if state == command:
        return True
    else:
        await validateChangeCommand(state)

@app.route(base + baseSML + "/sendState/<state>", methods=["POST"])
async def sendStateSML(state):
    nonce = await getNonce()
    
    timeStart = time.time()
    
    transaccion = await buildTransactionSML(state, nonce)
    signedTransaction = await signTransaction(transaccion)
    hashedTransaction = await hashTransaction(signedTransaction)
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

    res = {}

    res["message"] = "Comando enviado satisfactoriamente!"
    res["status"] = 200
    res["data"] = {
        "success": True,
        "duration": timeEnd - timeStart
    }

    return jsonify(res)

@app.route(base + baseSML + "/getState")
async def getStateSML():
    command = contractSML.functions.getComandoSML().call()
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