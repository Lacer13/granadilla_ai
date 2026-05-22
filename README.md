# Sistema de deteccion y clasificacion de granadillas

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Lacer13/granadilla_ai/blob/main/notebooks/yolo_tiny_granadilla_training.ipynb)

Proyecto basado en Raspberry Pi, OpenCV y modelos YOLO Tiny para la deteccion, clasificacion y futura medicion de tamano de granadillas.

## Objetivo general

Desarrollar un sistema de vision artificial capaz de detectar granadillas, clasificar su estado visual y estimar su tamano aproximado, usando una Raspberry Pi como plataforma de inferencia.

## Clases iniciales

- granadilla_buena
- granadilla_golpeada
- granadilla_inmadura

## Arquitectura general

El flujo propuesto del sistema es:

1. Captura de imagen con camara Raspberry Pi.
2. Deteccion de la granadilla con YOLO Tiny.
3. Clasificacion del estado visual.
4. Estimacion de tamano mediante OpenCV.
5. Visualizacion de resultados en interfaz.
6. Registro de datos para analisis posterior.

## Distribucion de trabajo

### Raspberry Pi

La Raspberry Pi se usara para:

- Captura de imagenes.
- Inferencia con OpenCV DNN.
- Pruebas de YOLOv3-Tiny y YOLOv4-Tiny.
- Medicion de tamano con OpenCV.
- Interfaz de monitoreo.
- Registro de resultados.

### Google Colab

Google Colab se usara para:

- Entrenamiento del modelo YOLO Tiny.
- Uso de GPU.
- Evaluacion del modelo entrenado.
- Generacion de pesos finales .weights.

### GitHub

GitHub se usara para:

- Control de versiones.
- Documentacion.
- Respaldo del codigo.
- Trabajo colaborativo.

## Benchmark inicial en Raspberry Pi

Se evaluaron YOLOv3-Tiny y YOLOv4-Tiny usando OpenCV DNN sobre CPU.

| Modelo | Entrada | Tiempo promedio | FPS promedio |
|---|---:|---:|---:|
| YOLOv3-Tiny | 320x320 | 135.4 ms | 7.39 |
| YOLOv3-Tiny | 416x416 | 311.9 ms | 3.21 |
| YOLOv4-Tiny | 320x320 | 154.7 ms | 6.46 |
| YOLOv4-Tiny | 416x416 | 306.7 ms | 3.26 |

## Decision inicial

El modelo base inicial sera:

- YOLOv3-Tiny
- Entrada 320x320
- OpenCV DNN
- CPU

YOLOv4-Tiny queda como modelo alternativo para comparar cuando se tengan imagenes reales de granadillas.


## Estructura del repositorio

La organizacion principal del proyecto es la siguiente:

- `benchmarks/`: resultados de rendimiento, FPS, tiempos de inferencia y graficas.
- `captures/`: imagenes capturadas con la camara de la Raspberry Pi.
- `dataset/`: futura estructura del dataset etiquetado.
- `docs/`: documentacion tecnica del proyecto.
- `models/`: archivos de configuracion y pesos base de YOLO Tiny.
- `notebooks/`: notebooks y plantillas para Google Colab.
- `results/`: resultados generados por pruebas de deteccion.
- `scripts/`: codigos Python principales.
- `training/`: archivos base para entrenamiento con Darknet.

## Carpetas importantes

Dentro de `models/` se encuentran:

- `models/yolov3_tiny/`
- `models/yolov4_tiny/`

Dentro de `captures/` se usaran:

- `captures/buenas/`
- `captures/golpeadas/`
- `captures/inmaduras/`
- `captures/pruebas/`

Dentro de `benchmarks/` se encuentran:

- `benchmark_results.csv`
- `benchmark_analysis.md`
- `figures/`

## Scripts principales

- `scripts/detect_image_flexible.py`: permite probar YOLOv3-Tiny o YOLOv4-Tiny con cualquier imagen.
- `scripts/benchmark_yolo_tiny.py`: mide FPS y tiempo de inferencia de los modelos.
- `scripts/plot_benchmark_results.py`: genera graficas a partir de los benchmarks.
- `scripts/capture_single_image.py`: captura una imagen individual con la camara.
- `scripts/capture_dataset_images.py`: captura multiples imagenes para crear el dataset.
- `scripts/test_opencv.py`: verifica que OpenCV funcione.
- `scripts/test_yolo_tiny_load.py`: verifica que los modelos YOLO Tiny carguen correctamente.

## Archivos de entrenamiento

En `training/darknet/` se tienen archivos base para entrenamiento futuro:

- `obj.names`: contiene los nombres de las clases.
- `obj.data`: contiene la configuracion base para Darknet.

Clases iniciales:

- `granadilla_buena`
- `granadilla_golpeada`
- `granadilla_inmadura`


## Uso rapido en Raspberry Pi

Antes de ejecutar cualquier script, entrar al proyecto y activar el entorno virtual.

### Activar entorno virtual

Comando:

cd ~/granadilla_ai
source venv/bin/activate

### Probar deteccion con YOLOv3-Tiny

Comando:

python scripts/detect_image_flexible.py --model yolov3_tiny --image test_images/dog.jpg --img-size 320 --conf 0.3

### Probar deteccion con YOLOv4-Tiny

Comando:

python scripts/detect_image_flexible.py --model yolov4_tiny --image test_images/dog.jpg --img-size 320 --conf 0.3

### Captura individual futura

Comando:

python scripts/capture_single_image.py --class-name prueba

Opciones de clase:

- buena
- golpeada
- inmadura
- prueba

### Captura multiple futura

Ejemplo:

python scripts/capture_dataset_images.py --class-name buena --count 20 --interval 2

Este comando tomara 20 imagenes de la clase buena, con un intervalo de 2 segundos entre imagenes.

## Notebook de entrenamiento

El notebook principal de Colab esta en:

notebooks/yolo_tiny_granadilla_training.ipynb

Tambien puede abrirse desde el boton Open in Colab ubicado al inicio de este README.

## Notebook de entrenamiento

El notebook principal de Colab esta en:

notebooks/yolo_tiny_granadilla_training.ipynb

Tambien puede abrirse desde el boton Open in Colab ubicado al inicio de este README.

