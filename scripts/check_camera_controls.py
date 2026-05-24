from picamera2 import Picamera2

picam2 = Picamera2()
picam2.configure("preview")

print("")
print("Propiedades de la camara")
print("------------------------")

try:
    for key, value in picam2.camera_properties.items():
        print(f"{key}: {value}")
except Exception:
    print("No se pudieron leer propiedades.")

print("")
print("Controles disponibles")
print("---------------------")

for control_name in sorted(picam2.camera_controls.keys()):
    print(control_name)

print("")
print("Revision importante")
print("-------------------")

if "AfMode" in picam2.camera_controls:
    print("[OK] Autofocus disponible.")
else:
    print("[AVISO] Autofocus NO disponible.")

if "AfTrigger" in picam2.camera_controls:
    print("[OK] Trigger de autofocus disponible.")
else:
    print("[AVISO] Trigger de autofocus NO disponible.")

if "LensPosition" in picam2.camera_controls:
    print("[OK] Control de posicion de lente disponible.")
else:
    print("[AVISO] LensPosition NO disponible.")

if "AeEnable" in picam2.camera_controls:
    print("[OK] Autoexposicion disponible.")
else:
    print("[AVISO] Autoexposicion NO disponible.")

if "AwbEnable" in picam2.camera_controls:
    print("[OK] Balance de blancos automatico disponible.")
else:
    print("[AVISO] Balance de blancos automatico NO disponible.")

picam2.close()
