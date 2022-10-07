import serial  # add Serial library for Serial communication

Arduino_Serial = serial.Serial(
    "com5", 9600
)  # Create Serial port object called arduinoSerialData
input(Arduino_Serial.readline())  # read the serial data and print it as line
print("Enter 1 to ON LED and 0 to OFF LED")

# while 1:  # infinite loop
#     input_data = input("==> ")  # prints the data for confirmation

#     if input_data == "1":  # if the entered data is 1
#         Arduino_Serial.write("1")  # send 1 to arduino
#         print("LED ON")

#     if input_data == "0":  # if the entered data is 0
#         Arduino_Serial.write("0")  # send 0 to arduino
#         print("LED OFF")
