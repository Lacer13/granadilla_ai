# Sistema de deteccion y clasificacion de granadillas

Proyecto basado en Raspberry Pi, OpenCV y modelos YOLO Tiny para la deteccion, clasificacion y medicion de granadillas.

## Objetivo

Desarrollar un sistema de vision artificial capaz de detectar granadillas, clasificar su estado visual y estimar su tamano mediante procesamiento de imagenes.

## Modelos evaluados inicialmente

- YOLOv3-Tiny
- YOLOv4-Tiny

## Resultado inicial de benchmark

- YOLOv3-Tiny 320x320: 7.39 FPS
- YOLOv3-Tiny 416x416: 3.21 FPS
- YOLOv4-Tiny 320x320: 6.46 FPS
- YOLOv4-Tiny 416x416: 3.26 FPS

## Decision inicial

Modelo base inicial: YOLOv3-Tiny a 320x320.

## Estructura del proyecto

- scripts/: codigos Python
- models/: configuraciones y modelos YOLO Tiny
- dataset/: futuro dataset etiquetado
- captures/: futuras capturas de camara
- results/: resultados generados
- notebooks/: notebooks para Google Colab
- docs/: documentacion del proyecto

## Tecnologias

- Raspberry Pi
- Python
- OpenCV
- Picamera2
- YOLOv3-Tiny
- YOLOv4-Tiny
- Google Colab
- GitHub
