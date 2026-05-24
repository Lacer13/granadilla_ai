import argparse
from pathlib import Path
from datetime import datetime
import cv2
from picamera2 import Picamera2

from camera_utils import (
    print_camera_summary,
    configure_camera_auto,
    trigger_autofocus,
    calculate_sharpness,
    frame_to_bgr,
    save_capture_metadata,
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


def save_preview_frame(frame_bgr, metadata, class_name, sharpness):
    output_folder = get_output_folder(class_name)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{class_name}_preview_{timestamp}.jpg"
    output_path = output_folder / filename

    cv2.imwrite(str(output_path), frame_bgr)

    extra_data = {
        "class_name": class_name,
        "source": "live_preview",
        "sharpness_score": sharpness
    }

    metadata_path = save_capture_metadata(
        output_path,
        metadata,
        extra_data=extra_data
    )

    print("")
    print("Imagen guardada desde vista en vivo:")
    print(output_path)
    print("Metadata:")
    print(metadata_path)

def main():
    parser = argparse.ArgumentParser(
        description="Vista en vivo para Raspberry Pi Camera Module 3"
    )

    parser.add_argument(
        "--width",
        type=int,
        default=1280,
        help="Ancho de vista previa"
    )

    parser.add_argument(
        "--height",
        type=int,
        default=720,
        help="Alto de vista previa"
    )

    parser.add_argument(
        "--warmup",
        type=float,
        default=2.0,
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
        help="Posicion manual del lente si se usa focus-mode manual"
    )

    parser.add_argument(
        "--save-class",
        choices=["buena", "golpeada", "inmadura", "prueba"],
        default="prueba",
        help="Clase usada si se guarda una imagen con la tecla s"
    )

    args = parser.parse_args()

    picam2 = Picamera2()

    config = picam2.create_preview_configuration(
        main={
            "size": (args.width, args.height),
            "format": "RGB888"
        }
    )

    picam2.configure(config)

    try:
        print_camera_summary(picam2)

        print("")
        print("Iniciando vista en vivo...")
        print("Teclas disponibles:")
        print("q  : salir")
        print("ESC: salir")
        print("s  : guardar imagen de prueba")
        print("r  : reenfocar usando autofocus trigger")
        print("")

        picam2.start()

        configure_camera_auto(
            picam2,
            mode=args.focus_mode,
            warmup=args.warmup,
            lens_position=args.lens_position,
            lock_after_warmup=False
        )

        while True:
            frame = picam2.capture_array()

            try:
                metadata = picam2.capture_metadata()
            except Exception:
                metadata = {}

            sharpness = calculate_sharpness(frame)
            frame_bgr = frame_to_bgr(frame)

            if frame_bgr is None:
                print("No se pudo obtener frame de camara.")
                continue

            text_1 = "Camera V3 Preview | q: salir | s: guardar | r: reenfocar"
            text_2 = f"Nitidez: {sharpness:.2f} | Modo enfoque: {args.focus_mode}"

            cv2.putText(
                frame_bgr,
                text_1,
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame_bgr,
                text_2,
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.imshow("Raspberry Pi Camera Module 3 - Vista en vivo", frame_bgr)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == 27:
                print("Cerrando vista en vivo.")
                break

            if key == ord("s"):
                save_preview_frame(
                    frame_bgr,
                    metadata,
                    args.save_class,
                    sharpness
                )

            if key == ord("r"):
                print("Reenfocando...")
                trigger_autofocus(picam2, wait_time=1.0)

    finally:
        picam2.stop()
        picam2.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
