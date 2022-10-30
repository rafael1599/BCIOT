import serial as s

conexion = s.Serial("COM3", 9600)

command = input("Ingrese Encender o Apagar: ")

if command == "Encender":
    command = command + "\r"
    print("El command que esta siendo enviado al arduino es: " + command)
    conexion.write(command.encode())
    print("LED encendido")
elif command == "1":
    command = command + "\r"
    print("El command que esta siendo enviado al arduino es: " + command)
    conexion.write(command.encode())
    print("LED 0")

# int led =2;
# String command;

# void setup() {
#   // put your setup code here, to run once:
#   Serial.begin(9600);
#   pinMode(led, OUTPUT);
# }

# void loop() {
#   // put your main code here, to run repeatedly:
#   while (Serial.available() == 0){

#     }
#   command = Serial.readStringUntil('\r');

#   if (command == "Encender")
#      digitalWrite(led, HIGH);

#   if (command == "Apagar")
#      digitalWrite(led, LOW);

#   if (command == "")
#       Serial.println("command incorrecto, intentelo de nuevo");
# }