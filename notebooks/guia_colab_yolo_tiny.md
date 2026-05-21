# Guia para entrenamiento en Google Colab

## Objetivo

Entrenar un modelo YOLO Tiny personalizado para detectar y clasificar granadillas usando imagenes reales.

## Clases iniciales

- granadilla_buena
- granadilla_golpeada
- granadilla_inmadura

## Flujo general

1. Capturar imagenes reales de granadillas.
2. Etiquetar imagenes en Roboflow o LabelImg.
3. Exportar dataset en formato YOLO Darknet.
4. Subir dataset a Google Drive o descargarlo desde Roboflow.
5. Clonar Darknet en Google Colab.
6. Compilar Darknet con GPU y OpenCV.
7. Configurar archivos de entrenamiento.
8. Entrenar YOLOv3-Tiny o YOLOv4-Tiny.
9. Descargar pesos entrenados .weights.
10. Copiar los pesos finales a la Raspberry Pi.
11. Probar el modelo con OpenCV DNN.

## Modelo base inicial

- YOLOv3-Tiny 320x320

## Modelo alternativo

- YOLOv4-Tiny 320x320

## Nota

Por ahora no se entrena porque aun no se tienen imagenes reales ni etiquetas.
