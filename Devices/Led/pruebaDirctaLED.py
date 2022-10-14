import serial as s

conexion = s.Serial("COM5", 9600)

comando = input("Ingrese Encender o Apagar: ")

if comando == "Encender":
    comando = comando + "\r"
    print("El comando que esta siendo enviado al arduino es: " + comando)
    conexion.write(comando.encode())
    print("LED encendido")
elif comando == "Apagar":
    comando = comando + "\r"
    print("El comando que esta siendo enviado al arduino es: " + comando)
    conexion.write(comando.encode())
    print("LED Apagado")
