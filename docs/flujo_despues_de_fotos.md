# Flujo despues de tomar fotos

## Objetivo

Esta guia explica que hacer despues de capturar imagenes de granadillas con la Raspberry Pi.

## Flujo general

1. Capturar fotos por clase.
2. Revisar fotos borrosas o mal iluminadas.
3. Eliminar imagenes inutiles.
4. Contar imagenes por clase.
5. Comprimir la carpeta captures.
6. Subir imagenes a Roboflow o LabelImg.
7. Etiquetar cada granadilla con cajas delimitadoras.
8. Exportar dataset en formato YOLO Darknet.
9. Entrenar modelo en Google Colab.
10. Descargar pesos entrenados.
11. Probar pesos en Raspberry Pi.

## Revision de calidad de imagen

Antes de etiquetar, revisar que las imagenes cumplan:

- La granadilla debe verse completa.
- La imagen no debe estar borrosa.
- La iluminacion debe permitir ver manchas, golpes o coloracion.
- El fondo debe diferenciarse del fruto.
- No debe haber sombras fuertes que oculten defectos.
- No mezclar clases en carpetas incorrectas.

Imagenes que deben eliminarse:

- Fotos movidas.
- Fotos oscuras.
- Fotos sobreexpuestas.
- Fotos donde la granadilla aparece cortada.
- Fotos donde no se distingue el estado real del fruto.

## Flujo Roboflow, Colab y Raspberry

### En Roboflow o LabelImg

- Subir imagenes.
- Etiquetar cada granadilla.
- Usar las clases:
  - granadilla_buena
  - granadilla_golpeada
  - granadilla_inmadura
- Exportar en formato YOLO Darknet.

### En Google Colab

- Abrir el notebook:
  notebooks/yolo_tiny_granadilla_training.ipynb
- Cargar el dataset exportado.
- Entrenar YOLOv3-Tiny o YOLOv4-Tiny.
- Descargar el mejor archivo .weights.

### En Raspberry Pi

- Copiar el archivo .weights entrenado.
- Copiar el archivo .cfg personalizado.
- Copiar el archivo .names.
- Probar inferencia con OpenCV DNN.
- Comparar FPS y tiempo de inferencia.

