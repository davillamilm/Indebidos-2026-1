# Configuración y control de Raspberry Pi Zero 2W mediante Bluetooth

## Descripción del proyecto

Este proyecto consiste en la configuración y puesta en funcionamiento de una Raspberry Pi Zero 2W como plataforma de control inalámbrico para dispositivos conectados a sus pines GPIO. La comunicación con el sistema se realiza mediante Bluetooth, permitiendo enviar instrucciones desde un dispositivo móvil hacia la Raspberry Pi para controlar diferentes actuadores.

Como aplicación de prueba, se implementó el control de cinco LEDs conectados a los pines GPIO de la Raspberry Pi. El sistema permite activar una secuencia luminosa tipo cascada y detenerla mediante comandos enviados de forma inalámbrica. Para establecer esta comunicación se utiliza Bluetooth clásico mediante el protocolo RFCOMM, mientras que el control de los dispositivos conectados a los GPIO se realiza mediante Python y la librería GPIO Zero.

La implementación desarrollada permite comprobar el funcionamiento conjunto de la comunicación inalámbrica, el procesamiento de comandos y el control de dispositivos físicos. Aunque en este proyecto se utilizan LEDs como actuadores, la arquitectura propuesta puede adaptarse a otras aplicaciones en las que sea necesario controlar relés, motores, servomotores u otros dispositivos compatibles con las características eléctricas de los GPIO de la Raspberry Pi.

De igual manera, la estructura del sistema puede ampliarse para incorporar sensores y establecer una comunicación bidireccional, de forma que la Raspberry Pi no solo reciba comandos de control, sino que también pueda procesar información obtenida de sensores y transmitirla hacia el dispositivo móvil.

---

## Hardware utilizado

Para la implementación del proyecto se utilizaron los siguientes elementos:

- Raspberry Pi Zero 2W.
- Tarjeta microSD.
- Cinco LEDs.
- Resistencias limitadoras de corriente de 220 Ω a 330 Ω.
- Protoboard.
- Cables jumper.
- Computador para la configuración inicial de la Raspberry Pi.
- Dispositivo móvil con comunicación Bluetooth.

La Raspberry Pi Zero 2W funciona como la unidad principal de procesamiento y control del sistema. En ella se ejecuta Raspberry Pi OS Lite y el programa desarrollado en Python, encargado de gestionar la comunicación Bluetooth y controlar los actuadores conectados a los pines GPIO.

La conexión de los cinco LEDs se realizó utilizando la siguiente asignación:

| Actuador | GPIO (BCM) | Pin físico |
|---|---:|---:|
| LED 1 | GPIO 17 | Pin 11 |
| LED 2 | GPIO 27 | Pin 13 |
| LED 3 | GPIO 22 | Pin 15 |
| LED 4 | GPIO 10 | Pin 19 |
| LED 5 | GPIO 9 | Pin 21 |

Cada LED se conecta mediante una resistencia limitadora de corriente para evitar daños en el dispositivo y garantizar un funcionamiento adecuado de las salidas GPIO.

---

## Configuración de la Raspberry Pi

### Instalación del sistema operativo

La configuración comienza con la instalación de Raspberry Pi OS Lite de 64 bits en la tarjeta microSD de la Raspberry Pi Zero 2W. Para realizar este procedimiento se utiliza Raspberry Pi Imager, herramienta que permite seleccionar el modelo de Raspberry Pi, descargar el sistema operativo correspondiente y realizar la instalación directamente sobre la tarjeta de memoria.

Antes de iniciar la escritura del sistema operativo, se configuran los parámetros necesarios para facilitar el acceso remoto posterior a la Raspberry Pi. En este proyecto se estableció el nombre de host `raspberrypi`, se configuró el usuario `indebidos` y se habilitó el servicio SSH mediante autenticación por contraseña. También se configuraron los datos de la red Wi-Fi a la que se conectaría la tarjeta durante su funcionamiento.

Esta configuración permite que, una vez instalada la tarjeta microSD en la Raspberry Pi y conectada la alimentación, el sistema operativo pueda iniciar y conectarse a la red inalámbrica sin necesidad de utilizar un monitor, teclado o mouse conectados directamente a la tarjeta.

Una vez finalizado el proceso de grabación y verificación de la tarjeta microSD, esta se instala en la Raspberry Pi Zero 2W y se procede a iniciar el sistema.

---

## Acceso remoto mediante SSH

Después de iniciar la Raspberry Pi y establecer su conexión con la red Wi-Fi configurada, se utiliza el protocolo SSH para acceder remotamente a la terminal del sistema.

Para establecer la conexión es necesario conocer la dirección IP asignada a la Raspberry Pi dentro de la red local. Desde un computador con Windows se puede utilizar PowerShell o Windows Terminal para iniciar la sesión SSH utilizando el usuario configurado previamente.

Una vez establecida la conexión, es posible administrar completamente la Raspberry Pi desde la terminal del computador. Esto permite instalar las herramientas necesarias, configurar los servicios del sistema y ejecutar los programas del proyecto sin necesidad de utilizar periféricos conectados directamente a la tarjeta.

Este método de trabajo corresponde a una configuración denominada *headless*, en la cual la Raspberry Pi funciona sin una interfaz gráfica ni dispositivos de entrada conectados de forma permanente.

---

## Entorno de desarrollo en Python

Para ejecutar el programa de control se utiliza Python. Con el objetivo de mantener separadas las dependencias del proyecto de los paquetes instalados globalmente en el sistema operativo, se crea un entorno virtual utilizando `venv`.

El entorno virtual proporciona un espacio independiente para instalar y administrar las librerías utilizadas por el proyecto. Esta configuración facilita la organización del software y permite mantener una instalación reproducible en caso de que el proyecto deba ser implementado nuevamente.

Dentro del entorno virtual se instalan las dependencias necesarias para la comunicación Bluetooth y el control de los dispositivos conectados a los GPIO.

La implementación utiliza principalmente Python junto con las librerías BlueDot y GPIO Zero. GPIO Zero proporciona una interfaz sencilla para controlar los dispositivos electrónicos conectados a la Raspberry Pi, mientras que la configuración Bluetooth permite establecer la comunicación inalámbrica necesaria para recibir los comandos de control.

---

## Configuración de la comunicación Bluetooth

La comunicación inalámbrica del sistema se implementa mediante Bluetooth clásico utilizando el protocolo RFCOMM. Este protocolo permite establecer una comunicación de tipo serial entre la Raspberry Pi y el dispositivo móvil.

Para gestionar la comunicación Bluetooth en el sistema operativo se utiliza BlueZ, la pila de protocolos Bluetooth implementada en Linux. La configuración del servicio Bluetooth es necesaria para permitir que el programa desarrollado en Python pueda utilizar sockets RFCOMM y establecer la conexión con el dispositivo externo.

Una vez realizada la configuración correspondiente del servicio BlueZ, se reinicia el servicio Bluetooth para aplicar los cambios. Posteriormente, la Raspberry Pi queda preparada para establecer una conexión con el dispositivo móvil mediante Bluetooth.

El emparejamiento se realiza desde la configuración Bluetooth del dispositivo móvil. Una vez que ambos dispositivos han sido vinculados correctamente, se utiliza la aplicación Serial Bluetooth Terminal para enviar los comandos de control hacia la Raspberry Pi.

---

## Conexión de los actuadores

Los actuadores utilizados para comprobar el funcionamiento del sistema son cinco LEDs conectados a diferentes pines GPIO de la Raspberry Pi Zero 2W.

Cada salida GPIO controla un LED y la conexión se realiza utilizando una resistencia limitadora de corriente. Los cinco dispositivos son gestionados desde el programa mediante la librería GPIO Zero, lo que permite tratarlos como un conjunto y recorrerlos de forma secuencial.

El objetivo de esta configuración es generar una secuencia luminosa en la que los LEDs se encienden uno después de otro, produciendo un efecto de desplazamiento o cascada.

La selección de los LEDs como actuadores permite visualizar fácilmente las acciones ejecutadas por el sistema. Sin embargo, la misma lógica de control puede utilizarse como base para manejar otros dispositivos conectados a los GPIO, siempre que se utilicen los circuitos de interfaz y protección adecuados.

---

## Funcionamiento del sistema de control

El programa principal del proyecto tiene dos funciones fundamentales: mantener la comunicación Bluetooth con el dispositivo móvil y controlar los actuadores conectados a los GPIO.

Al iniciar la ejecución, el programa configura los cinco LEDs y establece la lógica necesaria para controlar la secuencia luminosa. Paralelamente, se inicia un hilo de ejecución independiente encargado de ejecutar continuamente el comportamiento de los LEDs.

Mientras el hilo de control se encarga de la secuencia luminosa, el proceso principal permanece disponible para recibir información mediante la conexión Bluetooth RFCOMM.

Cuando se establece la comunicación, el programa recibe los mensajes enviados desde la aplicación Serial Bluetooth Terminal. Cada mensaje es interpretado como una instrucción de control y, dependiendo de su contenido, se modifica el estado de funcionamiento del sistema.

Para esta implementación se definieron dos comandos principales:

- `avanzar`: activa la ejecución de la secuencia luminosa.
- `detener`: interrumpe la secuencia y apaga los cinco LEDs.

Cuando se recibe el comando `avanzar`, el sistema cambia su estado de funcionamiento y permite que el hilo encargado del control de los LEDs ejecute la secuencia.

Por otra parte, cuando se recibe el comando `detener`, el estado de funcionamiento cambia a inactivo y los LEDs son apagados. La secuencia cuenta con comprobaciones periódicas del estado del sistema, por lo que puede interrumpirse rápidamente cuando se recibe la orden de detener el funcionamiento.

Si se recibe un mensaje diferente de los comandos establecidos, este se identifica como una instrucción no reconocida y no genera ninguna acción sobre los actuadores.

---

## Ejecución concurrente mediante hilos

El uso de hilos de ejecución es una parte importante de la arquitectura del sistema. La Raspberry Pi debe ser capaz de ejecutar la secuencia luminosa y, al mismo tiempo, permanecer disponible para recibir nuevos comandos mediante Bluetooth.

Para lograrlo, el programa utiliza un hilo independiente que ejecuta la función encargada de controlar los LEDs. De esta manera, la comunicación Bluetooth continúa funcionando mientras la secuencia luminosa se encuentra activa.

El estado del sistema se controla mediante una variable que indica si la secuencia debe estar ejecutándose o permanecer detenida. El hilo encargado de las luces consulta continuamente este estado y actúa de acuerdo con su valor.

Cuando el sistema se encuentra detenido, los LEDs permanecen apagados. Cuando se recibe una orden de activación, el hilo comienza a recorrer la secuencia de iluminación.

Esta estructura permite que el sistema responda de manera rápida a los comandos recibidos, evitando que la ejecución de la secuencia bloquee la comunicación Bluetooth.

---

## Secuencia luminosa

La secuencia implementada consiste en encender los cinco LEDs de manera consecutiva. Cada LED permanece encendido durante un intervalo determinado y posteriormente se apaga antes de continuar con el siguiente.

El programa utiliza diferentes tiempos de espera para modificar progresivamente la velocidad de la secuencia. De esta manera, el efecto visual comienza con una velocidad más lenta y posteriormente aumenta su rapidez.

Para la velocidad más alta se realizan un mayor número de repeticiones con el objetivo de que el efecto pueda apreciarse correctamente antes de continuar con la siguiente etapa de la secuencia.

La ejecución continúa mientras el sistema permanezca en estado activo. En el momento en que se recibe el comando `detener`, la secuencia se interrumpe y los cinco LEDs se apagan.

---

## Comunicación entre el dispositivo móvil y la Raspberry Pi

La comunicación Bluetooth funciona como la interfaz entre el usuario y el sistema de control. El dispositivo móvil se utiliza para enviar instrucciones, mientras que la Raspberry Pi recibe y procesa dichas instrucciones para generar acciones sobre los dispositivos conectados a sus GPIO.

El flujo general de información puede representarse de la siguiente manera:

**Dispositivo móvil → Bluetooth RFCOMM → Raspberry Pi → Procesamiento del comando → GPIO → Actuador**

En la implementación desarrollada, el funcionamiento es:

**Dispositivo móvil → Comando Bluetooth → Raspberry Pi → Procesamiento → GPIO → LEDs**

Esta arquitectura permite controlar el sistema de forma inalámbrica y separar la interfaz de usuario de la lógica de control. El usuario únicamente necesita enviar el comando correspondiente y la Raspberry Pi se encarga de interpretar la instrucción y ejecutar la acción asociada.

---

## Aplicación a sensores y actuadores

Aunque la implementación realizada utiliza cinco LEDs como actuadores de prueba, la arquitectura desarrollada puede utilizarse como base para aplicaciones de automatización y sistemas embebidos.

En una aplicación orientada al control de actuadores, los comandos recibidos mediante Bluetooth podrían utilizarse para activar o desactivar relés, motores, servomotores u otros dispositivos conectados a la Raspberry Pi mediante circuitos de interfaz adecuados.

De igual manera, el sistema puede ampliarse para incorporar sensores. En este caso, la Raspberry Pi podría adquirir información de los sensores conectados, procesar los datos obtenidos y transmitir los resultados mediante Bluetooth hacia el dispositivo móvil.

El flujo de información podría establecerse en ambos sentidos:

**Control de actuadores:**

`Dispositivo móvil → Bluetooth → Raspberry Pi → Procesamiento → Actuadores`

**Lectura de sensores:**

`Sensores → Raspberry Pi → Procesamiento → Bluetooth → Dispositivo móvil`

La combinación de ambas funciones permitiría desarrollar sistemas en los que el usuario pueda enviar instrucciones de control y, simultáneamente, recibir información del estado de diferentes variables físicas.

Por esta razón, la implementación desarrollada puede considerarse como una base para aplicaciones de automatización, robótica, sistemas embebidos e Internet de las Cosas.

---

## Arquitectura general del sistema

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
