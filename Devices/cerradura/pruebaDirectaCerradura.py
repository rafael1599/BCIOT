import serial  # para cominicarse con arduino

arduinoData = serial.Serial("com5")
# def color_elegido(color):
command = input("Ingrese 1 para Abrir, 2 para Cerrar: ")
verde = "0:10:0"
rojo = "255:0:0"

if command == "1":
    print("El command que se esta enviando al arduino es: " + verde)
    arduinoData.write(verde.encode())
    print("Se abrió la cerradura")

elif command == "2":
    arduinoData.write(rojo.encode())
    print("Se cerró")
else:
    print("La opción elegida no existe")
