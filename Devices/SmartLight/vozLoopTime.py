# Esta version esta intacta, deberia funcionar con el archivo LED_Block
# que tiene como comandos de entrada palabras, NO NUMEROS.

import json
import speech_recognition as sr
import pyttsx3
from web3 import Web3 as w3

# Informacion de la conexion a BC
infura_url = "https://goerli.infura.io/v3/f1ee978b04d04b4e8bb83d51b731c973"
web3 = w3(w3.HTTPProvider(infura_url))
chainId = 5

account = "0xc8f39fC331f0799F655490Bb7dc2D0d484018Bc0"
private_key = "abff363e849b97ba975265f8d28eafb56f0851011fcd37b211c78f0febd0b55a"

# Direccion del contrato y su ABI
contratoDir = "0x5b2f3a01031b5AcB1fE60Aa1EF1a73a6457cd5E7"
contractABI = json.loads(
    '[ 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "comando", 				"type": "string" 			} 		], 		"name": "manejarLED", 		"type": "event" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_comando", 				"type": "string" 			} 		], 		"name": "enviarComando", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	} ]'
)

contrato = web3.eth.contract(address=contratoDir, abi=contractABI)

nonce = web3.eth.getTransactionCount(account)

comando = ""


def enviarEstado(estado):
    # Esperar que la transaccion se mine
    transaccion = contrato.functions.enviarComando(estado).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            "chainId": chainId,
            "from": account,
            "nonce": nonce,
        }
    )
    transaccionFirmada = web3.eth.account.sign_transaction(
        transaccion, private_key=private_key
    )
    print(transaccionFirmada)
    print("\n")
    transaction_hash = web3.eth.send_raw_transaction(transaccionFirmada.rawTransaction)
    print(transaction_hash)

    # transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)


name = "Jarvis"
listener = sr.Recognizer()
engine = pyttsx3.init()

# Esta funcion pasa el audio a String
def speak(msg):
    engine = pyttsx3.init("sapi5")
    engine.setProperty("volume", 1.0)
    engine.setProperty("rate", 200)
    engine.setProperty("voz", "españa")
    print("MarioVoice: " + msg)
    engine.say(msg)
    engine.runAndWait()


# Función responsable de escuchar y reconocer el habla.
def listen():
    # Habilita el microfono para oir al usuario
    try:
        with sr.Microphone as recurso:
            print("Jarvis está escuchando ...")
        # Funcion de speech_recognition para eliminar el ruido
        listener.adjust_for_ambient_noise(recurso)
        # Almacene la información de audio en la variable pc
        pc = listener.listen(recurso)
        maria = listener.recognize_google(pc, language="es")
        maria = rec.lower()
        if name in rec:
            rec = rec.replace(name, "")

        # Si no reconoció el patrón de voz, muestra este mensaje que no entendió
    except sr.UnknownValueError:
        print("No entendí")
    return maria


def run_María():
    while True:
        maria = listen()
        if "maria" in maria:
            speak("What is your command?: ")


if __name__ == "_main_":
    run_María()
listen()
