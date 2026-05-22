# Checklist antes de entrenar

## Imagenes

- [ ] Hay imagenes suficientes de granadilla_buena.
- [ ] Hay imagenes suficientes de granadilla_golpeada.
- [ ] Hay imagenes suficientes de granadilla_inmadura.
- [ ] Se eliminaron imagenes borrosas.
- [ ] Se eliminaron imagenes oscuras o sobreexpuestas.
- [ ] Las imagenes tienen buena variedad de orientaciones.

## Etiquetado

- [ ] Todas las imagenes tienen cajas delimitadoras.
- [ ] Las clases estan escritas correctamente.
- [ ] No hay etiquetas vacias innecesarias.
- [ ] Cada imagen tiene su archivo .txt correspondiente.

## Dataset

- [ ] El dataset fue exportado en formato YOLO Darknet.
- [ ] Existe train.txt.
- [ ] Existe valid.txt.
- [ ] Existe obj.names.
- [ ] Existe obj.data.
- [ ] Las rutas de train.txt y valid.txt son correctas.

## Colab

- [ ] GPU activada.
- [ ] Darknet clonado.
- [ ] Darknet compilado.
- [ ] Dataset cargado.
- [ ] cfg personalizado creado.
- [ ] Pesos preentrenados descargados.

## Raspberry

- [ ] Se descargaron los mejores pesos .weights.
- [ ] Se copio el .cfg personalizado.
- [ ] Se copio el archivo .names.
- [ ] Se probo inferencia.
- [ ] Se registro FPS y tiempo de inferencia.
