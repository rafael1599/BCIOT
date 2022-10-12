# Aqui solo podemos controlar al arduino desde el IDE Remix de Ethereum, una vez desplegado el contrato
# podemos comenzar a enviar comandos al contrato para controlar el led.

from base64 import encode
import sys
import json
from web3 import Web3 as w3
import asyncio
import warnings
import time
import serial as s

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Generalidades
infura_url = "https://goerli.infura.io/v3/f1ee978b04d04b4e8bb83d51b731c973"
w3 = w3(w3.HTTPProvider(infura_url))
print(w3.isConnected())

print(
    "BIENVENIDO: En Remix, escribe uno de estos numeros segun desees:"
    + "\nEscriba Encender para encender LED."
    + "\nEscriba Apagar para apagar LED. "
    + "\nEscriba Finalizar programa para finalizar programa."
)

contract_Address = "0x5b2f3a01031b5AcB1fE60Aa1EF1a73a6457cd5E7"
contract_abi = json.loads(
    '[{"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "comando","type": "string"}],"name": "manejarLED","type": "event"},{"inputs": [{"internalType": "string","name": "_comando","type": "string"}],"name": "enviarComando","outputs": [],"stateMutability": "nonpayable","type": "function"} ]'
)

contract = w3.eth.contract(address=contract_Address, abi=contract_abi)

conexion = s.Serial("COM5", 9600)

# Funciones
async def log_loop(event_filter, poll_interval):
    while True:
        for manejarLED in event_filter.get_new_entries():
            handle_event(manejarLED)
        await asyncio.sleep(poll_interval)


comando = ""
encender = "Encender"
apagar = "Apagar"


def handle_event(event):
    orden = json.loads(w3.toJSON(event))
    comando = orden["args"]
    print(comando["comando"])
    if comando["comando"] == "Encender":
        print("Se está enviando: " + encender)
        conexion.write(encender.encode())
        print("LED encendido")
    elif comando["comando"] == "Apagar":
        print("Se está enviando: " + apagar)
        conexion.write(apagar.encode())
        print("LED apagado")
    else:
        print("la opción que elegiste no es correcta o reconocida. Intentalo de nuevo")


def main():
    event_filter = contract.events.manejarLED.createFilter(fromBlock="latest")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        print("Finalizando procesos")
        loop.close()


if __name__ == "__main__":
    main()
