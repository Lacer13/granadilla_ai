# Analisis inicial de rendimiento YOLO Tiny

## Objetivo

Comparar el rendimiento inicial de YOLOv3-Tiny y YOLOv4-Tiny en Raspberry Pi usando OpenCV DNN sobre CPU.

## Resultados iniciales

| Modelo | Entrada | Tiempo promedio (s) | Tiempo promedio (ms) | FPS |
|---|---:|---:|---:|---:|
| YOLOv3-Tiny | 320x320 | 0.1354 | 135.4 | 7.39 |
| YOLOv3-Tiny | 416x416 | 0.3119 | 311.9 | 3.21 |
| YOLOv4-Tiny | 320x320 | 0.1547 | 154.7 | 6.46 |
| YOLOv4-Tiny | 416x416 | 0.3067 | 306.7 | 3.26 |

## Interpretacion

El mejor resultado en velocidad fue YOLOv3-Tiny con entrada 320x320, alcanzando 7.39 FPS y un tiempo promedio de inferencia de 135.4 ms.

YOLOv4-Tiny con entrada 320x320 obtuvo 6.46 FPS y 154.7 ms, por lo que queda como modelo alternativo para comparar posteriormente con imagenes reales de granadillas.

## Decision inicial

Modelo base recomendado para primeras pruebas:

- YOLOv3-Tiny
- Entrada 320x320
- Backend OpenCV DNN
- Target CPU

## Nota

Estos resultados corresponden a una prueba inicial con una imagen de referencia. La decision final debera validarse con imagenes reales de granadillas.
