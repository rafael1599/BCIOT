# Se usa con el archivo: importante codigo SmartLight arduino.txt
import serial  # para cominicarse con arduino

arduinoData = serial.Serial("com5")


# def color_elegido(color):
color = input("Ingrese 1 para Rojo, 2 para Verde o 3 para Azul: ")
rojo = "255:0:0"
verde = "0:255:0"
azul = "0:0:255"

if color == "1":
    arduinoData.write(rojo.encode())
    print("Se encendio el color Rojo")
elif color == "2":
    arduinoData.write(verde.encode())
    print("Se encendio el color Verde")
elif color == "3":
    arduinoData.write(azul.encode())
    print("Se encendio el color Azul")
else:
    print("La opcion elegida no existe")
