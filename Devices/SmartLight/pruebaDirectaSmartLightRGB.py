# Se usa con el archivo: importante codigo SmartLight arduino.txt
import serial  # para cominicarse con arduino

conexion = serial.Serial("com5")


# def color_elegido(color):
color = input("Ingrese 1 para Rojo, 2 para Verde o 3 para Azul: ")
rojo = "250:0:0"
verde = "0:250:0"
azul = "0:0:250"

if color == "1":
    conexion.write(rojo.encode())
    print("Se encendio el color Rojo")
elif color == "2":
    conexion.write(verde.encode())
    print("Se encendio el color Verde")
elif color == "3":
    conexion.write(azul.encode())
    print("Se encendio el color Azul")
else:
    print("La opcion elegida no existe")
