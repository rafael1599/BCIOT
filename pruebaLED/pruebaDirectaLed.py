import serial  # para cominicarse con arduino

arduinoData = serial.Serial("com5")


# def color_elegido(color):
color = input("Ingrese 1 para Rojo, 2 para Verde o 3 para Azul: ")
rojo = "255:50:0"
verde = "0:255:0"
azul = "0:0:255"

if color == "1":
    arduinoData.write(rojo.encode())
    color = "Rojo"
    print("Se encendio el color " + color)
elif color == "2":
    arduinoData.write(verde.encode())
    color = "Verde"
    print("Se encendio el color " + color)
elif color == "3":
    arduinoData.write(azul.encode())
    color = "Azul"
    print("Se encendio el color " + color)
else:
    print("La opcion elegida no existe")
