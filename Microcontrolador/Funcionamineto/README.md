# Funcionamiento

Para la fabricación del microcontrolador para este proyecto, nos apoyamos del datasheet de la [ESP32-S3-WROOM-1](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf) que en su sección de "Peripheral Schematics" muestra cuales son algunas de las características que debe tener el chip de la ESP32-S3 para funcionar, en la imagen se puede ver el diseño que propone espressif, pero nosotros decidimos usar solo las partes que están encerradas en verde, ya que con estas 3 partes es suficiente para que nuestro proyecto se puede efectuar.

![aaaaaa](https://github.com/davillamilm/Indebidos-2026-1/blob/4cbfdd2ad5b5953e19191a7d7c9a1caa77f0195e/Microcontrolador/Funcionamineto/imagenes/Captura%20de%20pantalla%202026-07-28%20165501.png)


En la parte superior izquierda hace referencia de por donde va ser alimentado el chip de la ESP32-S3 donde hay condensadores que funcionan como filtro de ruido que ayuda a que no afecte el funcionamiento del chip. En la zona de la izquierda se encuentra por donde va el conector USB que permitir el paso de la información entre el chip y el computador por medio de los carriles D+ y D-. EN la derecha se encuentran los botones de boot y reset como dice la imagen.

# Desarrollo en kicad

Como fuente de alimentación de la placa se uso el mismo conector que va directo al PC, por lo tanto este va suministrar 5 V, por lo tanto es necesario un regulador de voltaje que tenga como salida 3.3 V que es lo que necesita el chip, también se agregó un led en la etapa de salida del regulador para que enseñara que la placa si estaba recibiendo alimentación. Para el proyecto se necesita 1 sensor (micrófono) y 2 actuadores (led y servo) para cada uno de estos solo se necesita un pin GPIO, para el micrófono se utilizó el GPIO 2, para el led el GPIO1 y para el servo se uso el GPIO 14. Todos los componentes necesarios conectados entre si y al chip se ven en la siguiente imagen:

