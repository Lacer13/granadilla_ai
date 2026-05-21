import cv2
import time
from pathlib import Path
import csv

BASE = Path.home() / "granadilla_ai"
IMAGE_PATH = BASE / "test_images/dog.jpg"
RESULTS_PATH = BASE / "results/benchmark_yolo_tiny.csv"

MODELS = {
    "yolov3_tiny": {
        "cfg": BASE / "models/yolov3_tiny/yolov3-tiny.cfg",
        "weights": BASE / "models/yolov3_tiny/yolov3-tiny.weights",
    },
    "yolov4_tiny": {
        "cfg": BASE / "models/yolov4_tiny/yolov4-tiny.cfg",
        "weights": BASE / "models/yolov4_tiny/yolov4-tiny.weights",
    },
}

IMG_SIZES = [320, 416]
ITERATIONS = 30

def get_output_layers(net):
    layer_names = net.getLayerNames()
    return [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]


def benchmark_model(model_name, cfg, weights, img_size):
    image = cv2.imread(str(IMAGE_PATH))

    if image is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {IMAGE_PATH}")

    net = cv2.dnn.readNetFromDarknet(str(cfg), str(weights))
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    output_layers = get_output_layers(net)

    blob = cv2.dnn.blobFromImage(
        image,
        scalefactor=1 / 255.0,
        size=(img_size, img_size),
        mean=(0, 0, 0),
        swapRB=True,
        crop=False
    )

    for _ in range(3):
        net.setInput(blob)
        net.forward(output_layers)

    times = []

    for _ in range(ITERATIONS):
        net.setInput(blob)
        start = time.time()
        net.forward(output_layers)
        end = time.time()
        times.append(end - start)

    avg_time = sum(times) / len(times)
    fps = 1 / avg_time if avg_time > 0 else 0

    return avg_time, fps


def main():
    BASE.joinpath("results").mkdir(exist_ok=True)

    rows = []

    print("")
    print("Benchmark YOLO Tiny en Raspberry Pi")
    print("-----------------------------------")

    for model_name, paths in MODELS.items():
        for img_size in IMG_SIZES:
            avg_time, fps = benchmark_model(
                model_name,
                paths["cfg"],
                paths["weights"],
                img_size
            )

            print("Modelo:", model_name)
            print("Tamano:", str(img_size) + "x" + str(img_size))
            print("Tiempo promedio:", round(avg_time, 4), "s")
            print("FPS promedio:", round(fps, 2))
            print("-----------------------------------")

            rows.append({
                "modelo": model_name,
                "tamano_entrada": str(img_size) + "x" + str(img_size),
                "iteraciones": ITERATIONS,
                "tiempo_promedio_s": round(avg_time, 4),
                "fps_promedio": round(fps, 2)
            })

    with open(RESULTS_PATH, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "modelo",
                "tamano_entrada",
                "iteraciones",
                "tiempo_promedio_s",
                "fps_promedio"
            ]
        )
        writer.writeheader()
        writer.writerows(rows)

    print("")
    print("Resultados guardados en:", RESULTS_PATH)


if __name__ == "__main__":
    main()
