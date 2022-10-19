import serial as s

conexion = s.Serial("COM3", 9600)

comando = input("Ingrese Encender o Apagar: ")

if comando == "Encender":
    comando = comando + "\r"
    print("El comando que esta siendo enviado al arduino es: " + comando)
    conexion.write(comando.encode())
    print("LED encendido")
elif comando == "1":
    comando = comando + "\r"
    print("El comando que esta siendo enviado al arduino es: " + comando)
    conexion.write(comando.encode())
    print("LED 0")

# int led =2;
# String comando;

# void setup() {
#   // put your setup code here, to run once:
#   Serial.begin(9600);
#   pinMode(led, OUTPUT);
# }

# void loop() {
#   // put your main code here, to run repeatedly:
#   while (Serial.available() == 0){

#     }
#   comando = Serial.readStringUntil('\r');

#   if (comando == "Encender")
#      digitalWrite(led, HIGH);

#   if (comando == "Apagar")
#      digitalWrite(led, LOW);

#   if (comando == "")
#       Serial.println("Comando incorrecto, intentelo de nuevo");
# }