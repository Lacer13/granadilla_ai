import csv
from pathlib import Path
import matplotlib.pyplot as plt

BASE = Path.home() / "granadilla_ai"
CSV_PATH = BASE / "benchmarks/benchmark_results.csv"
FIG_DIR = BASE / "benchmarks/figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

labels = []
fps_values = []
time_ms_values = []

with open(CSV_PATH, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        label = row["model"] + " " + row["input_size"]
        labels.append(label)
        fps_values.append(float(row["fps"]))
        time_ms_values.append(float(row["avg_time_ms"]))

plt.figure(figsize=(10, 5))
plt.bar(labels, fps_values)
plt.ylabel("FPS promedio")
plt.xlabel("Modelo y tamano de entrada")
plt.title("Comparacion de FPS - YOLO Tiny en Raspberry Pi")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(FIG_DIR / "fps_comparison.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 5))
plt.bar(labels, time_ms_values)
plt.ylabel("Tiempo promedio de inferencia (ms)")
plt.xlabel("Modelo y tamano de entrada")
plt.title("Comparacion de tiempo de inferencia - YOLO Tiny")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(FIG_DIR / "inference_time_comparison.png", dpi=150)
plt.close()

print("Graficas generadas en:", FIG_DIR)
print("- fps_comparison.png")
print("- inference_time_comparison.png")
