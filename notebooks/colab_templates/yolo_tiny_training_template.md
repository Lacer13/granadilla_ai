# Plantilla de entrenamiento YOLO Tiny en Google Colab

Esta plantilla servira para entrenar un modelo YOLOv3-Tiny o YOLOv4-Tiny para la deteccion y clasificacion de granadillas.

## Objetivo

Entrenar un modelo personalizado capaz de detectar y clasificar granadillas en las siguientes clases:

- granadilla_buena
- granadilla_golpeada
- granadilla_inmadura

## 1. Configuracion inicial en Colab

Antes de ejecutar el entrenamiento:

1. Abrir Google Colab.
2. Ir a Runtime.
3. Seleccionar Change runtime type.
4. Elegir GPU.
5. Guardar la configuracion.

Esto permitira entrenar el modelo usando aceleracion por GPU.

## 2. Clonar y compilar Darknet

Comandos futuros en Colab:

!git clone https://github.com/AlexeyAB/darknet.git
%cd darknet

!sed -i 's/GPU=0/GPU=1/' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile
!make

## 3. Archivos necesarios del dataset

El dataset exportado debe incluir:

- Imagenes .jpg o .png
- Etiquetas .txt en formato YOLO
- obj.names
- obj.data
- train.txt
- valid.txt

El archivo obj.names debe contener:

granadilla_buena
granadilla_golpeada
granadilla_inmadura

El archivo obj.data debe contener:

classes = 3
train = data/train.txt
valid = data/valid.txt
names = data/obj.names
backup = backup/

## 4. Entrenamiento YOLOv3-Tiny

Comando futuro para YOLOv3-Tiny:

!./darknet detector train data/obj.data cfg/yolov3-tiny-custom.cfg darknet53.conv.74 -dont_show -map

## 5. Entrenamiento YOLOv4-Tiny

Comando futuro para YOLOv4-Tiny:

!./darknet detector train data/obj.data cfg/yolov4-tiny-custom.cfg yolov4-tiny.conv.29 -dont_show -map

## 6. Archivos finales esperados

Al terminar el entrenamiento, Darknet generara archivos en la carpeta backup/.

Ejemplos:

- yolov3-tiny-custom_best.weights
- yolov4-tiny-custom_best.weights

Estos archivos se copiaran a la Raspberry Pi junto con:

- archivo .cfg personalizado
- archivo .names

## 7. Uso en Raspberry Pi

La Raspberry Pi usara OpenCV DNN para ejecutar el modelo entrenado.

Flujo en Raspberry:

1. Cargar .cfg
2. Cargar .weights
3. Cargar .names
4. Capturar imagen o video
5. Detectar granadilla
6. Clasificar estado
7. Medir tamano con OpenCV
8. Mostrar resultado en interfaz

