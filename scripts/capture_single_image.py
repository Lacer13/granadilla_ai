import argparse
from pathlib import Path
from datetime import datetime
import cv2
from picamera2 import Picamera2

from camera_utils import (
    print_camera_summary,
    configure_camera_auto,
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
        description="Captura individual con Raspberry Pi Camera Module 3"
    )

    parser.add_argument(
        "--class-name",
        required=True,
        choices=["buena", "golpeada", "inmadura", "prueba"],
        help="Clase de la imagen capturada"
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
        "--delay",
        type=float,
        default=3.0,
        help="Tiempo de estabilizacion antes de capturar"
    )

    parser.add_argument(
        "--focus-mode",
        choices=["continuous", "trigger", "manual"],
        default="trigger",
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
        help="Cantidad de capturas rapidas para elegir la mas nitida"
    )

    parser.add_argument(
        "--lock-after-warmup",
        action="store_true",
        help="Bloquea exposicion y balance despues del ajuste inicial"
    )

    args = parser.parse_args()

    output_folder = get_output_folder(args.class_name)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{args.class_name}_{timestamp}.jpg"
    output_path = output_folder / filename

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
            warmup=args.delay,
            lens_position=args.lens_position,
            lock_after_warmup=args.lock_after_warmup
        )

        frame, metadata, sharpness = capture_best_frame(
            picam2,
            samples=args.samples,
            interval=0.15
        )

        frame_bgr = frame_to_bgr(frame)

        if frame_bgr is None:
            raise RuntimeError("No se pudo capturar imagen.")

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
            "samples": args.samples,
            "lock_after_warmup": args.lock_after_warmup
        }

        metadata_path = save_capture_metadata(
            output_path,
            metadata,
            extra_data=extra_data
        )

        print("")
        print("Imagen guardada en:")
        print(output_path)

        print("")
        print("Metadata guardada en:")
        print(metadata_path)

        print("")
        print("Puntaje de nitidez:")
        print(round(sharpness, 2))

        if sharpness < 80:
            print("")
            print("Advertencia: la imagen podria estar poco nitida.")
            print("Revisar enfoque, distancia, iluminacion o vibracion.")

    finally:
        picam2.stop()
        picam2.close()


if __name__ == "__main__":
    main()
