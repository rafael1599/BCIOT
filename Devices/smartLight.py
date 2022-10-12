import serial

arduinoCMD = serial.Serial("COM5", 9600)

while True:
    comando = input("Ingrese su color R:G:B 0-255 ")
    comando = comando + "\r"
    arduinoCMD.write(comando.encode())
