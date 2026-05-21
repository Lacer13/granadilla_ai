# Plantilla Colab - Entrenamiento YOLO Tiny para granadillas

Esta plantilla servira como base para entrenar YOLOv3-Tiny o YOLOv4-Tiny cuando ya se tenga el dataset etiquetado.

## 1. Activar GPU en Colab

En Google Colab:

Runtime > Change runtime type > GPU

## 2. Clonar Darknet

Comandos futuros en Colab:

!git clone https://github.com/AlexeyAB/darknet.git
%cd darknet

## 3. Configurar Darknet con GPU y OpenCV

Comandos futuros en Colab:

!sed -i 's/GPU=0/GPU=1/' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile
!make

## 4. Clases del proyecto

granadilla_buena
granadilla_golpeada
granadilla_inmadura

## 5. Estructura esperada del dataset

El dataset exportado debe contener imagenes y etiquetas en formato YOLO Darknet.

Ejemplo de estructura:

obj/
  imagen1.jpg
  imagen1.txt
  imagen2.jpg
  imagen2.txt

Cada archivo .txt debe tener el mismo nombre que su imagen.

Formato de cada etiqueta YOLO:

class_id x_center y_center width height

Los valores deben estar normalizados entre 0 y 1.

## 6. Entrenamiento futuro

Cuando el dataset ya este listo, se entrenara con comandos similares a los siguientes.

Para YOLOv3-Tiny:

!./darknet detector train data/obj.data cfg/yolov3-tiny-custom.cfg darknet53.conv.74 -dont_show -map

Para YOLOv4-Tiny:

!./darknet detector train data/obj.data cfg/yolov4-tiny-custom.cfg yolov4-tiny.conv.29 -dont_show -map

## 7. Resultado esperado

Al finalizar el entrenamiento, Darknet generara pesos en la carpeta backup/.

Ejemplos de archivos finales:

yolov3-tiny-custom_best.weights
yolov4-tiny-custom_best.weights

Estos pesos finales se copiaran a la Raspberry Pi para hacer inferencia con OpenCV DNN.

## 8. Uso en Raspberry Pi

La Raspberry Pi no entrenara el modelo principal.

La Raspberry Pi se usara para:

- Capturar imagenes.
- Ejecutar inferencia.
- Medir tamano con OpenCV.
- Mostrar resultados en la interfaz.
- Controlar el sistema de clasificacion.

