import librosa
import soundfile as sf
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore') 

DIR_ENTRADA = '/content/drive/MyDrive/2026-1/Indebidos/datos/ruido_seg'
DIR_SALIDA = '/content/drive/MyDrive/2026-1/Indebidos/entreno/ruido'

os.makedirs(DIR_SALIDA, exist_ok=True)

SAMPLE_RATE = 16000

def cambiar_tono(data, sample_rate, pasos):
    return librosa.effects.pitch_shift(y=data, sr=sample_rate, n_steps=pasos)

def cambiar_velocidad(data, factor, muestras_objetivo=16000):
    data_modificada = librosa.effects.time_stretch(y=data, rate=factor)

    if len(data_modificada) > muestras_objetivo:
        return data_modificada[:muestras_objetivo]
    else:
        return np.pad(data_modificada, (0, muestras_objetivo - len(data_modificada)), 'constant')

def cambiar_volumen(data, factor):
    data_modificada = data * factor
    return np.clip(data_modificada, -1.0, 1.0)

archivos = [f for f in os.listdir(DIR_ENTRADA) if f.endswith('.wav')]
contador = 0

print(f"Se encontraron {len(archivos)} audios. Iniciando aumento de datos...")

for archivo in archivos:
    ruta_audio = os.path.join(DIR_ENTRADA, archivo)
    nombre_base = os.path.splitext(archivo)[0]
  
    data, sr = librosa.load(ruta_audio, sr=SAMPLE_RATE)
    sf.write(os.path.join(DIR_SALIDA, f"{nombre_base}_original.wav"), data, SAMPLE_RATE)

    data_grave = cambiar_tono(data, SAMPLE_RATE, pasos=-2)
    sf.write(os.path.join(DIR_SALIDA, f"{nombre_base}_grave.wav"), data_grave, SAMPLE_RATE)

    data_lento = cambiar_velocidad(data, factor=0.85)
    sf.write(os.path.join(DIR_SALIDA, f"{nombre_base}_lento.wav"), data_lento, SAMPLE_RATE)

    data_rapido = cambiar_velocidad(data, factor=1.15)
    sf.write(os.path.join(DIR_SALIDA, f"{nombre_base}_rapido.wav"), data_rapido, SAMPLE_RATE)

    data_fuerte = cambiar_volumen(data, factor=1.5)
    sf.write(os.path.join(DIR_SALIDA, f"{nombre_base}_fuerte.wav"), data_fuerte, SAMPLE_RATE)

    contador += 5 

print(f"¡Proceso terminado! Ahora tienes {contador} audios en la carpeta '{DIR_SALIDA}'.")
