import cv2
import numpy as np
import time
from pathlib import Path

base = Path.home() / "granadilla_ai"

model_name = "yolov4_tiny"
image_path = base / "test_images/dog.jpg"

cfg = base / "models/yolov4_tiny/yolov4-tiny.cfg"
weights = base / "models/yolov4_tiny/yolov4-tiny.weights"
names = base / "models/yolov4_tiny/coco.names"

classes = [line.strip() for line in open(names)]

image = cv2.imread(str(image_path))
if image is None:
    raise FileNotFoundError(f"No se pudo leer la imagen: {image_path}")

height, width = image.shape[:2]

net = cv2.dnn.readNetFromDarknet(str(cfg), str(weights))
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

blob = cv2.dnn.blobFromImage(
    image,
    1 / 255.0,
    (416, 416),
    swapRB=True,
    crop=False
)

net.setInput(blob)

start = time.time()
outputs = net.forward(output_layers)
elapsed = time.time() - start

boxes = []
confidences = []
class_ids = []

for output in outputs:
    for detection in output:
        scores = detection[5:]
        class_id = int(np.argmax(scores))
        confidence = float(scores[class_id])

        if confidence > 0.3:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(confidence)
            class_ids.append(class_id)

indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)

detections = 0

if len(indices) > 0:
    for i in indices.flatten():
        x, y, w, h = boxes[i]
        label = classes[class_ids[i]]
        conf = confidences[i]

        detections += 1

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            image,
            f"{label}: {conf:.2f}",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        print(f"Detectado: {label} | Confianza: {conf:.2f}")

fps = 1 / elapsed if elapsed > 0 else 0

print(f"Tiempo de inferencia: {elapsed:.3f} s")
print(f"FPS aproximado: {fps:.2f}")
print(f"Detecciones: {detections}")

output_path = base / "results/result_yolov4_tiny_dog.jpg"
cv2.imwrite(str(output_path), image)

print(f"Resultado guardado en: {output_path}")
