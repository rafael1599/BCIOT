# SMART LIGHT CONECTADA CON BLOCKCHAIN VERSIÓN 1.0
# Version donde le cambio los commands de numeros a palabras
# para que funcione con commands de voz

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
def enviar_command(commandArd):
    commandArd = commandArd + "\r"
    arduinoCMD.write(commandArd.encode())


def avisar_arduino(event):
    rojo = "255:0:0"
    verde = "0:255:0"
    azul = "0:0:255"
    apagar = "0:0:0"

    orden = json.loads(w3.toJSON(event))
    commandVoz = orden["args"]
    print(commandVoz["command"])
    if commandVoz["command"] == "Red":
        enviar_command(rojo)
        print("el color " + commandVoz + " se encendio")
    elif commandVoz["command"] == "Green":
        enviar_command(verde)
        print("el color " + commandVoz + " se encendio")
    elif commandVoz["command"] == "Blue":
        enviar_command(azul)
        print("el color " + commandVoz + " se encendio")
    elif commandVoz["command"] == "Finish":
        print("Apagando led")
        enviar_command(apagar)
        sys.exit()
    else:
        print("command no reconocido, intentelo de nuevo")


async def bucle_registro(event_filter, poll_interval):
    while True:
        for manejarLED in event_filter.get_new_entries():
            avisar_arduino(manejarLED)
        await asyncio.sleep(poll_interval)


infura_url = "https://goerli.infura.io/v3/f1ee978b04d04b4e8bb83d51b731c973"
w3 = w3(w3.HTTPProvider(infura_url))
print(w3.isConnected())

print(
    "BIENVENIDO: Diga el numero correspondiente a su color a cambiar:\n- Rojo\n- Verde\n- Azul \n- Finalizar programa"
)

contract_Address = "0x4a6F8f71814a8C8bd6a82591FD86ab89E5f9F125"
contract_abi = json.loads(
    '[{"anonymous": false,"inputs": [{"indexed": false,"internalType": "string","name": "command","type": "string"}],"name": "manejarLED","type": "event"},{"inputs": [{"internalType": "string","name": "_command","type": "string"}],"name": "enviarcommand","outputs": [],"stateMutability": "nonpayable","type": "function"} ]'
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
