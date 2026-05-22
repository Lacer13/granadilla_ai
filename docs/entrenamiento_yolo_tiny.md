# Entrenamiento YOLO Tiny para granadillas

## Objetivo

Entrenar un modelo YOLOv3-Tiny o YOLOv4-Tiny personalizado para detectar y clasificar granadillas.

## Clases del proyecto

- granadilla_buena
- granadilla_golpeada
- granadilla_inmadura

## Flujo general

1. Capturar imagenes.
2. Revisar calidad de imagenes.
3. Etiquetar imagenes.
4. Exportar dataset en formato YOLO Darknet.
5. Entrenar en Google Colab.
6. Descargar pesos finales.
7. Probar en Raspberry Pi.

## 1. Preparacion del dataset

Despues de capturar las imagenes, se deben etiquetar usando Roboflow o LabelImg.

Cada imagen debe tener una caja delimitadora alrededor de la granadilla.

Las clases deben escribirse exactamente asi:

granadilla_buena
granadilla_golpeada
granadilla_inmadura

Luego se debe exportar el dataset en formato YOLO Darknet.

## 2. Estructura esperada del dataset

El dataset exportado debe tener imagenes y etiquetas en formato YOLO.

Ejemplo:

obj/
  imagen_001.jpg
  imagen_001.txt
  imagen_002.jpg
  imagen_002.txt

train.txt
valid.txt
obj.names
obj.data

Cada archivo .txt debe tener el mismo nombre que su imagen.

Ejemplo:

imagen_001.jpg
imagen_001.txt

## 3. Configuracion de YOLO Tiny

Para entrenar con 3 clases, se debe modificar el archivo .cfg.

Numero de clases:

classes = 3

Formula para filtros:

filters = (classes + 5) * 3

Para este proyecto:

filters = (3 + 5) * 3 = 24

Por eso, en las capas anteriores a cada deteccion YOLO se debe usar:

filters = 24

## 4. Entrenamiento YOLOv3-Tiny en Colab

Comando base:

./darknet detector train data/obj.data cfg/yolov3-tiny-granadilla.cfg darknet53.conv.74 -dont_show -map

Archivos necesarios:

- data/obj.data
- data/obj.names
- data/train.txt
- data/valid.txt
- cfg/yolov3-tiny-granadilla.cfg
- darknet53.conv.74

## 6. Despues del entrenamiento

Al terminar, Darknet guardara pesos en la carpeta backup/.

Archivos importantes:

- yolov3-tiny-granadilla_best.weights
- yolov4-tiny-granadilla_best.weights

Luego se deben copiar a la Raspberry Pi junto con:

- archivo .cfg personalizado
- archivo .names

Despues se prueba inferencia con OpenCV DNN.

## 7. Criterio de seleccion final

Se seleccionara el mejor modelo considerando:

- FPS en Raspberry Pi
- tiempo de inferencia
- precision
- recall
- mAP
- estabilidad con imagenes reales
- capacidad de detectar defectos o inmadurez

