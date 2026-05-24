import subprocess
import sys

PYTHON = sys.executable


def run_command(command):
    print("")
    print("Ejecutando:")
    print(" ".join(command))
    print("")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("Error al ejecutar el comando.")
    except KeyboardInterrupt:
        print("Proceso interrumpido por el usuario.")

def live_preview():
    command = [
        PYTHON,
        "scripts/live_camera_preview.py",
        "--focus-mode",
        "continuous",
        "--warmup",
        "2"
    ]
    run_command(command)


def check_camera():
    command = [
        PYTHON,
        "scripts/check_camera_controls.py"
    ]
    run_command(command)


def capture_single(class_name):
    command = [
        PYTHON,
        "scripts/capture_single_image.py",
        "--class-name",
        class_name,
        "--focus-mode",
        "trigger",
        "--delay",
        "3",
        "--samples",
        "3"
    ]
    run_command(command)

def capture_multiple(class_name, count, interval):
    command = [
        PYTHON,
        "scripts/capture_dataset_images.py",
        "--class-name",
        class_name,
        "--count",
        str(count),
        "--interval",
        str(interval),
        "--focus-mode",
        "continuous",
        "--warmup",
        "3",
        "--samples",
        "3"
    ]
    run_command(command)


def count_images():
    command = [
        PYTHON,
        "scripts/count_captures.py"
    ]
    run_command(command)


def package_captures():
    command = [
        PYTHON,
        "scripts/package_captures.py"
    ]
    run_command(command)

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

def show_menu():
    print("")
    print("====================================")
    print(" MENU DE CAPTURA DE GRANADILLAS")
    print(" Raspberry Pi Camera Module 3")
    print("====================================")
    print("1. Ver camara en vivo")
    print("2. Verificar controles de camara")
    print("3. Capturar imagen de prueba")
    print("4. Capturar granadilla buena")
    print("5. Capturar granadilla golpeada")
    print("6. Capturar granadilla inmadura")
    print("7. Captura multiple")
    print("8. Contar imagenes capturadas")
    print("9. Comprimir capturas")
    print("10. Salir")
    print("====================================")

def main():
    while True:
        show_menu()
        option = input("Selecciona una opcion: ").strip()

        if option == "1":
            live_preview()

        elif option == "2":
            check_camera()

        elif option == "3":
            capture_single("prueba")

        elif option == "4":
            capture_single("buena")

        elif option == "5":
            capture_single("golpeada")

        elif option == "6":
            capture_single("inmadura")

        elif option == "7":
            ask_multiple_capture()

        elif option == "8":
            count_images()

        elif option == "9":
            package_captures()

        elif option == "10":
            print("Saliendo del menu.")
            break

        else:
            print("Opcion no valida. Intenta nuevamente.")


if __name__ == "__main__":
    main()
