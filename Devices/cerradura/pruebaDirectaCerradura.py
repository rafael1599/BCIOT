import serial  # para cominicarse con arduino

arduinoData = serial.Serial("com5")
# def color_elegido(color):
color = input("Ingrese 1 para Abrir, 2 para Cerrar: ")
verde = "0:10:0"
rojo = "255:0:0"

if color == "1":
    arduinoData.write(verde.encode())
    print("Se abrió la cerradura")

elif color == "2":
    arduinoData.write(rojo.encode())
    print("Se cerró")
else:
    print("La opción elegida no existe")
