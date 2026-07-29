### Modelo de IA entrenado para reconocer audio

# Recoleccion de datos

Se le pidio a familiares, amigos y conocidos que mandaran un audio diciendo la palabra "Abrir" y otro diciendo cualquier otra palabra que termienara en "-ir", como puede ser "adquirir", "parir", "cubrir", etc. 

# Post procesamiento

Como cada una de las personas utilizaron el microfono de su celular, que es un smarth phone moderno y claramente cuenta con un microfono distinto al del microcontrolador que es el MAX4466, por lo tanto se opto por grabar nuevamente todos los audios, pero esta vez utilizando el altavoz de un mismo celular, acercandolo al microfono del microcontrolador y grabando el audio con las variables que va entender el microfono.  
Todos estos nuevos audios se guardaron en archivos .wav que es el mas sencillo de procesar y es el que permite colab, se guardaron los audios en dos carpetas, la primera carpeta se llama "Abrir" y donde se guardaron todos los audios de las personas que dijieron esta palabra y la segunda carpeta de nombre "Ruido", que es la que contiene todos los demas audios que no dijieran la palabra clave.  

# Entrenamiento

Para entrenar una IA con audio se tienen dos caminos, entrenar la IA con los audios tal cual se tomaron o tomar esos audio y aplicarl la transformada de Fourier a cada uno de esos audios para pasarlos en terminos de frecuencia y amplitud, 
