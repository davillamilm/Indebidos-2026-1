from google.colab import drive
drive.mount('/content/drive')

import os
import librosa
import numpy as np
import soundfile as sf

carpeta_entrada = '/content/drive/MyDrive/2026-1/Indebidos/datos/abrir'
carpeta_salida = '/content/drive/MyDrive/2026-1/Indebidos/datos/abrir_seg'
FRECUENCIA_MUESTREO = 16000
DURACION_OBJETIVO = 1.0   
TOP_DB = 25                

if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

muestras_objetivo = int(FRECUENCIA_MUESTREO * DURACION_OBJETIVO)

def procesar_audio(ruta_archivo, ruta_guardado):
    try:

        y, sr = librosa.load(ruta_archivo, sr=FRECUENCIA_MUESTREO)
        y_recortado, indices = librosa.effects.trim(y, top_db=TOP_DB)

        centro_idx = (indices[0] + indices[1]) // 2

        mitad_ventana = muestras_objetivo // 2
        inicio = centro_idx - mitad_ventana
        fin = centro_idx + mitad_ventana

        y_final = np.zeros(muestras_objetivo)

        out_inicio = max(0, -inicio)
        in_inicio = max(0, inicio)

        out_fin = muestras_objetivo - max(0, fin - len(y))
        in_fin = min(len(y), fin)

        y_final[out_inicio:out_fin] = y[in_inicio:in_fin]

        sf.write(ruta_guardado, y_final, FRECUENCIA_MUESTREO)
        print(f"Procesado con éxito: {os.path.basename(ruta_archivo)}")

    except Exception as e:
        print(f"Error procesando {ruta_archivo}: {e}")

archivos = [f for f in os.listdir(carpeta_entrada) if f.endswith(('.wav', '.mp3', '.ogg'))]

print(f"Se encontraron {len(archivos)} audios. Iniciando procesamiento...\n")

for archivo in archivos:
    ruta_in = os.path.join(carpeta_entrada, archivo)
    ruta_out = os.path.join(carpeta_salida, archivo)
    procesar_audio(ruta_in, ruta_out)

print("\n¡Procesamiento terminado! Todos los audios duran exactamente 1 segundo.")
