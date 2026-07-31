# Configuración y Control de Raspberry Pi Zero 2W mediante Bluetooth

## Descripción del proyecto

Este proyecto presenta la configuración y puesta en funcionamiento de una Raspberry Pi Zero 2W como plataforma de control remoto mediante comunicación Bluetooth. El sistema permite establecer una comunicación inalámbrica entre un dispositivo móvil Android y la Raspberry Pi, de manera que las instrucciones enviadas desde el teléfono puedan utilizarse para controlar dispositivos conectados a los pines GPIO de la tarjeta.

Como demostración del funcionamiento, se implementó el control de una secuencia luminosa tipo cascada utilizando cinco LEDs conectados a diferentes pines GPIO. La comunicación entre el dispositivo móvil y la Raspberry Pi se realiza mediante Bluetooth Serial utilizando el protocolo RFCOMM.

El sistema permite que la Raspberry Pi reciba comandos enviados desde un teléfono móvil, interprete estas instrucciones y ejecute acciones sobre los dispositivos conectados a sus GPIO. Aunque en esta implementación se utilizan LEDs como actuadores, la arquitectura puede adaptarse para controlar otros dispositivos como relés, motores, servomotores u otros actuadores compatibles.

---

## 1. Hardware utilizado

Para la implementación del sistema se utilizaron los siguientes elementos:

- Raspberry Pi Zero 2W.
- Tarjeta microSD.
- Cinco LEDs.
- Resistencias limitadoras de corriente de 220 Ω a 330 Ω.
- Protoboard.
- Cables jumper macho-hembra.
- Computador con Windows.
- Teléfono inteligente Android con Bluetooth.

La Raspberry Pi Zero 2W funciona como el controlador principal del sistema. En ella se ejecuta Raspberry Pi OS Lite y el programa desarrollado en Python encargado de gestionar la comunicación Bluetooth y el control de los dispositivos conectados a los GPIO.

La asignación de los LEDs utilizada en el proyecto es la siguiente:

| Actuador | GPIO (BCM) | Pin físico |
|---|---:|---:|
| LED 1 | GPIO 17 | Pin 11 |
| LED 2 | GPIO 27 | Pin 13 |
| LED 3 | GPIO 22 | Pin 15 |
| LED 4 | GPIO 10 | Pin 19 |
| LED 5 | GPIO 9 | Pin 21 |

Cada LED debe conectarse utilizando una resistencia limitadora de corriente en serie para proteger el LED y la salida GPIO de la Raspberry Pi.

---

## 2. Instalación y flasheo del sistema operativo

El primer paso consiste en instalar el sistema operativo que ejecutará la Raspberry Pi Zero 2W. Para este proyecto se utilizó Raspberry Pi OS Lite de 64 bits, una versión del sistema operativo que no incluye un entorno gráfico de escritorio y que resulta adecuada para aplicaciones embebidas y proyectos administrados remotamente.

La instalación se realiza utilizando Raspberry Pi Imager. Esta herramienta permite preparar la tarjeta microSD con el sistema operativo correspondiente.

Antes de iniciar la escritura de la imagen en la tarjeta, se configuran los parámetros necesarios para acceder posteriormente a la Raspberry Pi de forma remota.

Los parámetros utilizados fueron:

- Nombre de host: `raspberrypi`
- Usuario: `indebidos`
- SSH: habilitado mediante autenticación por contraseña.
- Red Wi-Fi: configurada previamente.
- Sistema operativo: Raspberry Pi OS Lite 64-bit.

La configuración previa de estos parámetros permite que la Raspberry Pi pueda iniciar y conectarse automáticamente a la red Wi-Fi sin necesidad de utilizar un monitor, teclado o mouse.

Una vez configurados los parámetros, se procede a grabar el sistema operativo en la tarjeta microSD. Raspberry Pi Imager realiza la escritura de los archivos necesarios y posteriormente verifica que el proceso se haya realizado correctamente.

Cuando finaliza la instalación, la tarjeta microSD se retira del computador y se inserta en la Raspberry Pi Zero 2W. Finalmente, se conecta la alimentación de la tarjeta para iniciar el sistema operativo.

---

## 3. Acceso remoto mediante SSH

Una vez iniciada la Raspberry Pi y conectada a la red Wi-Fi configurada, se establece una conexión remota mediante SSH.

SSH permite acceder a la terminal de la Raspberry Pi desde un computador externo, evitando la necesidad de conectar directamente un monitor, teclado o mouse.

Desde Windows se puede utilizar PowerShell o Windows Terminal para establecer la conexión. Para ello, se utiliza el usuario configurado durante la instalación junto con la dirección IP asignada a la Raspberry Pi dentro de la red local.

Una vez establecida correctamente la conexión, se obtiene acceso a la terminal del sistema y se pueden realizar de forma remota todas las tareas necesarias para configurar y ejecutar el proyecto.

Este procedimiento permite trabajar con la Raspberry Pi en modo *headless*, es decir, sin utilizar periféricos externos conectados directamente a la tarjeta.

---

## 4. Creación del entorno virtual de Python

Para ejecutar el software del proyecto se utiliza Python. Con el objetivo de mantener aisladas las dependencias y evitar conflictos con otros paquetes instalados en el sistema, se crea un entorno virtual utilizando `venv`.

El entorno virtual proporciona un espacio independiente donde se instalan las librerías necesarias para el proyecto.

Una vez creado, el entorno virtual debe activarse antes de instalar las dependencias y ejecutar el programa.

El uso de este entorno facilita la organización del proyecto y permite mantener una configuración reproducible para futuras instalaciones.

---

## 5. Instalación de dependencias

El proyecto utiliza principalmente las siguientes herramientas y librerías:

- **Python:** lenguaje utilizado para desarrollar la lógica de control.
- **BlueDot:** proporciona soporte para la comunicación Bluetooth utilizada en el proyecto.
- **GPIO Zero:** permite controlar de manera sencilla los dispositivos conectados a los pines GPIO de la Raspberry Pi.
- **BlueZ:** sistema de gestión de Bluetooth utilizado por Linux.

GPIO Zero se utiliza para organizar y controlar los cinco LEDs conectados a la Raspberry Pi, mientras que la comunicación Bluetooth permite recibir instrucciones de manera inalámbrica desde el teléfono móvil.

Las dependencias de Python deben instalarse dentro del entorno virtual creado previamente.

---

## 6. Configuración del servicio Bluetooth mediante BlueZ

Para permitir la comunicación Bluetooth entre la Raspberry Pi y el dispositivo móvil se utiliza BlueZ, el sistema de gestión de Bluetooth empleado en Linux.

El proyecto utiliza Bluetooth clásico mediante el protocolo RFCOMM, que permite establecer una comunicación similar a un puerto serial entre la Raspberry Pi y el dispositivo móvil.

Para que Python pueda utilizar correctamente los sockets RFCOMM, es necesario configurar el servicio Bluetooth de BlueZ en modo compatible.

Después de modificar la configuración correspondiente, se recarga la configuración de los servicios del sistema y se reinicia el servicio Bluetooth.

Esta configuración es necesaria para que el programa pueda crear correctamente el servidor Bluetooth y aceptar conexiones provenientes del teléfono móvil.

---

## 7. Emparejamiento Bluetooth con el teléfono móvil

Una vez configurado el servicio Bluetooth, se realiza el emparejamiento entre la Raspberry Pi y un teléfono inteligente Android.

La Raspberry Pi se configura para que su adaptador Bluetooth esté activo, visible y disponible para realizar el proceso de emparejamiento.

Desde el teléfono móvil se busca el dispositivo Bluetooth correspondiente a la Raspberry Pi y se inicia la vinculación.

Durante este proceso puede solicitarse la confirmación de una clave de emparejamiento. Una vez aceptada, ambos dispositivos quedan vinculados.

Para la comunicación se utiliza la aplicación **Serial Bluetooth Terminal**, que permite enviar mensajes de texto desde el teléfono móvil hacia la Raspberry Pi mediante Bluetooth.

---

## 8. Conexión de los actuadores a los GPIO

Con la Raspberry Pi configurada y la comunicación Bluetooth preparada, se realiza la conexión física de los actuadores.

En esta implementación se utilizaron cinco LEDs conectados a los GPIO 17, 27, 22, 10 y 9.

Cada salida GPIO controla un LED independiente mediante una resistencia limitadora conectada en serie.

Los LEDs funcionan como actuadores de demostración del sistema. El programa controla su comportamiento y genera una secuencia luminosa tipo cascada.

La arquitectura utilizada puede adaptarse para controlar otros dispositivos conectados a los GPIO, como módulos de relé, motores, servomotores u otros actuadores compatibles.

---

## 9. Funcionamiento general del programa

El programa desarrollado en Python tiene como objetivo establecer la comunicación Bluetooth y utilizar los mensajes recibidos para controlar los actuadores conectados a la Raspberry Pi.

Su funcionamiento se divide principalmente en tres componentes:

1. Configuración de los actuadores.
2. Ejecución de la secuencia de control.
3. Comunicación Bluetooth para recibir instrucciones.

Al iniciar, el programa configura los cinco LEDs conectados a los GPIO correspondientes.

Posteriormente, se ejecuta un proceso independiente encargado de controlar la secuencia luminosa.

Al mismo tiempo, el programa principal configura un servidor Bluetooth RFCOMM y permanece esperando una conexión proveniente del dispositivo móvil.

Cuando el teléfono establece la conexión, la Raspberry Pi comienza a recibir los mensajes enviados desde la aplicación Serial Bluetooth Terminal.

Los mensajes recibidos son interpretados como comandos de control.

En la implementación realizada se utilizan principalmente dos comandos:

- `avanzar`: activa la secuencia luminosa.
- `detener`: detiene la secuencia y apaga todos los LEDs.

Cuando se recibe el comando `avanzar`, el sistema cambia su estado interno y permite que la secuencia luminosa comience a ejecutarse.

Cuando se recibe el comando `detener`, el sistema interrumpe la secuencia y apaga todos los LEDs.

Si se recibe un comando diferente a los establecidos, el sistema lo identifica como un comando no reconocido y no realiza ninguna acción sobre los actuadores.

---

## 10. Control concurrente mediante hilos

Una característica importante de la implementación es el uso de hilos de ejecución (*threading*).

El sistema necesita realizar simultáneamente dos tareas:

- Esperar y recibir comandos mediante Bluetooth.
- Ejecutar continuamente la secuencia de los LEDs.

Para lograrlo, se utiliza un hilo independiente encargado de ejecutar la secuencia de iluminación.

Mientras este hilo controla los LEDs, el programa principal permanece disponible para recibir nuevos comandos mediante Bluetooth.

La comunicación entre ambas partes se realiza mediante una variable de estado que indica si la secuencia debe estar activa o detenida.

Cuando el sistema está detenido, los LEDs permanecen apagados. Cuando se recibe la orden de activación, el hilo comienza a ejecutar la secuencia.

Esta arquitectura permite que el sistema responda rápidamente a las instrucciones recibidas desde el teléfono móvil.

---

## 11. Secuencia de iluminación

La secuencia implementada genera un efecto de cascada en el que los LEDs se encienden uno después de otro.

El programa utiliza diferentes intervalos de tiempo para modificar la velocidad de desplazamiento de la secuencia.

La secuencia recorre los cinco LEDs en orden, encendiendo cada uno durante un intervalo determinado antes de apagarlo y continuar con el siguiente.

Los intervalos utilizados permiten generar diferentes velocidades de funcionamiento, desde una secuencia lenta hasta una más rápida.

Cuando se alcanza la velocidad máxima, se aumenta el número de repeticiones para que el efecto visual pueda ser apreciado antes de cambiar nuevamente de velocidad.

La secuencia permanece activa mientras el sistema se encuentre en estado de ejecución.

Cuando se recibe el comando `detener`, el sistema interrumpe la secuencia y apaga inmediatamente los actuadores.

---

## 12. Comunicación Bluetooth como interfaz de control

La comunicación Bluetooth funciona como una interfaz inalámbrica entre el usuario y el sistema embebido.

El teléfono inteligente actúa como dispositivo de control y la Raspberry Pi funciona como servidor.

El usuario envía una instrucción desde la aplicación Serial Bluetooth Terminal y esta información es transmitida mediante una conexión Bluetooth RFCOMM.

La Raspberry Pi recibe los datos, interpreta el comando y ejecuta la acción correspondiente sobre los GPIO.

El flujo general del sistema es:

**Dispositivo móvil → Bluetooth RFCOMM → Raspberry Pi → Procesamiento del comando → GPIO → Actuador**

En la implementación realizada:

**Teléfono Android → Comando Bluetooth → Raspberry Pi → Procesamiento → GPIO → LEDs**

Esta arquitectura permite separar la interfaz de usuario de la lógica de control. El usuario puede controlar el sistema desde un dispositivo móvil sin necesidad de interactuar directamente con la Raspberry Pi.

---

## 13. Aplicación para sensores y actuadores

Aunque la implementación de demostración utiliza cinco LEDs, la arquitectura desarrollada puede utilizarse como base para sistemas de automatización y control más complejos.

En el caso de los actuadores, los comandos recibidos mediante Bluetooth pueden utilizarse para activar o desactivar diferentes dispositivos conectados a los GPIO.

Por ejemplo, una instrucción enviada desde el teléfono podría activar un relé, encender un motor o modificar el estado de un sistema de señalización.

De forma similar, el proyecto puede ampliarse para trabajar con sensores. La Raspberry Pi podría realizar la lectura periódica de un sensor y enviar los datos obtenidos mediante Bluetooth hacia el dispositivo móvil.

El funcionamiento podría representarse de las siguientes maneras:

**Control de actuadores:**

`Dispositivo móvil → Bluetooth → Raspberry Pi → Procesamiento → Actuadores`

**Lectura de sensores:**

`Sensores → Raspberry Pi → Procesamiento → Bluetooth → Dispositivo móvil`

También es posible combinar ambas funciones para desarrollar un sistema bidireccional en el que el teléfono envíe comandos de control mientras la Raspberry Pi transmite información obtenida de diferentes sensores.

Esta arquitectura puede utilizarse como base para aplicaciones de sistemas embebidos, automatización, robótica e Internet de las Cosas (IoT).

---

## 14. Ejecución del sistema

Una vez finalizada la configuración de la Raspberry Pi, instalado el entorno virtual, configurado el servicio Bluetooth, realizado el emparejamiento con el teléfono y conectado el hardware, se procede a ejecutar el programa de control.

El programa se inicia dentro del entorno virtual de Python.

Cuando se ejecuta correctamente, la Raspberry Pi inicia el servidor Bluetooth RFCOMM y permanece a la espera de una conexión desde la aplicación Serial Bluetooth Terminal.

El funcionamiento esperado es el siguiente:

1. La Raspberry Pi inicia el programa.
2. Se configura el control de los cinco LEDs.
3. Se inicia el proceso encargado de ejecutar la secuencia luminosa.
4. Se inicia el servidor Bluetooth RFCOMM.
5. La Raspberry Pi espera una conexión.
6. El teléfono Android establece la conexión Bluetooth.
7. El usuario envía el comando de activación.
8. La Raspberry Pi recibe e interpreta el comando.
9. Se activa la secuencia de LEDs.
10. El usuario envía el comando de detención.
11. La Raspberry Pi detiene la secuencia.
12. Los LEDs se apagan.

El sistema también contempla el cierre de las conexiones Bluetooth y el apagado de los actuadores cuando finaliza la ejecución del programa.

---

## 15. Arquitectura general del sistema

```text
                    DISPOSITIVO MÓVIL
                           │
                           │
                    Bluetooth RFCOMM
                           │
                           ▼
                  ┌──────────────────┐
                  │  Raspberry Pi    │
                  │     Zero 2W      │
                  └──────────────────┘
                           │
                    Programa Python
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      Control de GPIO              Comunicación
             │                      Bluetooth
             │
             ▼
       Actuadores / LEDs
