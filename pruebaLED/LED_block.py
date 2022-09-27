import sys
# import the following dependencies
import json
from web3 import Web3 as w3
import asyncio
import warnings
import time
import pyfirmata
from pyfirmata import Arduino, util
warnings.filterwarnings("ignore", category = DeprecationWarning)
 
# add your blockchain connection information
infura_url =  'https://rinkeby.infura.io/v3/eb28ba0d5b2848d39c6a5367837d5ce2'
w3= w3(w3.HTTPProvider(infura_url))
print(w3.isConnected())
print("En el SC escribe uno de estos numeros segun desees: \n1. Encender LED./n0. Apagar LED. \n2. Finalizar programa.")
 
# contract address and abi
contract_Address = '0xA795c368906d8Ef99Cc94330cCad284365F2c991'
contract_abi = json.loads('[ 	{ 		"anonymous": false, 		"inputs": [ 			{ 				"indexed": false, 				"internalType": "string", 				"name": "comando", 				"type": "string" 			} 		], 		"name": "manejarLED", 		"type": "event" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "string", 				"name": "_comando", 				"type": "string" 			} 		], 		"name": "enviarComando", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	} ]')
 
contract = w3.eth.contract(address=contract_Address, abi=contract_abi)
 
board = Arduino("COM7")
 
comando = ""
 
 
def handle_event(event):
    person_dict = json.loads(w3.toJSON(event))
    comando = person_dict["args"]
    print(comando["comando"])
    if comando["comando"] == "1":
        board.digital[13].write(1)
        print("LED encendido")
    elif comando["comando"] == "0":
        board.digital[13].write(0)
        print("LED apagado")
    elif comando["comando"] == "2":
        sys.exit("Bye bye!")
    else:
        print("la opción que elegiste no es correcta o reconocida. Intentalo de nuevo")
 
 
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