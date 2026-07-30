### Modelo de IA entrenado para reconocer audio

# Recoleccion de datos

Se le pidio a familiares, amigos y conocidos que mandaran un audio diciendo la palabra "Abrir" y otro diciendo cualquier otra palabra que termienara en "-ir", como puede ser "adquirir", "parir", "cubrir", etc. 

# Post procesamiento

Como cada una de las personas utilizaron el microfono de su celular, que es un smarth phone moderno y claramente cuenta con un microfono distinto al del microcontrolador que es el MAX4466, por lo tanto se opto por grabar nuevamente todos los audios, pero esta vez utilizando el altavoz de un mismo celular, acercandolo al microfono del microcontrolador y grabando el audio con las variables que va entender el microfono.  
Todos estos nuevos audios se guardaron en archivos .wav que es el mas sencillo de procesar y es el que permite colab, se guardaron los audios en dos carpetas, la primera carpeta se llama "Abrir" y donde se guardaron todos los audios de las personas que dijieron esta palabra y la segunda carpeta de nombre "Ruido", que es la que contiene todos los demas audios que no dijieran la palabra clave "Abrir". En total se lograron obtener 23 datos de "Abrir" y 17 de "Ruido".

### Entrenamiento

# Tipo de entrenamiento

Para entrenar una IA con audio se tienen dos caminos, entrenamiento con los audios en crudo o tomar estos audios y aplicarles la transformada de Fourier a cada uno de estos para pasarlos en términos de frecuencia y amplitud. Ambos caminos se intentaron pero el que mostro unos resultados mas solidos con los pocos datos que se tenían, el entrenamiento con los audios en crudo era muy deficiente, ya que el cambio de voz y el volumen con el que mencionaran la palabra hacia que lo datos cambiaran mucho, por otro lado el método de volverlos imágenes y la transformada de Fourier, hacia que para la IA el patrón fuera mas reconocible ya que tanto las vocales y consonantes dejan una huella reconocible para la IA cuando el audio esta en función de la frecuencia. 

# Recorte de audios

Dado que cada persona se tomaba su tiempo para decir la palabra "Abrir" al momento de grabar el Audio la ventana era de 2 segundos, posteriormente cuando ya se tenian todos los audios se opto por recortarlos a 1 segundo, esto ayudaria a la IA en que el lapso de reconocimiento fuera mucho menor y la validacion mucho mas rapida. Este recorte se hizo con el codigo de [Recorte](https://github.com/davillamilm/Indebidos-2026-1/blob/67e7ec42d652365bc5dccb43b2e07557b704bf3f/Miniproyecto%201/IA/src/Recorte.py) de la carpeta src.

# Aumento de datos

Posteriormente se multiplicaron la cantidad de datos en ambas ramas usando el código de [Multiplicador](https://github.com/davillamilm/Indebidos-2026-1/blob/254675ed171666eeaa0aee547c45afade63feb53/Miniproyecto%201/IA/src/Multiplicador.py) el cual consiste en a cada una de los audios sacarle variantes con la voz mas grave, aguda y con una mayor velocidad o una menor, por lo tanto el banco de datos para entrenar la IA ya era de 115 para "Abrir" y 85 para "Ruido". Todos estos archivos se guardaron en una carpeta de Drive que contenia dos carpetas, una de nombre "abrir" y otra con nombre "ruido" con los archivos que corresponden a cada uno.

# Procesar los datos

Esta función toma la ruta de un archivo de audio .wav y devuelve la tupla (espectrograma, etiqueta_numérica) lista para alimentar o entrenar un modelo de aprendizaje automático, esta funcion de llama "[procesar_audio](https://github.com/davillamilm/Indebidos-2026-1/blob/b70c28ea2291d912af3b7f39ba77e8cc5bf911fe/Miniproyecto%201/IA/src/Entrenamiento.py)". El proceso se divide en 2: 

- Obtiene la etiqueta numérica: Extrae el nombre de la carpeta que contiene el archivo (que actúa como nombre de la clase) a partir de la ruta y lo convierte en un número entero buscando su índice en la lista de clases
- Lee y procesa el audio: Carga el archivo desde el disco, decodifica el audio en mono (1 canal) a 16,000 muestras, elimina la dimensión extra del canal y llama a la función get_spectrogram() para convertir la onda sonora en la imagen final.

# Espectrogama

Como se opto por el metodo de entrenamiento que utiliza la transformada de fourier, se uso la funcion "[get_espectrograma](https://github.com/davillamilm/Indebidos-2026-1/blob/b70c28ea2291d912af3b7f39ba77e8cc5bf911fe/Miniproyecto%201/IA/src/Entrenamiento.py)" en donde esta función transforma una señal de audio cruda en una imagen de espectrograma optimizada para redes neuronales con las que la ESP32-S3 sea capaz de trabajar. Lo hace en tres pasos clave: primero, rectifica y normaliza la duración del audio a exactamente 1 segundo (16,000 muestras a 16 kHz) agregando ceros al final si es muy corto. Luego, aplica la Transformada de Fourier de Tiempo Reducido (STFT) y extrae su magnitud para convertir las frecuencias del sonido en una matriz visual. Por último, le añade una dimensión de canal y la redimensiona a 64x64 píxeles para que ocupe muy poca memoria y sea rápida de procesar. 

# Formacion red neuronal

Esta es la fase final de preparación de datos, arquitectura y entrenamiento de la red neuronal convolucional (CNN) en TensorFlow. la cual se divide en tre partes principales:
- Pipeline de datos (tf.data): Aplica la función procesar_audio a todas las rutas de archivo en paralelo (AUTOTUNE) para no saturar la memoria, y agrupa los espectrogramas en lotes de 32 (batch(32)) para procesarlos eficientemente.

- Definición de la Red Neuronal (CNN):
    1. Entrada y ajuste: Recibe la imagen de 64x64x1 (generada por get_spectrogram) e inmediatamente la redimensiona a 32x32 (aquí es donde se aplica el recorte para aligerar la memoria de la ESP32-S3).
    2. Extracción de características: Pasa la imagen por dos capas de convolución (Conv2D) y reducción (MaxPooling2D) para detectar patrones visuales en el audio (frecuencias y tiempos).
    3. Clasificación: Aplanar los datos (Flatten) y los pasa a una capa Dense final que calcula la probabilidad de pertenecer a cada una de las clases mediante softmax.

- Compilación y entrenamiento: Configura el modelo con el optimizador Adam y la pérdida sparse_categorical_crossentropy (ideal porque las etiquetas son números enteros), e inicia el entrenamiento (fit) ejecutando 90 pasadas completas (epochs=90) sobre los datos.

