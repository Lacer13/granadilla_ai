import cv2
import time
from pathlib import Path

MODELS = {
    "yolov3_tiny": {
        "cfg": "models/yolov3_tiny/yolov3-tiny.cfg",
        "weights": "models/yolov3_tiny/yolov3-tiny.weights",
    },
    "yolov4_tiny": {
        "cfg": "models/yolov4_tiny/yolov4-tiny.cfg",
        "weights": "models/yolov4_tiny/yolov4-tiny.weights",
    },
}

for name, paths in MODELS.items():
    cfg = Path(paths["cfg"])
    weights = Path(paths["weights"])

    print(f"\nProbando modelo: {name}")

    if not cfg.exists():
        print(f"No existe cfg: {cfg}")
        continue

    if not weights.exists():
        print(f"No existe weights: {weights}")
        continue

    start = time.time()
    net = cv2.dnn.readNetFromDarknet(str(cfg), str(weights))
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    elapsed = time.time() - start

    layers = net.getLayerNames()
    print(f"Modelo cargado correctamente: {name}")
    print(f"Cantidad de capas: {len(layers)}")
    print(f"Tiempo de carga: {elapsed:.2f} s")

print("\nPrueba finalizada.")
