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

