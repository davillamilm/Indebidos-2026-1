### Limitaciones y Reglas de Fabricación de la PCB

A continuación se detallan los parámetros y restricciones técnicas para la fabricación de placas en el laboratorio de prototipado:

#### Especificaciones de Diseño
* **Ancho mínimo de pistas:** `0.6 mm` (`30 th`)
* **Separación mínima (pistas y pads):** `0.5 mm` (`20 th` aprox.)
* **Perforaciones de sujeción:** Se deben agregar orificios de `3 mm` para facilitar la alineación en fabricación y sujeción del proyecto.
* **Tamaño máximo de placa:** `120 x 100 mm`
* **Sustrato / Material:** FR4 (fibra de vidrio) de `1.6 mm` con capa de cobre de `34 µm` ($\text{Er} = 4.3$)

#### Restricciones Generales
* **Capa doble:** **NO** se manufacturan PCBs de doble cara.
* **Archivos:** Solo se aceptan los formatos solicitados (`.pdf`, `.gbr`, `.drl`).

#### Archivos Requeridos para Envío
1. **Capa Bottom** (*con mirror*) $\rightarrow$ `.PDF`
2. **Capa Soldermask** (*con mirror*) $\rightarrow$ `.PDF`
3. **Capa Edgecut** $\rightarrow$ `.PDF`
4. **Capa Silkscreen** $\rightarrow$ `.PDF`
5. **Gerber Edgecut** $\rightarrow$ `.gbr`
6. **Gerber Drill** $\rightarrow$ `.drl`

Con estas especificación dadas por el labortario, este fue el resultado de la PCB en Kicad:
![PCB](https://github.com/davillamilm/Indebidos-2026-1/blob/994c40a167e61e321b9a2fb1c71cf60042479895/Microcontrolador/Funcionamineto/imagenes/PCB.png)
