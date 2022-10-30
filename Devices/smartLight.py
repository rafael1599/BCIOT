import serial

arduinoCMD = serial.Serial("COM5", 9600)

while True:
    command = input("Ingrese su color R:G:B 0-255 ")
    command = command + "\r"
    arduinoCMD.write(command.encode())
