# Guia para colaborador

## Objetivo

Esta guia permite que otro integrante pueda continuar el proyecto desde GitHub y ejecutarlo en una Raspberry Pi o computadora compatible.

El proyecto usa:

- Raspberry Pi
- Python
- OpenCV
- YOLOv3-Tiny
- YOLOv4-Tiny
- Google Colab
- GitHub

## 1. Clonar repositorio

En la Raspberry Pi o computadora de trabajo, ejecutar:

git clone https://github.com/Lacer13/granadilla_ai.git
cd granadilla_ai

## 2. Instalar paquetes del sistema en Raspberry Pi

Ejecutar:

sudo apt update
sudo apt install -y git python3-full python3-pip python3-venv python3-opencv python3-picamera2 python3-numpy python3-pandas python3-matplotlib htop nano tmux build-essential cmake pkg-config

## 3. Crear entorno virtual

Dentro de la carpeta del proyecto:

python3 -m venv --system-site-packages venv
source venv/bin/activate

Actualizar herramientas de Python:

python -m pip install --upgrade pip setuptools wheel

Instalar librerias del proyecto:

python -m pip install -r requirements_raspberry.txt

## 4. Pruebas basicas

Activar entorno:

source venv/bin/activate

Probar OpenCV:

python scripts/test_opencv.py

Probar carga de modelos YOLO Tiny:

python scripts/test_yolo_tiny_load.py

## 5. Probar deteccion flexible

Probar YOLOv3-Tiny:

python scripts/detect_image_flexible.py --model yolov3_tiny --image test_images/dog.jpg --img-size 320 --conf 0.3

Probar YOLOv4-Tiny:

python scripts/detect_image_flexible.py --model yolov4_tiny --image test_images/dog.jpg --img-size 320 --conf 0.3

Los resultados se guardaran en la carpeta:

results/

## 6. Flujo de trabajo recomendado con Git

Antes de modificar codigo, actualizar el repositorio:

git pull

Crear una rama nueva:

git checkout -b nueva_funcion

Luego de hacer cambios:

git status
git add .
git commit -m "Descripcion del cambio"
git push -u origin nueva_funcion

## 7. Archivos que no se deben subir

No subir al repositorio:

- tokens de GitHub
- API keys de Roboflow
- contrasenas
- archivos .env
- datasets completos
- imagenes grandes
- pesos .weights
- modelos .pt u .onnx pesados

Estos archivos deben mantenerse fuera del repositorio o compartirse por otro medio.

