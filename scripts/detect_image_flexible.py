import cv2
import numpy as np
import argparse
import time
from pathlib import Path

BASE = Path.home() / "granadilla_ai"

def get_model_paths(model_name):
    if model_name == "yolov3_tiny":
        return {
            "cfg": BASE / "models/yolov3_tiny/yolov3-tiny.cfg",
            "weights": BASE / "models/yolov3_tiny/yolov3-tiny.weights",
            "names": BASE / "models/yolov3_tiny/coco.names"
        }

    if model_name == "yolov4_tiny":
        return {
            "cfg": BASE / "models/yolov4_tiny/yolov4-tiny.cfg",
            "weights": BASE / "models/yolov4_tiny/yolov4-tiny.weights",
            "names": BASE / "models/yolov4_tiny/coco.names"
        }

    raise ValueError("Modelo no reconocido. Usa yolov3_tiny o yolov4_tiny.")


def load_classes(names_path):
    with open(names_path, "r") as f:
        return [line.strip() for line in f.readlines()]


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = net.getUnconnectedOutLayers().flatten()
    return [layer_names[i - 1] for i in output_layers]

def detect_image(model_name, image_path, img_size, conf_threshold, nms_threshold):
    paths = get_model_paths(model_name)

    image_path = Path(image_path).expanduser()
    image = cv2.imread(str(image_path))

    if image is None:
        raise FileNotFoundError("No se pudo leer la imagen: " + str(image_path))

    classes = load_classes(paths["names"])

    net = cv2.dnn.readNetFromDarknet(str(paths["cfg"]), str(paths["weights"]))
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    height, width = image.shape[:2]

    blob = cv2.dnn.blobFromImage(
        image,
        scalefactor=1 / 255.0,
        size=(img_size, img_size),
        mean=(0, 0, 0),
        swapRB=True,
        crop=False
    )

    output_layers = get_output_layers(net)

    net.setInput(blob)
    start = time.time()
    outputs = net.forward(output_layers)
    inference_time = time.time() - start

    boxes = []
    confidences = []
    class_ids = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = int(np.argmax(scores))
            confidence = float(scores[class_id])

            if confidence > conf_threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                box_w = int(detection[2] * width)
                box_h = int(detection[3] * height)

                x = int(center_x - box_w / 2)
                y = int(center_y - box_h / 2)

                boxes.append([x, y, box_w, box_h])
                confidences.append(confidence)
                class_ids.append(class_id)

    if boxes:
        indices = cv2.dnn.NMSBoxes(
            boxes,
            confidences,
            conf_threshold,
            nms_threshold
        )
    else:
        indices = []

    detections_count = 0

    if len(indices) > 0:
        for i in np.array(indices).flatten():
            x, y, box_w, box_h = boxes[i]
            class_id = class_ids[i]
            confidence = confidences[i]

            if class_id < len(classes):
                label = classes[class_id]
            else:
                label = "unknown"

            detections_count += 1

            cv2.rectangle(image, (x, y), (x + box_w, y + box_h), (0, 255, 0), 2)
            cv2.putText(
                image,
                label + ": " + str(round(confidence, 2)),
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            print("Detectado:", label, "| Confianza:", round(confidence, 2), "| Caja:", x, y, box_w, box_h)

    fps = 1 / inference_time if inference_time > 0 else 0

    print("")
    print("Resumen")
    print("Modelo:", model_name)
    print("Imagen:", image_path)
    print("Tamano de entrada:", str(img_size) + "x" + str(img_size))
    print("Detecciones:", detections_count)
    print("Tiempo de inferencia:", round(inference_time, 4), "s")
    print("FPS aproximado:", round(fps, 2))

    output_dir = BASE / "results"
    output_dir.mkdir(exist_ok=True)

    output_name = "result_" + model_name + "_" + str(img_size) + "_" + image_path.stem + ".jpg"
    output_path = output_dir / output_name

    cv2.imwrite(str(output_path), image)

    print("Resultado guardado en:", output_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=["yolov3_tiny", "yolov4_tiny"])
    parser.add_argument("--image", required=True)
    parser.add_argument("--img-size", type=int, default=320)
    parser.add_argument("--conf", type=float, default=0.3)
    parser.add_argument("--nms", type=float, default=0.4)

    args = parser.parse_args()

    detect_image(
        model_name=args.model,
        image_path=args.image,
        img_size=args.img_size,
        conf_threshold=args.conf,
        nms_threshold=args.nms
    )


if __name__ == "__main__":
    main()
