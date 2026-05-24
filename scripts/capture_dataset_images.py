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

def capture_dataset(class_name, count, interval, width, height, warmup):
    if class_name not in VALID_CLASSES:
        raise ValueError("Clase no valida. Usa: buena, golpeada, inmadura o prueba.")

    output_folder = CAPTURES_DIR / VALID_CLASSES[class_name]
    output_folder.mkdir(parents=True, exist_ok=True)

    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (width, height)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")

    print("Iniciando camara...")
    picam2.start()
    time.sleep(warmup)

    for i in range(1, count + 1):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_folder / f"{class_name}_{timestamp}_{i:03d}.jpg"

        frame = picam2.capture_array()
        cv2.imwrite(str(output_path), frame)

        print(f"Imagen {i}/{count} guardada en: {output_path}")

        if i < count:
            time.sleep(interval)

    picam2.stop()
    print("Captura finalizada.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--class-name",
        required=True,
        choices=["buena", "golpeada", "inmadura", "prueba"]
    )
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--warmup", type=float, default=2.0)

    args = parser.parse_args()

    capture_dataset(
        class_name=args.class_name,
        count=args.count,
        interval=args.interval,
        width=args.width,
        height=args.height,
        warmup=args.warmup
    )


if __name__ == "__main__":
    main()
import argparse
from pathlib import Path
from datetime import datetime
import time
import cv2
from picamera2 import Picamera2

from camera_utils import (
    print_camera_summary,
    configure_camera_auto,
    trigger_autofocus,
    capture_best_frame,
    frame_to_bgr,
    save_capture_metadata,
    get_resolution_preset,
    save_jpeg,
)

BASE = Path.home() / "granadilla_ai"

CLASS_FOLDERS = {
    "buena": "buenas",
    "golpeada": "golpeadas",
    "inmadura": "inmaduras",
    "prueba": "pruebas",
}

def get_output_folder(class_name):
    folder_name = CLASS_FOLDERS.get(class_name)

    if folder_name is None:
        raise ValueError("Clase no valida: " + class_name)

    output_folder = BASE / "captures" / folder_name
    output_folder.mkdir(parents=True, exist_ok=True)

    return output_folder

def main():
    parser = argparse.ArgumentParser(
        description="Captura multiple con Raspberry Pi Camera Module 3"
    )

    parser.add_argument(
        "--class-name",
        required=True,
        choices=["buena", "golpeada", "inmadura", "prueba"],
        help="Clase de las imagenes capturadas"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=20,
        help="Cantidad de imagenes"
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Intervalo entre imagenes en segundos"
    )

    parser.add_argument(
        "--resolution",
        choices=["hd", "fhd", "qhd", "full", "custom"],
        default="fhd",
        help="Preset de resolucion: hd, fhd, qhd, full o custom"
    )

    parser.add_argument(
        "--width",
        type=int,
        default=1920,
        help="Ancho de captura si se usa custom"
    )

    parser.add_argument(
        "--height",
        type=int,
        default=1080,
        help="Alto de captura si se usa custom"
    )

    parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=95,
        help="Calidad JPEG entre 1 y 100"
    )

    parser.add_argument(
        "--warmup",
        type=float,
        default=3.0,
        help="Tiempo de estabilizacion inicial"
    )

    parser.add_argument(
        "--focus-mode",
        choices=["continuous", "trigger", "manual"],
        default="continuous",
        help="Modo de enfoque"
    )

    parser.add_argument(
        "--lens-position",
        type=float,
        default=None,
        help="Posicion manual del lente si focus-mode es manual"
    )

    parser.add_argument(
        "--samples",
        type=int,
        default=3,
        help="Cantidad de capturas rapidas por imagen para elegir la mas nitida"
    )

    parser.add_argument(
        "--lock-after-warmup",
        action="store_true",
        help="Bloquea exposicion y balance despues del ajuste inicial"
    )

    args = parser.parse_args()

    output_folder = get_output_folder(args.class_name)

    capture_width, capture_height = get_resolution_preset(
        args.resolution,
        width=args.width,
        height=args.height
    )

    picam2 = Picamera2()

    config = picam2.create_preview_configuration(
        main={
            "size": (capture_width, capture_height),
            "format": "RGB888"
        }
    )

    picam2.configure(config)

    try:
        print_camera_summary(picam2)

        print("")
        print("Iniciando camara...")
        picam2.start()

        configure_camera_auto(
            picam2,
            mode=args.focus_mode,
            warmup=args.warmup,
            lens_position=args.lens_position,
            lock_after_warmup=args.lock_after_warmup
        )

        print("")
        print("Iniciando captura multiple...")
        print("Clase:", args.class_name)
        print("Cantidad:", args.count)
        print("Intervalo:", args.interval, "s")
        print("Modo de enfoque:", args.focus_mode)
        print("Resolucion:", capture_width, "x", capture_height)

        for i in range(1, args.count + 1):
            if args.focus_mode == "trigger":
                trigger_autofocus(picam2, wait_time=1.0)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{args.class_name}_{timestamp}_{i:04d}.jpg"
            output_path = output_folder / filename

            frame, metadata, sharpness = capture_best_frame(
                picam2,
                samples=args.samples,
                interval=0.15
            )

            frame_bgr = frame_to_bgr(frame)

            if frame_bgr is None:
                print("No se pudo capturar imagen", i)
                continue

            save_jpeg(output_path, frame_bgr, quality=args.jpeg_quality)

            extra_data = {
                "class_name": args.class_name,
                "focus_mode": args.focus_mode,
                "lens_position": args.lens_position,
                "resolution_preset": args.resolution,
                "width": capture_width,
                "height": capture_height,
                "jpeg_quality": args.jpeg_quality,
                "sharpness_score": sharpness,
                "sample_number": i,
                "total_samples": args.count,
                "samples_per_image": args.samples,
                "lock_after_warmup": args.lock_after_warmup
            }

            metadata_path = save_capture_metadata(
                output_path,
                metadata,
                extra_data=extra_data
            )

    finally:
        picam2.stop()
        picam2.close()


if __name__ == "__main__":
    main()
