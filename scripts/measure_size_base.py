def estimate_diameter_cm(box_width_px, box_height_px, px_per_cm):
    diameter_px = (box_width_px + box_height_px) / 2
    diameter_cm = diameter_px / px_per_cm
    return diameter_cm


def classify_size(diameter_cm):
    if diameter_cm < 6.0:
        return "pequena"
    elif diameter_cm <= 7.5:
        return "mediana"
    else:
        return "grande"


# Ejemplo simulado:
# Supongamos que OpenCV/YOLO detecta una granadilla con caja de 220 x 210 pixeles.
box_width_px = 220
box_height_px = 210

# Valor referencial provisional.
# Luego se calculara con una regla, hoja A4 o patron conocido.
px_per_cm = 30

diameter_cm = estimate_diameter_cm(box_width_px, box_height_px, px_per_cm)
size_class = classify_size(diameter_cm)

print("Medicion simulada de granadilla")
print("-------------------------------")
print("Ancho caja px:", box_width_px)
print("Alto caja px:", box_height_px)
print("Escala px/cm:", px_per_cm)
print("Diametro estimado cm:", round(diameter_cm, 2))
print("Clasificacion por tamano:", size_class)
