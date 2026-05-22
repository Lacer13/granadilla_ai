# Guia rapida de captura de imagenes

## Objetivo

Capturar imagenes de granadillas para construir el dataset del modelo YOLO Tiny.

## Carpetas de captura

- captures/buenas
- captures/golpeadas
- captures/inmaduras
- captures/pruebas

## Captura individual

Ejemplo:

python scripts/capture_single_image.py --class-name prueba

## Captura multiple

Ejemplo:

python scripts/capture_dataset_images.py --class-name buena --count 20 --interval 2

## Recomendaciones

- Usar fondo uniforme.
- Evitar sombras fuertes.
- Mantener distancia fija entre camara y granadilla.
- Evitar imagenes borrosas.
- Capturar diferentes orientaciones del fruto.
- Tomar imagenes con diferentes condiciones de iluminacion.
- Revisar visualmente las fotos antes de etiquetarlas.
