# Esta version esta intacta, deberia funcionar con el archivo LED_Block
# que tiene como comandos de entrada palabras, NO NUMEROS.

import json
import speech_recognition as sr
import pyttsx3
from web3 import Web3 as w3

# Informacion de la conexion a BC
infura_url = "https://goerli.infura.io/v3/f1ee978b04d04b4e8bb83d51b731c973"
web3 = w3(w3.HTTPProvider(infura_url))
chainId = 4

account = "0xc8f39fC331f0799F655490Bb7dc2D0d484018Bc0"
private_key = "abff363e849b97ba975265f8d28eafb56f0851011fcd37b211c78f0febd0b55a"

# Direccion del contrato y su ABI
contratoDir = "0x4a6F8f71814a8C8bd6a82591FD86ab89E5f9F125"
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


# Esta funcion pasa el audio a String
def speak(msg):
    engine = pyttsx3.init("sapi5")
    engine.setProperty("volume", 1.0)
    engine.setProperty("rate", 200)
    # voices = engine.getProperty("voices")
    engine.setProperty("voz", "españa")
    print("MarioVoice: " + msg)
    engine.say(msg)
    engine.runAndWait()


# Función responsable de escuchar y reconocer el habla.


def oir_microfono():
    # Habilita el microfono para oir al usuario
    microfono = sr.Recognizer()
    with sr.Microphone() as recurso:
        # Funcion de speech_recognition para eliminar el ruido
        microfono.adjust_for_ambient_noise(recurso)
        # Deja saber que esta oyendo al usuario
        speak("What is your command?: ")
        # Almacene la información de audio en la variable audio
        audio = microfono.listen(recurso)
    try:
        # Pasa el audio al reconocedor de patrones speech_recognition
        estado = microfono.recognize_google(audio, language="es-Es")
        # Después de unos segundos, devuelve la frase hablada.
        print("Voz dice: " + estado)
        speak("Voz dice: " + estado)
        enviarEstado(estado)
        # Si no reconoció el patrón de voz, muestra este mensaje que no entendió
    except sr.UnknownValueError:
        print("No entendí")


oir_microfono()
