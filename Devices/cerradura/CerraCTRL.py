# Controlar la cerradura desde REMIX
import warnings
import serial as s  # para cominicarse con arduino
import json
from web3 import Web3 as w3
import asyncio

warnings.filterwarnings("ignore", category=DeprecationWarning)
conexion = s.Serial("COM5", 9600)

# ---> Declaraciones y presentación
infura_url = "https://goerli.infura.io/v3/f1ee978b04d04b4e8bb83d51b731c973"
w3 = w3(w3.HTTPProvider(infura_url))
print(w3.isConnected())

print(
    "BIENVENIDO!: Ingrese su comando en REMIX o use el "
    + "comando por voz, sus opciones son:\n1. Open\n2. Close\n3. Off"
)

contract_Address = "0x1d0DB50A11C3AAE2A2821D0dB69D44f27b391fFB"
contract_abi = json.loads(
    '[ 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "comandoLock", 				"type": "string" 			} 		], 		"name": "manejarLock", 		"type": "event" 	}, 	{ 		"inputs": [], 		"name": "comandoLock", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_comandoLock", 				"type": "string" 			} 		], 		"name": "enviarComandoLock", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "getComandoLock", 		"outputs": [ 			{ 				"internalType": "string", 				"name": "", 				"type": "string" 			} 		], 		"stateMutability": "view", 		"type": "function" 	} ]'
)

contract = w3.eth.contract(address=contract_Address, abi=contract_abi)
# <---

# Funciones
def enviar_comando(comando):
    comando = comando + "\r"
    print("Se esta enviando el comando <<" + comando + ">> al arduino")
    conexion.write(comando.encode())


def avisar_arduino(event):
    verde = "0:10:0"
    rojo = "10:0:0"
    apagar = "0:0:0"

    orden = json.loads(w3.toJSON(event))
    # print("La orden es: ", orden)
    comando = orden["args"]
    print("Comando proviniente de REMIX:", comando["comando"])
    if comando["comando"] == "Open":
        enviar_comando(verde)
        print("La cerradura se abrió")
    elif comando["comando"] == "Close":
        enviar_comando(rojo)
        print("La cerradura se bloqueó")
    elif comando["comando"] == "Off":
        print("Finalizando...")
        enviar_comando(apagar)
    else:
        print("Comando no reconocido, intentelo de nuevo")


async def bucle_registro(event_filter, poll_interval):
    while True:
        for manejarLock in event_filter.get_new_entries():
            avisar_arduino(manejarLock)
        await asyncio.sleep(poll_interval)


def main():
    event_filter = contract.events.manejarLock.createFilter(fromBlock="latest")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(bucle_registro(event_filter, 2)))
    finally:
        # close loop to free up system resources
        print("Finalizando procesos")
        loop.close()


if __name__ == "__main__":
    main()
