from pathlib import Path
from datetime import datetime
import zipfile

BASE = Path.home() / "granadilla_ai"
CAPTURES_DIR = BASE / "captures"
OUTPUT_DIR = BASE / "exports"
OUTPUT_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
zip_path = OUTPUT_DIR / f"captures_granadillas_{timestamp}.zip"

extensions = [".jpg", ".jpeg", ".png"]

total_files = 0

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for file in CAPTURES_DIR.rglob("*"):
        if file.is_file() and file.suffix.lower() in extensions:
            arcname = file.relative_to(BASE)
            zipf.write(file, arcname)
            total_files += 1

print("Archivo ZIP creado:", zip_path)
print("Total de imagenes comprimidas:", total_files)

if total_files == 0:
    print("Advertencia: no se encontraron imagenes para comprimir.")
