import subprocess
from pathlib import Path

BASE = Path.home() / "granadilla_ai"

def run_command(command):
    print("")
    print("Ejecutando:")
    print(" ".join(command))
    print("")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("Error al ejecutar el comando.")

def capture_single(class_name):
    command = [
        "python",
        "scripts/capture_single_image.py",
        "--class-name",
        class_name
    ]
    run_command(command)


def capture_multiple(class_name, count, interval):
    command = [
        "python",
        "scripts/capture_dataset_images.py",
        "--class-name",
        class_name,
        "--count",
        str(count),
        "--interval",
        str(interval)
    ]
    run_command(command)


def count_images():
    command = [
        "python",
        "scripts/count_captures.py"
    ]
    run_command(command)

def show_menu():
    print("")
    print("====================================")
    print(" MENU DE CAPTURA DE GRANADILLAS")
    print("====================================")
    print("1. Capturar imagen de prueba")
    print("2. Capturar granadilla buena")
    print("3. Capturar granadilla golpeada")
    print("4. Capturar granadilla inmadura")
    print("5. Captura multiple")
    print("6. Contar imagenes capturadas")
    print("7. Salir")
    print("====================================")

def ask_multiple_capture():
    print("")
    print("Selecciona la clase:")
    print("1. buena")
    print("2. golpeada")
    print("3. inmadura")
    print("4. prueba")

    class_option = input("Opcion: ").strip()

    class_map = {
        "1": "buena",
        "2": "golpeada",
        "3": "inmadura",
        "4": "prueba"
    }

    if class_option not in class_map:
        print("Opcion no valida.")
        return

    class_name = class_map[class_option]

    try:
        count = int(input("Cantidad de fotos: ").strip())
        interval = float(input("Intervalo entre fotos en segundos: ").strip())
    except ValueError:
        print("Cantidad o intervalo no valido.")
        return

    capture_multiple(class_name, count, interval)

def main():
    while True:
        show_menu()
        option = input("Selecciona una opcion: ").strip()

        if option == "1":
            capture_single("prueba")

        elif option == "2":
            capture_single("buena")

        elif option == "3":
            capture_single("golpeada")

        elif option == "4":
            capture_single("inmadura")

        elif option == "5":
            ask_multiple_capture()

        elif option == "6":
            count_images()

        elif option == "7":
            print("Saliendo del menu.")
            break

        else:
            print("Opcion no valida. Intenta nuevamente.")


if __name__ == "__main__":
    main()
