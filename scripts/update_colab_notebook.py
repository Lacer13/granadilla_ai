import json
from pathlib import Path

NOTEBOOK_PATH = Path.home() / "granadilla_ai/notebooks/yolo_tiny_granadilla_training.ipynb"

with open(NOTEBOOK_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

def md(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    }

def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.strip().split("\n")]
    }

new_cells = []

new_cells.append(md("""
## 2. Clonar Darknet

En esta seccion se descarga el repositorio Darknet de AlexeyAB, que se usara para entrenar YOLOv3-Tiny o YOLOv4-Tiny en Google Colab.
"""))

new_cells.append(code("""
!git clone https://github.com/AlexeyAB/darknet.git
%cd darknet
"""))

new_cells.append(md("""
## 3. Compilar Darknet con GPU y OpenCV

Se activan las opciones de GPU, CUDNN y OpenCV en el Makefile. Esto permite entrenar usando la GPU de Colab.
"""))

new_cells.append(code("""
!sed -i 's/GPU=0/GPU=1/' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile
!make
"""))

new_cells.append(md("""
## 4. Definir clases del proyecto

Las clases iniciales del sistema de granadillas seran:

- granadilla_buena
- granadilla_golpeada
- granadilla_inmadura
"""))

new_cells.append(code("""
classes = [
    "granadilla_buena",
    "granadilla_golpeada",
    "granadilla_inmadura"
]

with open("data/obj.names", "w") as f:
    for c in classes:
        f.write(c + "\\n")

print("Clases guardadas en data/obj.names")
!cat data/obj.names
"""))

new_cells.append(code("""
with open("data/obj.data", "w") as f:
    f.write("classes = 3\\n")
    f.write("train = data/train.txt\\n")
    f.write("valid = data/valid.txt\\n")
    f.write("names = data/obj.names\\n")
    f.write("backup = backup/\\n")

!mkdir -p backup
print("Archivo data/obj.data creado")
!cat data/obj.data
"""))

new_cells.append(md("""
## 5. Cargar dataset

En esta seccion se cargara el dataset cuando ya se tengan las imagenes etiquetadas.

Opciones futuras:

1. Descargar desde Roboflow.
2. Montar Google Drive.
3. Subir un archivo .zip manualmente.

Por ahora esta parte queda como plantilla.
"""))

new_cells.append(code("""
# Opcion A: montar Google Drive
# from google.colab import drive
# drive.mount('/content/drive')
"""))

new_cells.append(code("""
# Opcion B: descargar desde Roboflow
# Cuando tengas el dataset en Roboflow, se reemplazara este bloque
# con el codigo de descarga que Roboflow genera automaticamente.

# Ejemplo referencial:
# !pip install roboflow
# from roboflow import Roboflow
# rf = Roboflow(api_key="TU_API_KEY")
# project = rf.workspace("TU_WORKSPACE").project("TU_PROYECTO")
# dataset = project.version(1).download("darknet")
"""))

new_cells.append(md("""
## 6. Estructura esperada del dataset

Darknet espera archivos de imagen y etiquetas en formato YOLO.

Cada imagen debe tener un archivo .txt con el mismo nombre.

Ejemplo:

imagen_001.jpg  
imagen_001.txt  

Formato de etiqueta YOLO:

class_id x_center y_center width height

Los valores deben estar normalizados entre 0 y 1.
"""))

new_cells.append(md("""
## 7. Preparar configuracion YOLOv3-Tiny

Para entrenar YOLO con 3 clases, se deben ajustar los parametros `classes` y `filters` en el archivo .cfg.

Formula para filtros:

filters = (clases + 5) * 3

Para 3 clases:

filters = (3 + 5) * 3 = 24
"""))

new_cells.append(code("""
# Crear una copia del cfg base de YOLOv3-Tiny
!cp cfg/yolov3-tiny.cfg cfg/yolov3-tiny-granadilla.cfg

# Ajustes principales para 3 clases
!sed -i 's/classes=80/classes=3/g' cfg/yolov3-tiny-granadilla.cfg
!sed -i 's/filters=255/filters=24/g' cfg/yolov3-tiny-granadilla.cfg

# Ajustes iniciales de entrenamiento
!sed -i 's/batch=1/batch=64/g' cfg/yolov3-tiny-granadilla.cfg
!sed -i 's/subdivisions=1/subdivisions=16/g' cfg/yolov3-tiny-granadilla.cfg
!sed -i 's/max_batches = 500200/max_batches = 6000/g' cfg/yolov3-tiny-granadilla.cfg
!sed -i 's/steps=400000,450000/steps=4800,5400/g' cfg/yolov3-tiny-granadilla.cfg

print("Configuracion YOLOv3-Tiny personalizada creada")
"""))

new_cells.append(md("""
## 8. Preparar configuracion YOLOv4-Tiny

Tambien se deja preparada una configuracion alternativa para YOLOv4-Tiny.
"""))

new_cells.append(code("""
!cp cfg/yolov4-tiny.cfg cfg/yolov4-tiny-granadilla.cfg

!sed -i 's/classes=80/classes=3/g' cfg/yolov4-tiny-granadilla.cfg
!sed -i 's/filters=255/filters=24/g' cfg/yolov4-tiny-granadilla.cfg

!sed -i 's/batch=1/batch=64/g' cfg/yolov4-tiny-granadilla.cfg
!sed -i 's/subdivisions=1/subdivisions=16/g' cfg/yolov4-tiny-granadilla.cfg
!sed -i 's/max_batches = 500500/max_batches = 6000/g' cfg/yolov4-tiny-granadilla.cfg
!sed -i 's/steps=400000,450000/steps=4800,5400/g' cfg/yolov4-tiny-granadilla.cfg

print("Configuracion YOLOv4-Tiny personalizada creada")
"""))

new_cells.append(md("""
## 9. Descargar pesos preentrenados

Antes de entrenar desde cero, se descargan pesos convolucionales preentrenados.

Esto ayuda a que el entrenamiento sea mas rapido y estable.
"""))

new_cells.append(code("""
# Pesos para YOLOv3-Tiny
!wget -nc https://pjreddie.com/media/files/darknet53.conv.74

# Pesos para YOLOv4-Tiny
!wget -nc https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29
"""))

new_cells.append(md("""
## 10. Entrenar YOLOv3-Tiny

Ejecutar esta celda cuando el dataset ya este listo y existan los archivos:

- data/train.txt
- data/valid.txt
- data/obj.names
- data/obj.data
"""))

new_cells.append(code("""
# Entrenamiento YOLOv3-Tiny
# !./darknet detector train data/obj.data cfg/yolov3-tiny-granadilla.cfg darknet53.conv.74 -dont_show -map
"""))

new_cells.append(md("""
## 11. Entrenar YOLOv4-Tiny

Ejecutar esta celda si se desea entrenar el modelo alternativo YOLOv4-Tiny.
"""))

new_cells.append(code("""
# Entrenamiento YOLOv4-Tiny
# !./darknet detector train data/obj.data cfg/yolov4-tiny-granadilla.cfg yolov4-tiny.conv.29 -dont_show -map
"""))

new_cells.append(md("""
## 12. Pesos finales

Los mejores pesos se guardaran en la carpeta `backup/`.

Ejemplos:

- yolov3-tiny-granadilla_best.weights
- yolov4-tiny-granadilla_best.weights

Estos archivos se copiaran luego a la Raspberry Pi para inferencia con OpenCV DNN.
"""))

nb["cells"].extend(new_cells)

with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook actualizado:", NOTEBOOK_PATH)
print("Celdas agregadas:", len(new_cells))
