#Aqui solo podemos controlar al arduino desde el IDE Remix de Ethereum, una vez desplegado el contrato 
#podemos comenzar a enviar comandos al contrato para controlar el led.

import sys
import json
warnings.filterwarnings("ignore", category = DeprecationWarning)
from web3 import Web3 
import asyncio
import warnings
import time
import pyfirmata
from pyfirmata import Arduino, util
import speech_recognition as sr
import pyttsx3

infura_url =  'https://rinkeby.infura.io/v3/eb28ba0d5b2848d39c6a5367837d5ce2'
web3= Web3(Web3.HTTPProvider(infura_url))
chain_id = 4

account = "0xc3aA817a76962CB7Ce0bf37e8E3Cdd1891436f23"
private_key = '345b83b70fe09d2b7d060312cf3174755c8caf1410a952188d4db10ca7b171e4'

print(web3.isConnected())
print(
    "BIENVENIDO: En Remix escribe uno de estos numeros segun desees:" +
    "\nEscriba Encender para encender LED."+
    "\nEscriba Apagar para apagar LED. "+
    "\nEscriba Cerrar para finalizar programa.")
 
contract_Address = '0xA795c368906d8Ef99Cc94330cCad284365F2c991'

contract_abi = json.loads(
'[{"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "comando","type": "string"}], "name": "manejarLED","type": "event"},{"inputs": [{"internalType": "string","name": "_comando", "type": "string" }],"name": "enviarComando", "outputs": [],"stateMutability": "nonpayable", "type": "function" }]'
    )
contract = web3.eth.contract(address=contract_Address, abi=contract_abi)
nonce = web3.eth.getTransactionCount(account)

board = Arduino("COM7")
 
comando = ""
def enviarComando(comando):
    # Esperar que la transaccion sea minada
    transaction = contract.functions.manejarLED(comando).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            "chainId": chain_id,
            "from": account,
            "nonce": nonce 
        }
    )
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key = private_key)
    print(signed_transaction)
    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(transaction_hash)
    transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    
def speak(msg):
        engine = pyttsx3.init('sapi5')
        engine.setProperty('volume', 1.0)
        engine.setProperty('rate', 200)         
        voices = engine.getProperty('voices')
        engine.setProperty("voice", "brazil")
        print('MariaVoice: ' + msg)
        engine.say(msg)
        engine.runAndWait()

def handle_event(event):
    person_dict = json.loads(w3.toJSON(event))
    comando = person_dict["args"]
    print(comando["comando"])
    if comando["comando"] == "Encendido":
        board.digital[13].write(1)
        print("LED encendido")
    elif comando["comando"] == "Apagado":
        board.digital[13].write(0)
        print("LED apagado")
    elif comando["comando"] == "Cerrar":
        sys.exit("Bye bye!")
    else:
        print("la opción que elegiste no es correcta o reconocida. Intentalo de nuevo")

def ouvir_microfone():    
    #Habilita o microfone para ouvir o usuario
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        #Chama a funcao de reducao de ruido disponivel na speech_recognition
        microfone.adjust_for_ambient_noise(source)
        #Avisa ao usuario que esta pronto para ouvir        
        speak("Qual é o comando?: ")
        #Armazena a informacao de audio na variavel
        audio = microfone.listen(source)
    try:
        #Passa o audio para o reconhecedor de padroes do speech_recognition
        comando = microfone.recognize_google(audio,language='pt-BR')
        #Após alguns segundos, retorna a frase falada
        print("Você disse: " + comando)
        speak("Você disse: " + comando)
        enviarComando(comando)               
        #Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
    except sr.UnkownValueError:
            print("Não entendi")


ouvir_microfone()
 
async def log_loop(event_filter, poll_interval):
    while True:
        for manejarLED in event_filter.get_new_entries():
            handle_event(manejarLED)
        await asyncio.sleep(poll_interval)
 
def main():
    event_filter = contract.events.manejarLED.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        print("Error inesperado. Cerrando programa para no dañar el equipo")
        loop.close()
 

if __name__ == "__main__":
    main()
