import warnings
from turtle import color
import serial  # para cominicarse con arduino
import sys
import json
from web3 import Web3 as w3
import asyncio

warnings.filterwarnings("ignore", category=DeprecationWarning)
arduinoCMD = serial.Serial("COM5", 9600)

# Funciones
def enviar_comando(comando):
    comando = comando + "\r"
    arduinoCMD.write(comando.encode())


def avisar_arduino(event):
    rojo = "255:0:0"
    verde = "0:255:0"
    azul = "0:0:255"
    apagar = "0:0:0"

    person_dict = json.loads(w3.toJSON(event))
    comando = person_dict["args"]
    print(comando["comando"])
    if comando["comando"] == "1":
        enviar_comando(rojo)
        print("tu color elegido, se encendio")
    elif comando["comando"] == "2":
        enviar_comando(verde)
        print("tu color elegido, se encendio")
    elif comando["comando"] == "3":
        enviar_comando(azul)
        print("tu color elegido, se encendio")
    elif comando["comando"] == "Finalizar":
        print("Apagando led")
        enviar_comando(apagar)
        sys.exit()
    else:
        print("Comando no reconocido, intentelo de nuevo")


async def bucle_registro(event_filter, poll_interval):
    while True:
        for manejarLED in event_filter.get_new_entries():
            avisar_arduino(manejarLED)
        await asyncio.sleep(poll_interval)


infura_url = "https://goerli.infura.io/v3/f1ee978b04d04b4e8bb83d51b731c973"
w3 = w3(w3.HTTPProvider(infura_url))
print(w3.isConnected())

print(
    "BIENVENIDO: En Remix, Ingrese el numero correspondiente a su color a cambiar:\n1. Rojo\n2. Verde\n3. Azul"
)

contract_Address = "0x4a6F8f71814a8C8bd6a82591FD86ab89E5f9F125"
contract_abi = json.loads(
    '[{"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "comando","type": "string"}],"name": "manejarLED","type": "event"},{"inputs": [{"internalType": "string","name": "_comando","type": "string"}],"name": "enviarComando","outputs": [],"stateMutability": "nonpayable","type": "function"} ]'
)

contract = w3.eth.contract(address=contract_Address, abi=contract_abi)


def main():
    event_filter = contract.events.manejarLED.createFilter(fromBlock="latest")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(bucle_registro(event_filter, 2)))
    finally:
        # close loop to free up system resources
        print("Finalizando procesos")
        loop.close()


if __name__ == "__main__":
    main()
