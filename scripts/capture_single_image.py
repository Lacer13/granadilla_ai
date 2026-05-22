from picamera2 import Picamera2
from datetime import datetime
from pathlib import Path
import argparse
import time
import cv2

BASE = Path.home() / "granadilla_ai"
CAPTURES_DIR = BASE / "captures"

VALID_CLASSES = {
    "buena": "buenas",
    "golpeada": "golpeadas",
    "inmadura": "inmaduras",
    "prueba": "pruebas"
}

def capture_image(class_name, width, height, delay):
    if class_name not in VALID_CLASSES:
        raise ValueError("Clase no valida. Usa: buena, golpeada, inmadura o prueba.")

    output_folder = CAPTURES_DIR / VALID_CLASSES[class_name]
    output_folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_folder / f"{class_name}_{timestamp}.jpg"

    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (width, height)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")

    print("Iniciando camara...")
    picam2.start()
    time.sleep(delay)

    frame = picam2.capture_array()
    picam2.stop()

    cv2.imwrite(str(output_path), frame)

    print("Imagen guardada en:", output_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--class-name",
        required=True,
        choices=["buena", "golpeada", "inmadura", "prueba"],
        help="Clase o carpeta donde se guardara la imagen"
    )
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--delay", type=float, default=2.0)

    args = parser.parse_args()

    capture_image(
        class_name=args.class_name,
        width=args.width,
        height=args.height,
        delay=args.delay
    )


if __name__ == "__main__":
    main()
