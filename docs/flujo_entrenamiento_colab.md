# Flujo de entrenamiento YOLO Tiny para granadillas

## Objetivo

Entrenar un modelo YOLO Tiny personalizado para detectar y clasificar granadillas segun su estado visual.

## Clases iniciales

1. granadilla_buena
2. granadilla_golpeada
3. granadilla_inmadura

# Flujo de entrenamiento YOLO Tiny para granadillas

## Objetivo

Entrenar un modelo YOLO Tiny personalizado para detectar y clasificar granadillas segun su estado visual.

## Clases iniciales

1. granadilla_buena
2. granadilla_golpeada
3. granadilla_inmadura

## 1. Captura de imagenes

Las imagenes se capturaran con la Raspberry Pi y la camara.

Recomendaciones:

- Usar fondo uniforme.
- Mantener distancia fija entre camara y granadilla.
- Evitar sombras fuertes.
- Evitar imagenes borrosas.
- Capturar diferentes orientaciones del fruto.
- Tomar imagenes con diferentes condiciones de luz.

## 2. Organizacion inicial

Las imagenes se organizaran inicialmente en carpetas:

- captures/buenas
- captures/golpeadas
- captures/inmaduras
- captures/pruebas

Luego, las imagenes seleccionadas se etiquetaran y exportaran en formato YOLO.

## 3. Etiquetado

Las imagenes se etiquetaran usando Roboflow o LabelImg.

Cada granadilla debe tener una caja delimitadora alrededor del fruto.

Las etiquetas deben coincidir con las clases:

- granadilla_buena
- granadilla_golpeada
- granadilla_inmadura

## 4. Entrenamiento en Google Colab

El entrenamiento se realizara en Google Colab porque la Raspberry Pi no es ideal para entrenar modelos pesados.

En Colab se realizara el siguiente flujo:

1. Activar GPU.
2. Clonar Darknet.
3. Compilar Darknet con GPU y OpenCV.
4. Cargar el dataset exportado.
5. Configurar YOLOv3-Tiny o YOLOv4-Tiny.
6. Entrenar el modelo.
7. Descargar los pesos finales.

## 5. Prueba en Raspberry Pi

Despues del entrenamiento, los archivos .weights se copiaran a la Raspberry Pi.

La inferencia se realizara usando OpenCV DNN con los archivos:

- .cfg
- .weights
- .names

La Raspberry Pi ejecutara:

- deteccion de granadilla
- clasificacion de estado
- medicion de tamano con OpenCV
- visualizacion en interfaz

## 6. Decision tecnica inicial

Segun las pruebas iniciales en Raspberry Pi:

- YOLOv3-Tiny 320x320 obtuvo mayor velocidad.
- YOLOv4-Tiny 320x320 queda como modelo alternativo.

Modelo base inicial:

- YOLOv3-Tiny 320x320

Modelo alternativo:

- YOLOv4-Tiny 320x320

