# Dataset de granadillas

## Objetivo del dataset

Recolectar imagenes de granadillas para entrenar un modelo capaz de detectar y clasificar el fruto segun su estado visual.

## Clases

| ID | Clase | Descripcion |
|---|---|---|
| 0 | granadilla_buena | Fruto en buen estado visual |
| 1 | granadilla_golpeada | Fruto con manchas, golpes o dano visible |
| 2 | granadilla_inmadura | Fruto verde o con coloracion no comercial |

## Cantidad inicial recomendada

- 150 imagenes de granadilla_buena
- 150 imagenes de granadilla_golpeada
- 150 imagenes de granadilla_inmadura

Total inicial recomendado: 450 imagenes.

## Division recomendada

- 70% entrenamiento
- 20% validacion
- 10% prueba

## Recomendaciones de captura

- Usar fondo uniforme.
- Mantener distancia fija entre camara y fruta.
- Evitar imagenes borrosas.
- Capturar diferentes orientaciones de la granadilla.
- Tomar fotos con diferentes condiciones de luz.
- Incluir una referencia de escala si se desea medir tamano.
- Evitar sombras fuertes.
- No mezclar frutas muy tapadas o superpuestas en las primeras pruebas.

## Medicion de tamano

El tamano no se entrenara como clase inicialmente. Se estimara con OpenCV usando:

1. Caja detectada por YOLO.
2. Ancho y alto en pixeles.
3. Factor de conversion px/cm.
4. Diametro estimado.

## Clasificacion de tamano propuesta

- Pequena: diametro menor a 6.0 cm
- Mediana: diametro entre 6.0 cm y 7.5 cm
- Grande: diametro mayor a 7.5 cm
