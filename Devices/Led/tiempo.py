import time

# Aqui se estan haciendo las pruebas para medir el tiempo

import sys
import json
from web3 import Web3 as w3
import asyncio
import warnings
from pyfirmata import Arduino, util

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

contract_Address = "0x021df6de933553DfB30a5A4926db55F1D3C9609c"
contract_abi = json.loads(
    '[{"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "comando","type": "string"}],"name": "manejarLED","type": "event"},{"inputs": [{"internalType": "string","name": "_comando","type": "string"}],"name": "enviarComando","outputs": [],"stateMutability": "nonpayable","type": "function"} ]'
)

contract = w3.eth.contract(address=contract_Address, abi=contract_abi)

board = Arduino("COM5")

# Funciones
async def log_loop(event_filter, poll_interval):
    while True:
        for manejarLED in event_filter.get_new_entries():
            handle_event(manejarLED)
        await asyncio.sleep(poll_interval)


comando = ""


def handle_event(event):
    person_dict = json.loads(w3.toJSON(event))
    comando = person_dict["args"]
    print(comando["comando"])
    if comando["comando"] == "Encender":
        board.digital[13].write(1)
        print("LED encendido")
        # Tiempo final
        tiempoFinal = time.time()
        print("El tiempo al culminar la ejecucion es:", tiempoFinal)
    elif comando["comando"] == "Apagar":
        board.digital[13].write(0)
        print("LED apagado")
        # Tiempo final
        tiempoFinal = time.time()
        print("El tiempo al culminar la ejecucion es:", tiempoFinal)
    elif comando["comando"] == "Finalizar":
        # Tiempo final
        tiempoFinal = time.time()
        print("El tiempo al culminar la ejecucion es:", tiempoFinal)
        sys.exit("Finalizando...")
    else:
        # Tiempo final
        tiempoFinal = time.time()
        print("El tiempo al culminar la ejecucion es:", tiempoFinal)
        print("la opción que elegiste no es correcta o reconocida. Intentalo de nuevo")


def main():
    event_filter = contract.events.manejarLED.createFilter(fromBlock="latest")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        print("Finalizando procesos...")
        loop.close()


if __name__ == "__main__":
    main()
