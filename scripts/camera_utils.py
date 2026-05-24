from pathlib import Path
import time
import json
import cv2

try:
    from libcamera import controls
except ImportError:
    controls = None


def safe_json_value(value):
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value

    if isinstance(value, (list, tuple)):
        return [safe_json_value(v) for v in value]

    try:
        return float(value)
    except Exception:
        return str(value)

def get_available_controls(picam2):
    try:
        return picam2.camera_controls
    except Exception:
        return {}


def apply_supported_controls(picam2, requested_controls):
    available_controls = get_available_controls(picam2)

    accepted = {}
    ignored = []

    for name, value in requested_controls.items():
        if name in available_controls:
            accepted[name] = value
        else:
            ignored.append(name)

    if accepted:
        picam2.set_controls(accepted)

    return accepted, ignored

def print_camera_summary(picam2):
    print("")
    print("Resumen de camara")
    print("-----------------")

    try:
        properties = picam2.camera_properties
        for key, value in properties.items():
            print(f"{key}: {value}")
    except Exception:
        print("No se pudieron leer propiedades de camara.")

    print("-----------------")

def trigger_autofocus(picam2, wait_time=1.5):
    if controls is None:
        print("No se puede activar AfTrigger porque libcamera.controls no esta disponible.")
        return

    requested = {
        "AfTrigger": controls.AfTriggerEnum.Start
    }

    accepted, ignored = apply_supported_controls(picam2, requested)

    print("")
    print("Trigger de autofocus:")
    print("Aplicado:", accepted)

    if ignored:
        print("No disponible:", ignored)

    time.sleep(wait_time)

def configure_camera_auto(
    picam2,
    mode="continuous",
    warmup=2.0,
    lens_position=None,
    lock_after_warmup=False
):
    """
    Configura automaticamente la Raspberry Pi Camera Module 3.

    mode:
    - continuous: autofocus continuo.
    - trigger: enfoque automatico antes de capturar.
    - manual: enfoque manual usando LensPosition.
    """

    if controls is None:
        print("Advertencia: no se pudo importar libcamera.controls.")
        print("Se usaran controles automaticos por defecto.")
        time.sleep(warmup)
        return

    requested = {}

    requested["AeEnable"] = True
    requested["AwbEnable"] = True

    if mode == "continuous":
        requested["AfMode"] = controls.AfModeEnum.Continuous

    elif mode == "trigger":
        requested["AfMode"] = controls.AfModeEnum.Auto

    elif mode == "manual":
        requested["AfMode"] = controls.AfModeEnum.Manual

        if lens_position is not None:
            requested["LensPosition"] = float(lens_position)

    else:
        print("Modo de enfoque no reconocido. Se usara continuous.")
        requested["AfMode"] = controls.AfModeEnum.Continuous

    accepted, ignored = apply_supported_controls(picam2, requested)

    print("")
    print("Controles solicitados:")
    print(requested)
    print("")
    print("Controles aplicados:")
    print(accepted)

    if ignored:
        print("")
        print("Controles no disponibles en esta camara:")
        print(ignored)

    print("")
    print(f"Esperando estabilizacion de camara: {warmup} s")
    time.sleep(warmup)

    if mode == "trigger":
        trigger_autofocus(picam2)

    if lock_after_warmup:
        lock_controls = {}

        available_controls = get_available_controls(picam2)

        if "AeEnable" in available_controls:
            lock_controls["AeEnable"] = False

        if "AwbEnable" in available_controls:
            lock_controls["AwbEnable"] = False

        if lock_controls:
            picam2.set_controls(lock_controls)
            print("")
            print("Autoexposicion y balance bloqueados despues del ajuste inicial:")
            print(lock_controls)

def calculate_sharpness(frame):
    if frame is None:
        return 0.0

    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    else:
        gray = frame

    score = cv2.Laplacian(gray, cv2.CV_64F).var()
    return float(score)


def capture_best_frame(picam2, samples=3, interval=0.15):
    best_frame = None
    best_metadata = {}
    best_sharpness = -1.0

    samples = max(1, int(samples))

    for i in range(samples):
        frame = picam2.capture_array()

        try:
            metadata = picam2.capture_metadata()
        except Exception:
            metadata = {}

        sharpness = calculate_sharpness(frame)

        if sharpness > best_sharpness:
            best_frame = frame
            best_metadata = metadata
            best_sharpness = sharpness

        if i < samples - 1:
            time.sleep(interval)

    return best_frame, best_metadata, best_sharpness


def frame_to_bgr(frame):
    if frame is None:
        return None

    if len(frame.shape) == 3 and frame.shape[2] == 4:
        return cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

    if len(frame.shape) == 3 and frame.shape[2] == 3:
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    return frame


def save_capture_metadata(image_path, metadata, extra_data=None):
    image_path = Path(image_path)
    metadata_path = image_path.with_suffix(".json")

    safe_metadata = {}

    for key, value in metadata.items():
        safe_metadata[key] = safe_json_value(value)

    data = {
        "image": image_path.name,
        "metadata": safe_metadata
    }

    if extra_data:
        data["extra"] = extra_data

    with open(metadata_path, "w") as f:
        json.dump(data, f, indent=4)

    return metadata_path


def get_resolution_preset(preset, width=None, height=None):
    presets = {
        "hd": (1280, 720),
        "fhd": (1920, 1080),
        "qhd": (2304, 1296),
        "full": (4608, 2592),
        "custom": (width, height),
    }

    if preset not in presets:
        raise ValueError("Preset de resolucion no valido: " + str(preset))

    selected_width, selected_height = presets[preset]

    if selected_width is None or selected_height is None:
        raise ValueError("Para preset custom debes indicar width y height.")

    return int(selected_width), int(selected_height)


def save_jpeg(image_path, frame_bgr, quality=95):
    quality = int(quality)

    if quality < 1:
        quality = 1

    if quality > 100:
        quality = 100

    return cv2.imwrite(
        str(image_path),
        frame_bgr,
        [cv2.IMWRITE_JPEG_QUALITY, quality]
    )
