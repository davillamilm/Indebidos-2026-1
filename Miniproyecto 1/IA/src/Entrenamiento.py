import tensorflow as tf
from tensorflow.keras import layers, models

from google.colab import drive
drive.mount('/content/drive')
rutas_archivos = tf.data.Dataset.list_files('/content/drive/MyDrive/2026-1/Indebidos/entrenamiento/*/*.wav')
clases = ['abrir', 'ruido']

def get_spectrogram(waveform):
  
    zero_padding = tf.zeros([16000] - tf.shape(waveform), dtype=tf.float32)
    waveform = tf.cast(waveform, tf.float32)
    equal_length = tf.concat([waveform, zero_padding], 0)

    spectrogram = tf.signal.stft(equal_length, frame_length=255, frame_step=128)
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.expand_dims(spectrogram, -1)
    spectrogram = tf.image.resize(spectrogram, [64, 64])

    return spectrogram

def procesar_audio(ruta_archivo):
  partes_ruta = tf.strings.split(ruta_archivo, '/')
  etiqueta = partes_ruta[-2]
  etiqueta_numero = tf.argmax(etiqueta == clases)

  crudo = tf.io.read_file(ruta_archivo)
  audio, _ = tf.audio.decode_wav(crudo, desired_channels=1,desired_samples=16000)
  audio = tf.squeeze(audio, axis=-1)
  audio = get_spectrogram(audio)

  return audio, etiqueta_numero

  dataset = rutas_archivos.map(procesar_audio, num_parallel_calls=tf.data.AUTOTUNE)
dataset = dataset.batch(32)

modelo = models.Sequential([
    layers.Input(shape=(64, 64, 1)),
    layers.Resizing(32, 32),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(), # Added Flatten layer
    layers.Dense(len(clases), activation = 'softmax')
])

modelo.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("Iniciando entrenamiento.....")
historial = modelo.fit(dataset, epochs=90)

converter = tf.lite.TFLiteConverter.from_keras_model(modelo) # Declarar TFLite y el modelo de Keras entrenado
tflite_model = converter.convert()

open("arduino_model.tflite", "wb").write(tflite_model) # Guardar el modelo TFLite
!echo "const unsigned char model [] = {" > /content/open64_final.h
!cat arduino_model.tflite | xxd -i >> /content/open64_final.h
!echo "};" >> /content/open64_final.h
