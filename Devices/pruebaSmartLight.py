import serial

arduinoCMD = serial.Serial("COM5", 9600)

while True:
    comando = input(
        "Ingrese su color R:G:B 0-250 "
    )  # Se debe ingresar un color como este 200:200:40

    comando = comando + "\r"
    arduinoCMD.write(comando.encode())
