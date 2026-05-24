# Guia rapida para captura de imagenes

## Objetivo

Esta guia explica como capturar imagenes de granadillas usando la Raspberry Pi para crear el dataset del proyecto.

## Antes de empezar

Verificar:

- Raspberry Pi encendida.
- Camara conectada.
- Raspberry conectada a la red.
- Acceso por VNC funcionando.
- Proyecto ubicado en: /home/pi/granadilla_ai

## 1. Entrar al proyecto

Abrir una terminal y ejecutar:

cd ~/granadilla_ai
source venv/bin/activate

## 2. Capturar una imagen de prueba

python scripts/capture_single_image.py --class-name prueba

La imagen se guardara en:

captures/pruebas/

## 3. Capturar imagenes por clase

### Granadillas buenas

python scripts/capture_dataset_images.py --class-name buena --count 30 --interval 2

### Granadillas golpeadas

python scripts/capture_dataset_images.py --class-name golpeada --count 30 --interval 2

### Granadillas inmaduras

python scripts/capture_dataset_images.py --class-name inmadura --count 30 --interval 2

## Recomendacion

Tomar las fotos en grupos pequenos, por ejemplo 20 o 30 imagenes por vez, para poder revisar si estan bien enfocadas.

## 4. Recomendaciones importantes

- Usar fondo uniforme.
- Mantener distancia fija entre camara y granadilla.
- Evitar sombras fuertes.
- Evitar imagenes borrosas.
- Tomar fotos desde diferentes orientaciones.
- Capturar imagenes con buena iluminacion.
- No mezclar clases en la misma carpeta.
- Revisar las fotos antes de subirlas a Roboflow.

## 5. Carpetas de salida

Las imagenes se guardaran en:

- captures/buenas/
- captures/golpeadas/
- captures/inmaduras/
- captures/pruebas/

## 6. Contar imagenes capturadas

Para revisar cuantas imagenes hay por clase:

python scripts/count_captures.py

Esto mostrara el total de imagenes en:

- buenas
- golpeadas
- inmaduras
- pruebas


## 7. Menu interactivo de captura

Para evitar escribir comandos largos, se puede usar el menu interactivo:

python scripts/capture_menu.py

Opciones disponibles:

1. Capturar imagen de prueba.
2. Capturar granadilla buena.
3. Capturar granadilla golpeada.
4. Capturar granadilla inmadura.
5. Captura multiple.
6. Contar imagenes capturadas.
7. Salir.

Recomendacion:

Antes de capturar imagenes reales, probar primero la opcion 1 con una imagen de prueba y luego revisar la carpeta captures/pruebas/.

## 8. Comprimir imagenes capturadas

Cuando se terminen de tomar fotos, ejecutar:

python scripts/package_captures.py

El archivo comprimido se guardara en:

exports/

Ese archivo ZIP puede subirse a Google Drive, Roboflow o enviarse para etiquetado.

## 9. Registrar sesion de captura

Despues de cada sesion, actualizar el archivo:

dataset_management/control_capturas.csv

Registrar:

- fecha
- responsable
- clase
- cantidad de fotos
- lugar
- iluminacion
- observaciones

## Vista en vivo de la camara

Antes de capturar fotos reales, se recomienda abrir la vista en vivo:

python scripts/live_camera_preview.py

Tambien se puede abrir desde el menu:

python scripts/capture_menu.py

Opcion recomendada:

1. Ver camara en vivo

Durante la vista en vivo:

- Presionar q para salir.
- Presionar ESC para salir.
- Presionar s para guardar una imagen de prueba.
- Presionar r para reenfocar.

La vista en vivo sirve para:

- acomodar la granadilla
- revisar enfoque
- revisar iluminacion
- revisar sombras
- revisar distancia camara-fruta
- verificar que el fondo sea uniforme

Antes de capturar el dataset real, usar primero la vista en vivo y ajustar la posicion de la granadilla.

## Captura desde vista en vivo con teclas

La vista en vivo permite acomodar la granadilla y guardar la imagen presionando una tecla.

Ejecutar:

python scripts/live_camera_preview.py

Teclas disponibles:

- 1: guardar como granadilla buena
- 2: guardar como granadilla golpeada
- 3: guardar como granadilla inmadura
- 4: guardar como prueba
- r: reenfocar
- q: salir
- ESC: salir

Importante:

Para que las teclas funcionen, primero hacer clic sobre la ventana de la camara.

Esta opcion es recomendada cuando se desea acomodar manualmente la granadilla y capturarla en diferentes posiciones.

## Resolucion y calidad de imagen

La Raspberry Pi Camera Module 3 permite capturar imagenes de alta resolucion.

Presets disponibles en los scripts:

- hd: 1280 x 720
- fhd: 1920 x 1080
- qhd: 2304 x 1296
- full: 4608 x 2592

Recomendacion:

- Usar hd para vista en vivo.
- Usar fhd para capturar el dataset.
- Usar qhd si se necesita ver mejor manchas o golpes.
- Usar full solo para pruebas puntuales, porque genera archivos mas pesados y puede ser mas lento.

Ejemplo captura Full HD:

python scripts/capture_dataset_images.py --class-name buena --count 30 --interval 2 --resolution fhd --focus-mode continuous

Ejemplo captura con mas detalle:

python scripts/capture_dataset_images.py --class-name buena --count 30 --interval 2 --resolution qhd --focus-mode continuous

## Seleccion rapida de calidad desde el menu

Al abrir la vista en vivo desde el menu, se puede seleccionar la calidad con un numero:

1. HD    1280 x 720    rapido
2. FHD   1920 x 1080   recomendado para dataset
3. QHD   2304 x 1296   mas detalle
4. FULL  4608 x 2592   maxima calidad, mas lento

Recomendacion:

- Usar HD solo para acomodar rapidamente.
- Usar FHD para capturar el dataset.
- Usar QHD si se necesita ver mejor manchas o golpes.
- Usar FULL solo para pruebas puntuales.

Dentro de la ventana en vivo:

- 1 guarda como granadilla buena.
- 2 guarda como granadilla golpeada.
- 3 guarda como granadilla inmadura.
- 4 guarda como prueba.
- r reenfoca.
- q sale.
