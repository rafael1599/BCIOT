import serial  # add Serial library for Serial communication

arduinoData = serial.Serial("com5")
comando = "1"
arduinoData.write(comando.encode())
print("fin")
