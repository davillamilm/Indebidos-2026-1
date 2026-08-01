#  Puerta Inteligente por Reconocimiento de Voz (ESP32 + Raspberry Pi Zero 2W)

Este proyecto implementa un sistema embebido de control de acceso mediante reconocimiento de voz en el borde (*Edge Computing*). El sistema utiliza un microcontrolador **ESP32** para la captura precisa de audio y la activación de los indicadores de estado, y una **Raspberry Pi Zero 2W** para procesar la señal de audio mediante una Red Neuronal Convolucional (CNN) entrenada en **TensorFlow** y optimizada en **TensorFlow Lite**.

---

##  Tabla de Contenidos
- [Descripción General](#-descripción-general)
- [Arquitectura y Hardware](#-arquitectura-y-hardware)
- [Esquema de Conexiones (Pinout ESP32)](#-esquema-de-conexiones-pinout-esp32)
- [Firmware del Microcontrolador (ESP32)](#-firmware-del-microcontrolador-esp32)
- [Modelo de Inteligencia Artificial (Python / TensorFlow)](#-modelo-de-inteligencia-artificial-python--tensorflow)
- [Explicación Detallada del Funcionamiento](#-explicación-detallada-del-funcionamiento)
  - [Funcionamiento del ESP32 (C++)](#funcionamiento-del-esp32-c)
  - [Funcionamiento del Modelo IA (Python)](#funcionamiento-del-modelo-ia-python)
- [Conclusiones](#-conclusiones)
- [Autores](#-autores)

---

##  Descripción General

El objetivo principal es permitir la apertura/validación automática de acceso cuando el usuario pronuncia la palabra clave **"abrir"**. 

1. El usuario presiona un botón físico para activar la grabación.
2. El ESP32 captura **1 segundo de audio a 16 kHz** mediante un micrófono analógico.
3. El audio en estado crudo (raw bytes) se envía por protocolo **HTTP POST** a un servidor Flask/Python alojado en la Raspberry Pi Zero 2W.
4. La Raspberry Pi convierte la señal de voz en un **espectrograma de 64x64 píxeles** (Transformada de Fourier - STFT) y ejecuta la inferencia con el modelo TensorFlow Lite.
5. Si el modelo detecta la orden `"correcto"`, el ESP32 enciende el LED indicador durante 3 segundos señalando el acceso concedido. Si detecta ruido u otra palabra, la solicitud es rechazada.

---

##  Arquitectura y Hardware

El sistema desacopla las tareas de adquisición y procesamiento en dos nodos conectados a una red WiFi local:

```
                  ┌────────────────────────┐
                  │   Botón de activación  │
                  └───────────┬────────────┘
                              │
                              ▼
  ┌───────────────────────────────────────────────────────┐
  │                    ESP32 (Nodo IoT)                   │
  │  - Captura Audio a 16 kHz (esp_timer)                 │
  │  - Envía datos binarios por HTTP POST                 │
  │  - Recibe respuesta y activa LED Indicador            │
  └───────────────────────────┬───────────────────────────┘
                              │
                              │ WiFi / HTTP (Red Local)
                              ▼
  ┌───────────────────────────────────────────────────────┐
  │            Raspberry Pi Zero 2W (Servidor IA)         │
  │  - Recibe búfer de audio octet-stream                 │
  │  - Genera Espectrograma STFT (64x64)                  │
  │  - Clasifica con modelo TensorFlow Lite (.tflite)     │
  └───────────────────────────┬───────────────────────────┘
```

### Componentes Utilizados:
* **Microcontrolador:** ESP32-WROOM-32.
* **Procesador Central / Servidor:** Raspberry Pi Zero 2W.
* **Sensor de Audio:** Micrófono analógico.
* **Entradas/Salidas:** Botón pulsador y LED indicador de acceso.

---

##  Esquema de Conexiones (Pinout ESP32)

| Componente | Pin ESP32 | Descripción |
| :--- | :--- | :--- |
| **LED Indicador** | `GPIO 1` | Salida digital para estado de apertura / acceso |
| **Micrófono Analógico** | `GPIO 2` | Entrada analógica (ADC 12 bits) |
| **Botón Pulsador** | `GPIO 9` | Entrada digital con `INPUT_PULLUP` |

---

##  Firmware del Microcontrolador (ESP32)

Código escrito en **C++** para Arduino IDE / PlatformIO.

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include "esp_timer.h"

// =====================================================
// PINES Y CONFIGURACIÓN
// =====================================================
const int PIN_LED = 1;
const int PIN_MIC = 2;
const int PIN_BOTON = 9;  

const char* ssid = "Esteban";
const char* password = "Estebantrejo2003";
const char* serverUrl = "[http://10.126.17.102:5000](http://10.126.17.102:5000)";

const uint32_t SAMPLE_RATE = 16000;
const uint32_t RECORD_TIME_SECONDS = 1;
const uint32_t NUM_SAMPLES = SAMPLE_RATE * RECORD_TIME_SECONDS;
const size_t AUDIO_BYTES = NUM_SAMPLES * sizeof(uint16_t);

uint16_t* audioBuffer = nullptr;
unsigned long tiempoInicioProceso = 0;

void conectarWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;
  Serial.print("Conectando a WiFi");
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);
  WiFi.begin(ssid, password);

  unsigned long inicioConexion = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - inicioConexion < 20000) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi conectado correctamente.");
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);
  pinMode(PIN_MIC, INPUT);
  pinMode(PIN_BOTON, INPUT_PULLUP);

  analogReadResolution(12);
  audioBuffer = (uint16_t*)malloc(AUDIO_BYTES);

  if (audioBuffer == nullptr) {
    while (true) {
      digitalWrite(PIN_LED, !digitalRead(PIN_LED));
      delay(200);
    }
  }

  conectarWiFi();
}

void capturarAudio() {
  uint16_t valorMinimo = 4095;
  uint16_t valorMaximo = 0;
  uint64_t suma = 0;
  uint64_t tiempoInicial = esp_timer_get_time();

  for (uint32_t i = 0; i < NUM_SAMPLES; i++) {
    uint64_t tiempoObjetivo = tiempoInicial + ((uint64_t)i * 1000000ULL) / SAMPLE_RATE;

    while (esp_timer_get_time() < tiempoObjetivo) {
      // Espera activa para muestreo preciso a 16 kHz
    }

    uint16_t valor = analogRead(PIN_MIC);
    audioBuffer[i] = valor;

    if (valor < valorMinimo) valorMinimo = valor;
    if (valor > valorMaximo) valorMaximo = valor;
    suma += valor;
  }
}

void enviarAudio() {
  if (WiFi.status() != WL_CONNECTED) conectarWiFi();
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(serverUrl);
  http.setTimeout(15000);
  http.addHeader("Content-Type", "application/octet-stream");
  http.addHeader("X-Sample-Rate", "16000");
  http.addHeader("X-Audio-Format", "uint16-little-endian");

  int httpResponseCode = http.POST((uint8_t*)audioBuffer, AUDIO_BYTES);

  if (httpResponseCode > 0) {
    String respuesta = http.getString();
    respuesta.trim();

    unsigned long tiempoFinalProceso = millis() - tiempoInicioProceso;
    Serial.printf("TIEMPO TOTAL: %lu ms\n", tiempoFinalProceso);

    if (respuesta == "correcto") {
      digitalWrite(PIN_LED, HIGH); // LED encendido (acceso concedido)
      delay(3000);        // Mantener estado 3 segundos
      digitalWrite(PIN_LED, LOW);
    }
  }
  http.end();
}

void loop() {
  if (digitalRead(PIN_BOTON) == LOW) {
    delay(50); // Antirrebote básico
    if (digitalRead(PIN_BOTON) == LOW) {
      tiempoInicioProceso = millis();
      delay(300);
      capturarAudio();
      enviarAudio();

      while (digitalRead(PIN_BOTON) == LOW) {
        delay(10);
      }
    }
  }

  if (WiFi.status() != WL_CONNECTED) {
    static unsigned long ultimoIntento = 0;
    if (millis() - ultimoIntento > 10000) {
      ultimoIntento = millis();
      conectarWiFi();
    }
  }
  delay(10);
}
```

---

##  Modelo de Inteligencia Artificial (Python / TensorFlow)

Script en **Python** para preprocesamiento de audio, entrenamiento de la CNN y exportación del modelo a **TensorFlow Lite**.

```python
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping
import glob
import numpy as np

# Configuración de dataset y clases
ruta_dataset = '/content/drive/MyDrive/2026-1/Indebidos/entreno/*/*.wav'
rutas_archivos = tf.data.Dataset.list_files(ruta_dataset)
total_archivos = len(glob.glob(ruta_dataset))

clases = tf.constant(['abrir', 'ruido'])

def get_spectrogram(waveform):
    # Asegurar exactamente 16000 muestras (1 segundo)
    zero_padding = tf.zeros([16000] - tf.shape(waveform), dtype=tf.float32)
    waveform = tf.cast(waveform, tf.float32)
    equal_length = tf.concat([waveform, zero_padding], 0)

    # Transformada de Fourier de Tiempo Reducido (STFT)
    spectrogram = tf.signal.stft(equal_length, frame_length=255, frame_step=128)
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.expand_dims(spectrogram, -1)
    
    # Redimensionar a imagen de 64x64 píxeles
    spectrogram = tf.image.resize(spectrogram, [64, 64])
    return spectrogram

def procesar_audio(ruta_archivo):
    partes_ruta = tf.strings.split(ruta_archivo, '/')
    etiqueta = tf.strings.lower(partes_ruta[-2])
    etiqueta_booleana = tf.math.equal(etiqueta, clases)
    etiqueta_numero = tf.argmax(tf.cast(etiqueta_booleana, tf.int32))

    crudo = tf.io.read_file(ruta_archivo)
    audio, _ = tf.audio.decode_wav(crudo, desired_channels=1, desired_samples=16000)
    audio = tf.squeeze(audio, axis=-1)
    audio = get_spectrogram(audio)
    return audio, etiqueta_numero

# División de Dataset (80% Train, 20% Val)
tamano_entrenamiento = int(total_archivos * 0.8)
dataset = rutas_archivos.shuffle(total_archivos, seed=42)
dataset = dataset.map(procesar_audio, num_parallel_calls=tf.data.AUTOTUNE)

train_dataset = dataset.take(tamano_entrenamiento).batch(8).prefetch(tf.data.AUTOTUNE)
val_dataset = dataset.skip(tamano_entrenamiento).batch(8).prefetch(tf.data.AUTOTUNE)

# Arquitectura de la CNN Ligera
modelo = models.Sequential([
    layers.Input(shape=(64, 64, 1)),

    layers.Conv2D(8, 3, padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),

    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),

    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),

    layers.GlobalAveragePooling2D(),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.6),  # Regularización para evitar over-fitting
    layers.Dense(len(clases), activation='softmax')
])

modelo.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

parada_temprana = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

historial = modelo.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=100,
    callbacks=[parada_temprana]
)

# Convertir y guardar el modelo en TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(modelo)
tflite_model = converter.convert()

nombre_archivo = "modelo_openv10.tflite"
with open(nombre_archivo, "wb") as f:
    f.write(tflite_model)
```

---

## 🔍 Explicación Detallada del Funcionamiento

### Funcionamiento del ESP32 (C++)
* **Reserva Dinámica de Memoria:** Mediante `malloc(AUDIO_BYTES)` se reservan 32,000 bytes en la memoria RAM (16,000 muestras x 2 bytes por muestra). Si no hay memoria suficiente, el sistema entra en un bucle de alerta por LED.
* **Muestreo Determinista (`esp_timer`):** Para mantener la frecuencia exacta de 16 kHz (62.5 microsegundos por muestra), el código utiliza el temporizador interno de hardware de la ESP32 en lugar de retardos comunes. Esto evita desvíos de tiempo (*jitter*) que arruinarían el espectrograma.
* **Envío Binario Rápido:** Los datos capturados no se convierten a formato JSON ni texto para no saturar la red. Se transmiten de forma cruda (`application/octet-stream`) mediante un puerto HTTP POST directo a la Raspberry Pi.
* **Control de Indicadores:** Si la respuesta recibida es `"correcto"`, el microcontrolador enciende el LED indicador durante 3 segundos para señalar la validación del comando de voz.

### Funcionamiento del Modelo IA (Python)
* **Conversión a Espectrogramas (STFT):** La función `get_spectrogram` convierte la onda de sonido temporal en una representación gráfica frecuencia-tiempo utilizando la Transformada de Fourier de Tiempo Reducido. La imagen generada se redimensiona a 64x64 píxeles en escala de grises.
* **Arquitectura CNN Optimizada:** Posee 3 bloques convolucionales (8, 16 y 32 filtros) acompañados de `BatchNormalization` y `MaxPooling2D`.
* **Prevención de Sobreajuste:** Como el conjunto de datos de voz suele ser pequeño, se incluye una capa de `Dropout(0.6)` (descarta el 60% de conexiones aleatoriamente) y una `EarlyStopping` que detiene el entrenamiento si el margen de error de validación deja de mejorar por 5 épocas seguidas.
* **TensorFlow Lite:** El archivo resultante `.tflite` es una versión comprimida que permite realizar inferencias ultra rápidas en hardware compacto como la Raspberry Pi Zero 2W.

---

##  Conclusiones

* **Desacoplamiento Efectivo:** Separar las tareas de adquisición física (ESP32) y procesamiento de Inteligencia Artificial (Raspberry Pi) garantizó un tiempo de respuesta bajo y estable dentro de una red local.
* **Muestreo por Hardware:** La utilización de los temporizadores internos del chip ESP32 permitió obtener muestras de voz a 16 kHz libres de ruido por tiempos de retardo de software.
* **Redes Convolucionales para Voz:** La transformación del audio a espectrogramas permitió tratar las señales de sonido como imágenes, aprovechando la alta precisión de las redes convolucionales livianas mediante modelos reducidos en **TensorFlow Lite**.

---

##  Autores

* **David Villamil** 
* **** - *Esteban Trejo* 
* **Juan José González** 
