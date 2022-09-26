# IoT-Blockchain Manual 

> Repositorio GitHub del proyecto [BCIOT](https://github.com/rafael1599/BCIOT).

**Contenido:** [ Introducción](#introduccion) -[ Características](#caracteristicas) -[ Descripciones](#descripciones)
>falta corregir el contenido **NO OLVIDAR**
  

## Introducción

Un pequeño preámbulo que será agregado más adelante explicando de manera general nuestro proyecto.

---

## Caracteristicas
¿Qué es lo que hace? aún en desarrollo..


---

## Contenido


### **Algunos conceptos clave**
Antes de comenzar con la programación nos gustaría presentar algunos conceptos necesarios para poder comprender el funcioniamento de lo que estamos desarrollando en este proyecto.

### ¿Qué es Blockchain?
> Blockchain es un libro mayor compartido e inmutable que facilita el proceso de registro de transacciones y de seguimiento de activos en una red de negocios. Un activo puede ser tangible (una casa, un auto, dinero en efectivo, terrenos) o intangible (propiedad intelectual, patentes, derechos de autor, marcas). Prácticamente cualquier cosa de valor puede ser rastreada y comercializada en una red de blockchain, reduciendo el riesgo y los costos para todos los involucrados.

### ¿Qué es Ethereum?
>Ethereum es una plataforma digital que adopta la tecnología de cadena de bloques (blockchain) y expande su uso a una gran variedad de aplicaciones. Ether, su criptomoneda nativa, es la segunda más grande del mercado.

### ¿Qué es un Smart Contract?
>Un smart contract es un tipo especial de instrucciones que es almacenada en la blockchain. Y que además tiene la capacidad de autoejecutar acciones de acuerdo a una serie de parámetros ya programados. Todo esto de forma inmutable, transparente y completamente segura.

### ¿Qué es Infura?
>Infura es una plataforma para conectar con redes Blockchain y permite a los desarrolladores construir Smart Contracts utilizando un API JSON-RPC para interactuar con múltiples blockchains.

### ¿Qué es una red de pruebas?
>Una red testnet es una herramienta imprescindible en el desarrollo de criptomonedas como Bitcoin. Gracias a este tipo de redes los equipos de desarrollo pueden hacer pruebas sin afectar el funcionamiento de la red original.

### ¿Qué es RINKEBY?
>Rinkeby. Una red de prueba con prueba de autoridad para los que ejecutan clientes de Geth.

### ¿Qué es IoT?
>El término IoT, o Internet de las cosas, se refiere a la red colectiva de dispositivos conectados y a la tecnología que facilita la comunicación entre los dispositivos y la nube, así como entre los propios dispositivos

### ¿Qué vulnerabilidades tiene el IoT?
>La seguridad de IoT siguen siendo un desafío importante esto en gran parte, debido al crecimiento en gran escala de la adopción de los dispositivos IoT y su crecimiento exponencial que ha estado aconteciendo hoy en día. Mientras las empresas que desarrollan la tecnología IoT buscan nuevas formas de proteger la infraestructura donde se guardan y manejan los datos. Por el otro lado, los atacantes también idean nuevas formas de poder infiltrarse o vulnerar la seguridad, de afectar negativamente la confidencialidad de la información de los dispositivos, de hacerse con el control de acceso a los dispositivos o sensores, así como también afectando la integridad de la información que estos envían o reciben, y por último la disponibilidad de los mismos.

### ¿Cómo la tecnología blockchain puede ayudar?
>La tecnología Blockchain ayudaria en un adecuado manejo de la información, permitirá a los usuarios hacer uso de cualquier dispositivo IoT de manera segura. También permitirá una encriptación de los datos, de esta manera asegurando la privacidad de la información que el usuario envía a la red sin la posibilidad de que alguien intercepte esta información y pueda alterarla, robarla, eliminarla o usarla de manera indebida, lo que beneficia a todos los usuarios que tienen accesos a los dispositivos IoT de la organización


---

# Instalación de herramientas de desarrollo
A continuación explicamos el paso a paso del desarrollo completo de esta pequeña demostración.

## 1. Instalando Python
Necesitamos descargar python (en su última versión estable), buscamos "python Download" en nuestro navegador o directamente puedes ingresar a la página oficial de Python ['https://www.python.org/downloads/'].

Damos click en el primer 
[resultado](https://www.python.org/downloads/) que encontramos.

<img src="img/pythonDownload.png" width="70%"/>

Una vez dentro de la página de descarga, generalmente ya tenemos lista la versión de sistema operativo que necesitamos, pero podemos verificar dando click en el nombre del sistema operativo que estamos usando.

<img src="img/pythonDownload1.png" width="70%"/>

En mi caso lo voy a descargar para SO Windows y se vería así.

<img src="img/pythonDownloadWindows.png" width="70%"/>

> En este caso sería la versión seria la version 3.10.7

Damos click en el botón de descarga.

<img src="img/pythonDownloadWindowsDescargar.png"width="70%"/>

Guardamos el archivo de instalación.

<img src="img/pythonDownloadWindowsDescargar1.png" width="70%"/>

Guardamos en nuestro escritorio.

<img src="img/pythonDownloadEscritorio.png" width="70%"/>

Ejecutamos el archivo de instalación como administrador.

<img src="img/pythonDownloadEscritorio1.png" width="70%"/>

Luego simplemente damos click al botón que dice Si.

Y se te abrirá esta ventana de instalación de Python, donde **primero** nos aseguramos de tener marcada la casilla donde señalo la **X** roja y luego damos click en "Customize Installation".

<img src="img/pythonInstall.png" width="70%"/>


En la siguiente vista lo dejamos tal cual como esta y damos click en "Next".

<img src="img/pythonInstall1.png" width="70%"/>

Luego nos aseguramos que queden las opciones marcadas como en esta imagen así como también el lugar de instalación.

<img src="img/pythonInstall2.png" width="70%"/>

Y por último vamos a dar click en "Install".

<img src="img/pythonInstall3.png" width="70%"/>

Al final simplemente seleccionas el botón que dice "close" y listo terminamos de instalar Python!.

<img src="img/pythonInstall4.png" width="70%"/>

---

## ‎  
## 2. Instalando Visual Studio Code
Despues de descaragr Python, nos dirijimos a la siguiente pagina ['https://code.visualstudio.com/']

<img src="img/vscodeDownload.jpeg" width="70%"/>

---

## ‎ 

## 3. Creando red de prueba en Infura
> very soon..

---

## ‎ 

## 4. Creando el Smart Contract
> very soon..

---

## ‎ 

# Comenzando con el desarrollo
## Programacion del backend en vscode

Aqui mostramos los pasos para crear el programa que nos va a permitir conectar Blockchain con IoT mediante el uso de un contrato inteligente desplegado en una testnet llamada RINKEBY a la cual nos conectaremos mediante Infura, una herramienta que permite la interaccion entre sistemas web3 y web2.


#### **Desarrollo del programa encargado de conectar arduino con nuestro contrato inteligente alojado en RINKENBY.**

Aqui presentamos las importaciones que vamos a utilizar para que nuestro proyecto pueda funcionar...

```python

import json //para poder utilizar codigo json dentro de este programa
from web3 import Web3 as w3 //Para todo lo relacionado a blockchain
import asyncio //Para ejecutar bucles asincronos
import warnings //Para omitir mensajes warning
import time //Para obtener hora y fecha de el sistema
import pyfirmata //nos permite manejar arduino
from pyfirmata import Arduino, util

```
En esta parte, se ve el codigo para que la aplicacion se pueda conectar a Infura.
```python
infura_url =  '...' //dentro de las comillas se coloca el link que Infura te proporciona una vez creada tu red de testeo dentro de su pagina
w3= w3(w3.HTTPProvider(infura_url))
print(w3.isConnected())
print("...")
 
```
### En la parte de 

```python
infura_url =
```
### Se coloca el enlace que te muestra e proegrama segun la blockchain de prueba que vas a utilizar

### - En esta parte se coloca un mensjae personalizado 

```python
print("...")
```

###  Aqui se muestra el codigo para que la aplicacion se pueda conectar al Smart Contract (contrato inteligente)   
```python
contract_Address = '...'
contract_abi = json.loads('....')
 
contract = w3.eth.contract(address=contract_Address, abi=contract_abi)
```
### El contrato inteligente fue desarrollado en Remix con el lenjuage de programacion Solidity


```python
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
 
contract LedIoT {
 
    event manejarLED(string comando);
 
    function enviarComando(string memory _comando) public {
        emit manejarLED(_comando);
    }
}
```


## ¿ Que es Remix?
    Remix es un entorno integrado de desarrollo (IDE) basado en un navegador que integra un compilador y un entorno en tiempo de ejecución para Solidity sin los componentes orientados al servidor.

### Conexion  a arduino 
```python
board = Arduino("COM7")
```
### ¿Qué es una Arduino y para qué sirve?
    El arduino es una placa que tiene todos los elementos necesarios para conectar periféricos a las entradas y salidas de un microcontrolador. Es decir, es una placa impresa con los componentes necesarios para que funcione el microcontrolador y su comunicación con un ordenador a través de la comunicación serial.

```python
def handle_event(event):
    person_dict = json.loads(w3.toJSON(event))
    comando = person_dict["args"]
    print(comando["comando"])
    if comando["comando"] == "1":
        board.digital[13].write(1)
        print("LED encendido")
    elif comando["comando"] == "0":
        board.digital[13].write(0)
        print("LED apagado")
    elif comando["comando"] == "2":
        sys.exit("Bye bye!")
    else:
        print("la opción que elegiste no es correcta o reconocida. Intentalo de nuevo")
```
```python
async def log_loop(event_filter, poll_interval):
    while True:
        for manejarLED in event_filter.get_new_entries():
            handle_event(manejarLED)
        await asyncio.sleep(poll_interval)
```
```python
def main():
    event_filter = contract.events.manejarLED.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        print("Error inesperado. Cerrando programa para no dañar el equipo")
        loop.close()
 
if __name__ == "__main__":
    main()
```
```python
```
```python
```
```python
```
 ['Back to top'](#iot-blockchain)
 
## Descripciones
['Back to top'](#iot-blockchain)


