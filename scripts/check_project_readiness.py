from pathlib import Path

BASE = Path.home() / "granadilla_ai"

required_files = [
    "README.md",
    ".gitignore",
    "requirements_raspberry.txt",
    "notebooks/yolo_tiny_granadilla_training.ipynb",
    "docs/guia_rapida_captura_companero.md",
    "docs/guia_colaborador.md",
    "docs/entrenamiento_yolo_tiny.md",
    "docs/checklist_entrenamiento.md",
    "scripts/capture_menu.py",
    "scripts/check_camera_controls.py",
    "scripts/camera_utils.py",
    "scripts/live_camera_preview.py",
    "scripts/capture_single_image.py",
    "scripts/capture_dataset_images.py",
    "scripts/count_captures.py",
    "scripts/package_captures.py",
    "scripts/detect_image_flexible.py",
    "scripts/benchmark_yolo_tiny.py",
    "scripts/plot_benchmark_results.py",
    "training/darknet/obj.names",
    "training/darknet/obj.data",
    "benchmarks/benchmark_results.csv",
    "benchmarks/benchmark_analysis.md",
]

required_dirs = [
    "captures/buenas",
    "captures/golpeadas",
    "captures/inmaduras",
    "captures/pruebas",
    "models/yolov3_tiny",
    "models/yolov4_tiny",
    "docs",
    "scripts",
    "notebooks",
    "training/darknet",
    "benchmarks",
    "dataset_management",
]

print("Revision general del proyecto")
print("--------------------------------")

missing_files = []
missing_dirs = []

for item in required_dirs:
    path = BASE / item
    if path.exists():
        print("[OK] Carpeta:", item)
    else:
        print("[FALTA] Carpeta:", item)
        missing_dirs.append(item)

print("--------------------------------")

for item in required_files:
    path = BASE / item
    if path.exists():
        print("[OK] Archivo:", item)
    else:
        print("[FALTA] Archivo:", item)
        missing_files.append(item)

print("--------------------------------")

if not missing_files and not missing_dirs:
    print("Proyecto listo. No faltan archivos esenciales.")
else:
    print("Hay elementos pendientes.")
    print("Carpetas faltantes:", missing_dirs)
    print("Archivos faltantes:", missing_files)
