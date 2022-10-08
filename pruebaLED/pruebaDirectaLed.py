import serial  # para cominicarse con arduino
import sys
import json
from web3 import Web3 as w3
import asyncio

arduinoData = serial.Serial("com5")
comando = "1"
arduinoData.write(comando.encode())
print("fin")
