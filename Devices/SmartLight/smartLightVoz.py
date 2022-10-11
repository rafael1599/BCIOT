# Esta version esta intacta, deberia funcionar con el archivo LED_Block
# que tiene como comandos de entrada palabras, NO NUMEROS.

import json
import speech_recognition as sr
import pyttsx3
from web3 import Web3 as w3

# Informacion de la conexion a BC
infura_url = "https://goerli.infura.io/v3/f1ee978b04d04b4e8bb83d51b731c973"
web3 = w3(w3.HTTPProvider(infura_url))
chain_id = 4

account = "0xc8f39fC331f0799F655490Bb7dc2D0d484018Bc0"
private_key = "abff363e849b97ba975265f8d28eafb56f0851011fcd37b211c78f0febd0b55a"

# Direccion del contrato y su ABI
contract_Address = "0x4a6F8f71814a8C8bd6a82591FD86ab89E5f9F125"
contract_abi = json.loads(
    '[ 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "comando", 				"type": "string" 			} 		], 		"name": "manejarLED", 		"type": "event" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_comando", 				"type": "string" 			} 		], 		"name": "enviarComando", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	} ]'
)

contract = web3.eth.contract(address=contract_Address, abi=contract_abi)

nonce = web3.eth.getTransactionCount(account)

comando = ""


def enviarEstado(estado):
    # Esperar que la transaccion se mine
    transaction = contract.functions.enviarComando(estado).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            "chainId": chain_id,
            "from": account,
            "nonce": nonce,
        }
    )
    signed_transaction = web3.eth.account.sign_transaction(
        transaction, private_key=private_key
    )
    print(signed_transaction)
    print("\n")
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(transaction_hash)

    # transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)


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
    with sr.Microphone() as source:
        # Funcion de speech_recognition para eliminar el ruido
        microfono.adjust_for_ambient_noise(source)
        # Deja saber que esta oyendo al usuario
        speak("Cual es su comando ?: ")
        # Almacene la información de audio en la variable audio
        audio = microfono.listen(source)
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
