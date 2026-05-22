from pathlib import Path

BASE = Path.home() / "granadilla_ai"
CAPTURES = BASE / "captures"

folders = {
    "buenas": CAPTURES / "buenas",
    "golpeadas": CAPTURES / "golpeadas",
    "inmaduras": CAPTURES / "inmaduras",
    "pruebas": CAPTURES / "pruebas",
}

extensions = [".jpg", ".jpeg", ".png"]

print("Conteo de imagenes capturadas")
print("--------------------------------")

total = 0

for name, folder in folders.items():
    count = 0

    if folder.exists():
        for file in folder.iterdir():
            if file.suffix.lower() in extensions:
                count += 1

    total += count
    print(name + ":", count)

print("--------------------------------")
print("Total:", total)
