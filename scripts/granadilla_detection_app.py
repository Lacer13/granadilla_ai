import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime
import time
import cv2
import numpy as np
from PIL import Image, ImageTk

try:
    from picamera2 import Picamera2
    PICAMERA_AVAILABLE = True
except Exception:
    Picamera2 = None
    PICAMERA_AVAILABLE = False


BASE = Path.home() / "granadilla_ai"

MODEL_CONFIGS = {
    "YOLOv3-Tiny COCO": {
        "cfg": BASE / "models/yolov3_tiny/yolov3-tiny.cfg",
        "weights": BASE / "models/yolov3_tiny/yolov3-tiny.weights",
        "names": BASE / "models/yolov3_tiny/coco.names",
    },
    "YOLOv4-Tiny COCO": {
        "cfg": BASE / "models/yolov4_tiny/yolov4-tiny.cfg",
        "weights": BASE / "models/yolov4_tiny/yolov4-tiny.weights",
        "names": BASE / "models/yolov4_tiny/coco.names",
    },
    "Modelo Granadilla Entrenado": {
        "cfg": BASE / "models/granadilla/yolo-granadilla.cfg",
        "weights": BASE / "models/granadilla/yolo-granadilla_best.weights",
        "names": BASE / "models/granadilla/obj.names",
    },
}

RESOLUTIONS = {
    "HD 1280x720": (1280, 720),
    "FHD 1920x1080": (1920, 1080),
    "QHD 2304x1296": (2304, 1296),
}

GRANADILLA_CLASSES = [
    "granadilla_buena",
    "granadilla_golpeada",
    "granadilla_inmadura",
]



class GranadillaDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Granadilla Diaz - Deteccion y Clasificacion")
        self.root.geometry("1180x650")
        self.root.minsize(1050, 600)

        # Variables principales
        self.picam2 = None
        self.camera_running = False
        self.detection_running = False

        self.net = None
        self.output_layer_names = []
        self.class_names = []

        self.current_frame = None
        self.current_annotated = None

        self.preview_width = 720
        self.preview_height = 430

        # Variables de configuracion
        self.model_var = tk.StringVar(value="Modelo Granadilla Entrenado")
        self.resolution_var = tk.StringVar(value="HD 1280x720")
        self.conf_var = tk.StringVar(value="0.35")
        self.nms_var = tk.StringVar(value="0.40")
        self.input_size_var = tk.StringVar(value="320")

        # Variables de estado
        self.status_var = tk.StringVar(value="Interfaz lista. Carga un modelo para iniciar.")
        self.fps_var = tk.StringVar(value="FPS: --")
        self.inference_var = tk.StringVar(value="Inferencia: -- ms")
        self.result_var = tk.StringVar(value="Resultado: --")
        self.detections_var = tk.StringVar(value="Detecciones: --")
        self.counts_var = tk.StringVar(value="Buenas: 0 | Malas: 0 | Golpeadas: 0 | Inmaduras: 0 | Total: 0")

        self.last_time = time.time()
        self.fps = 0.0
        self.last_inference_ms = 0.0

        self.setup_style()
        self.build_layout()
        self.bind_keys()


    def setup_style(self):
        self.root.configure(bg="#0F172A")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Main.TFrame",
            background="#0F172A"
        )

        style.configure(
            "Panel.TFrame",
            background="#1E293B",
            relief="flat"
        )

        style.configure(
            "Title.TLabel",
            background="#0F172A",
            foreground="#F8FAFC",
            font=("Arial", 23, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background="#0F172A",
            foreground="#CBD5E1",
            font=("Arial", 11)
        )

        style.configure(
            "PanelTitle.TLabel",
            background="#1E293B",
            foreground="#F8FAFC",
            font=("Arial", 13, "bold")
        )

        style.configure(
            "Text.TLabel",
            background="#1E293B",
            foreground="#E2E8F0",
            font=("Arial", 10)
        )

        style.configure(
            "Metric.TLabel",
            background="#1E293B",
            foreground="#A7F3D0",
            font=("Arial", 11, "bold")
        )

        style.configure(
            "Status.TLabel",
            background="#0F172A",
            foreground="#93C5FD",
            font=("Arial", 10)
        )

        style.configure(
            "TButton",
            font=("Arial", 10, "bold"),
            padding=8
        )


    def build_layout(self):
        main = ttk.Frame(self.root, style="Main.TFrame", padding=10)
        main.pack(fill="both", expand=True)

        header = ttk.Frame(main, style="Main.TFrame")
        header.pack(fill="x", pady=(0, 12))

        ttk.Label(
            header,
            text="Granadilla Diaz - Deteccion y Clasificacion",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Interfaz para inferencia en vivo usando Raspberry Pi Camera Module 3 y YOLO Tiny",
            style="Subtitle.TLabel"
        ).pack(anchor="w")

        content = ttk.Frame(main, style="Main.TFrame")
        content.pack(fill="both", expand=True)

        self.left_panel = ttk.Frame(content, style="Panel.TFrame", padding=10)
        self.left_panel.pack(side="left", fill="y", padx=(0, 10))

        self.right_panel = ttk.Frame(content, style="Panel.TFrame", padding=10)
        self.right_panel.pack(side="right", fill="both", expand=True)

        self.build_controls()
        self.build_preview()

        ttk.Label(
            main,
            textvariable=self.status_var,
            style="Status.TLabel"
        ).pack(fill="x", pady=(10, 0))

    def build_controls(self):
        ttk.Label(
            self.left_panel,
            text="Modelo de deteccion",
            style="PanelTitle.TLabel"
        ).pack(anchor="w", pady=(0, 5))

        model_box = ttk.Combobox(
            self.left_panel,
            textvariable=self.model_var,
            values=list(MODEL_CONFIGS.keys()),
            state="readonly",
            width=25
        )
        model_box.pack(fill="x", pady=(0, 5))

        ttk.Button(
            self.left_panel,
            text="Cargar modelo",
            command=self.load_model
        ).pack(fill="x", pady=2)

        ttk.Separator(self.left_panel).pack(fill="x", pady=8)

        ttk.Label(
            self.left_panel,
            text="Configuracion de camara",
            style="PanelTitle.TLabel"
        ).pack(anchor="w", pady=(0, 5))

        ttk.Label(
            self.left_panel,
            text="Resolucion",
            style="Text.TLabel"
        ).pack(anchor="w")

        resolution_box = ttk.Combobox(
            self.left_panel,
            textvariable=self.resolution_var,
            values=list(RESOLUTIONS.keys()),
            state="readonly",
            width=25
        )
        resolution_box.pack(fill="x", pady=(0, 5))

        self.camera_button = ttk.Button(
            self.left_panel,
            text="Iniciar camara",
            command=self.toggle_camera
        )
        self.camera_button.pack(fill="x", pady=2)

        ttk.Separator(self.left_panel).pack(fill="x", pady=8)

        ttk.Label(
            self.left_panel,
            text="Parametros de inferencia",
            style="PanelTitle.TLabel"
        ).pack(anchor="w", pady=(0, 5))

        ttk.Label(
            self.left_panel,
            text="Tamano de entrada YOLO",
            style="Text.TLabel"
        ).pack(anchor="w")

        input_box = ttk.Combobox(
            self.left_panel,
            textvariable=self.input_size_var,
            values=["320", "416"],
            state="readonly",
            width=10
        )
        input_box.pack(anchor="w", pady=(0, 5))

        ttk.Label(self.left_panel, text="Confianza minima", style="Text.TLabel").pack(anchor="w")

        ttk.Entry(
            self.left_panel,
            textvariable=self.conf_var,
            width=10
        ).pack(anchor="w", pady=(0, 2))

        ttk.Label(
            self.left_panel,
            text="Rango: 0.10 a 0.90 | recomendado: 0.35 a 0.45",
            style="Text.TLabel",
            wraplength=220
        ).pack(anchor="w", pady=(0, 5))

        ttk.Label(self.left_panel, text="NMS", style="Text.TLabel").pack(anchor="w")

        ttk.Entry(
            self.left_panel,
            textvariable=self.nms_var,
            width=10
        ).pack(anchor="w", pady=(0, 2))

        ttk.Label(
            self.left_panel,
            text="Rango: 0.10 a 0.90 | recomendado: 0.40",
            style="Text.TLabel",
            wraplength=220
        ).pack(anchor="w", pady=(0, 6))

        self.detect_button = ttk.Button(
            self.left_panel,
            text="Iniciar deteccion",
            command=self.toggle_detection
        )
        self.detect_button.pack(fill="x", pady=2)

        ttk.Separator(self.left_panel).pack(fill="x", pady=8)

        ttk.Label(self.left_panel, text="Metricas en vivo", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 5))

        ttk.Label(self.left_panel, textvariable=self.fps_var, style="Metric.TLabel").pack(anchor="w", pady=1)
        ttk.Label(self.left_panel, textvariable=self.inference_var, style="Metric.TLabel").pack(anchor="w", pady=1)

        ttk.Label(
            self.left_panel,
            textvariable=self.result_var,
            style="Metric.TLabel",
            wraplength=230
        ).pack(anchor="w", pady=(3, 2))

        ttk.Label(
            self.left_panel,
            textvariable=self.counts_var,
            style="Metric.TLabel",
            wraplength=230,
            justify="left"
        ).pack(anchor="w", pady=(3, 4))

        ttk.Label(
            self.left_panel,
            textvariable=self.detections_var,
            style="Text.TLabel",
            wraplength=230,
            justify="left"
        ).pack(anchor="w", pady=(2, 6))

        ttk.Button(
            self.left_panel,
            text="Guardar imagen detectada",
            command=self.save_detection_image
        ).pack(fill="x", pady=2)


    def build_preview(self):
        ttk.Label(
            self.right_panel,
            text="Vista de deteccion",
            style="PanelTitle.TLabel"
        ).pack(anchor="w", pady=(0, 8))

        self.preview_label = tk.Label(
            self.right_panel,
            bg="#020617",
            width=self.preview_width,
            height=self.preview_height
        )
        self.preview_label.pack(fill="both", expand=True)

        ttk.Label(
            self.right_panel,
            text="Atajos: q = salir | d = iniciar/detener deteccion | s = guardar imagen",
            style="Text.TLabel"
        ).pack(anchor="w", pady=(10, 0))

    def load_model(self):
        try:
            selected = self.model_var.get()
            model_info = MODEL_CONFIGS[selected]

            cfg_path = model_info["cfg"]
            weights_path = model_info["weights"]
            names_path = model_info["names"]

            missing = []

            for path in [cfg_path, weights_path, names_path]:
                if not path.exists():
                    missing.append(str(path))

            if missing:
                message = "Faltan archivos del modelo:" + chr(10) + chr(10) + chr(10).join(missing)
                messagebox.showwarning("Archivos faltantes", message)
                self.status_var.set("No se pudo cargar el modelo. Faltan archivos.")
                return

            self.class_names = self.load_class_names(names_path)

            self.net = cv2.dnn.readNetFromDarknet(
                str(cfg_path),
                str(weights_path)
            )

            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

            layer_names = self.net.getLayerNames()
            output_layers = self.net.getUnconnectedOutLayers()

            self.output_layer_names = [
                layer_names[int(i) - 1] for i in output_layers.flatten()
            ]

            self.status_var.set(f"Modelo cargado: {selected}")

        except Exception as error:
            messagebox.showerror("Error al cargar modelo", str(error))
            self.status_var.set("Error al cargar modelo.")

    def toggle_camera(self):
        if self.camera_running:
            self.stop_camera()
        else:
            self.start_camera()


    def start_camera(self):
        if self.camera_running:
            self.status_var.set("La camara ya esta iniciada.")
            return

        if not PICAMERA_AVAILABLE:
            messagebox.showerror(
                "Picamera2 no disponible",
                "No se pudo importar Picamera2. Revisar instalacion en Raspberry."
            )
            return

        try:
            width, height = RESOLUTIONS[self.resolution_var.get()]

            self.picam2 = Picamera2()

            config = self.picam2.create_preview_configuration(
                main={
                    "size": (width, height),
                    "format": "RGB888"
                }
            )

            self.picam2.configure(config)
            self.picam2.start()

            self.camera_running = True
            self.status_var.set(f"Camara iniciada en {width}x{height}.")

            if hasattr(self, "camera_button"):
                self.camera_button.configure(text="Detener camara")
            self.last_time = time.time()
            self.update_loop()

        except Exception as error:
            messagebox.showerror("Error al iniciar camara", str(error))
            self.camera_running = False

    def stop_camera(self):
        self.camera_running = False
        self.detection_running = False

        if self.picam2 is not None:
            try:
                self.picam2.stop()
                self.picam2.close()
            except Exception:
                pass

        self.picam2 = None
        self.preview_label.configure(image="")
        self.preview_label.image = None
        self.status_var.set("Camara detenida.")

        if hasattr(self, "camera_button"):
            self.camera_button.configure(text="Iniciar camara")

    def update_loop(self):
        if not self.camera_running or self.picam2 is None:
            return

        try:
            frame_rgb = self.picam2.capture_array()
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

            annotated = frame_bgr.copy()
            detections = []

            if self.detection_running:
                annotated, detections = self.run_detection(annotated)

            self.current_frame = frame_bgr
            self.current_annotated = annotated.copy()

            self.update_metrics(detections)
            self.show_frame(annotated)

        except Exception as error:
            self.status_var.set("Error en deteccion: " + str(error))

        self.root.after(10, self.update_loop)

    def show_frame(self, frame_bgr):
        display = cv2.resize(
            frame_bgr,
            (self.preview_width, self.preview_height)
        )

        cv2.putText(
            display,
            f"{self.fps_var.get()} | {self.inference_var.get()}",
            (18, 34),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        display_rgb = cv2.cvtColor(display, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(display_rgb)
        photo = ImageTk.PhotoImage(image=image)

        self.preview_label.configure(image=photo)
        self.preview_label.image = photo

    def run_detection(self, frame_bgr):
        if self.net is None:
            return frame_bgr, []

        height, width = frame_bgr.shape[:2]
        input_size = int(self.input_size_var.get())

        try:
            conf_threshold = float(self.conf_var.get())
            nms_threshold = float(self.nms_var.get())
        except ValueError:
            self.status_var.set("Confianza y NMS deben ser numeros. Ejemplo: 0.35")
            return frame_bgr, []

        if not (0.01 <= conf_threshold <= 0.99):
            self.status_var.set("Confianza debe estar entre 0.01 y 0.99")
            return frame_bgr, []

        if not (0.01 <= nms_threshold <= 0.99):
            self.status_var.set("NMS debe estar entre 0.01 y 0.99")
            return frame_bgr, []

        blob = cv2.dnn.blobFromImage(
            frame_bgr,
            scalefactor=1 / 255.0,
            size=(input_size, input_size),
            swapRB=True,
            crop=False
        )

        start_time = time.time()

        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layer_names)

        self.last_inference_ms = (time.time() - start_time) * 1000.0

        boxes = []
        confidences = []
        class_ids = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = int(np.argmax(scores))
                confidence = float(scores[class_id])

                if confidence > conf_threshold:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    box_w = int(detection[2] * width)
                    box_h = int(detection[3] * height)

                    x = int(center_x - box_w / 2)
                    y = int(center_y - box_h / 2)

                    boxes.append([x, y, box_w, box_h])
                    confidences.append(confidence)
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(
            boxes,
            confidences,
            conf_threshold,
            nms_threshold
        )

        detections = []

        if len(indices) > 0:
            for i in np.array(indices).flatten():
                x, y, box_w, box_h = boxes[int(i)]
                class_id = class_ids[int(i)]
                confidence = confidences[int(i)]

                if class_id < len(self.class_names):
                    label = self.class_names[class_id]
                else:
                    label = str(class_id)

                detections.append({
                    "label": label,
                    "confidence": confidence,
                    "box": [x, y, box_w, box_h]
                })

                color = (0, 255, 0)

                if "golpeada" in label:
                    color = (0, 0, 255)
                elif "inmadura" in label:
                    color = (0, 255, 255)
                elif "buena" in label:
                    color = (0, 255, 0)

                cv2.rectangle(
                    frame_bgr,
                    (x, y),
                    (x + box_w, y + box_h),
                    color,
                    2
                )

                text = f"{label} {confidence:.2f}"

                cv2.putText(
                    frame_bgr,
                    text,
                    (x, max(y - 8, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2
                )

        return frame_bgr, detections

    def update_metrics(self, detections):
        now = time.time()
        delta = now - self.last_time

        if delta > 0:
            self.fps = 1.0 / delta

        self.last_time = now

        self.fps_var.set(f"FPS: {self.fps:.2f}")
        self.inference_var.set(f"Inferencia: {self.last_inference_ms:.1f} ms")

        if not detections:
            if self.detection_running:
                self.result_var.set("Resultado: sin deteccion")
            else:
                self.result_var.set("Resultado: deteccion detenida")

            self.counts_var.set(
                "Buenas: 0 | Malas: 0 | Golpeadas: 0 | Inmaduras: 0 | Total: 0"
            )
            self.detections_var.set("Detecciones: --")
            return

        counts = {}

        for det in detections:
            label = det["label"]
            counts[label] = counts.get(label, 0) + 1

        buenas = sum(
            count for label, count in counts.items()
            if "buena" in label
        )

        golpeadas = sum(
            count for label, count in counts.items()
            if "golpeada" in label
        )

        inmaduras = sum(
            count for label, count in counts.items()
            if "inmadura" in label
        )

        malas_directas = sum(
            count for label, count in counts.items()
            if "mala" in label
        )

        malas = golpeadas + inmaduras + malas_directas
        total = len(detections)

        self.counts_var.set(
            f"Buenas: {buenas} | Malas: {malas} | "
            f"Golpeadas: {golpeadas} | Inmaduras: {inmaduras} | Total: {total}"
        )

        dominant = max(
            detections,
            key=lambda item: item["confidence"]
        )

        dominant_label = dominant["label"]
        dominant_confidence = dominant["confidence"]

        self.result_var.set(
            f"Resultado: {dominant_label} ({dominant_confidence:.2f})"
        )

        lines = []
        lines.append("Confianzas:")

        for det in detections[:6]:
            label = det["label"]
            confidence = det["confidence"]
            lines.append(f"- {label}: {confidence:.2f}")

        self.detections_var.set(
            "Detecciones:\n" + "\n".join(lines)
        )


    def start_detection(self):
        if self.net is None:
            self.status_var.set("Primero carga un modelo.")
            messagebox.showwarning(
                "Modelo no cargado",
                "Primero debes cargar un modelo YOLO."
            )
            return

        if not self.camera_running:
            self.status_var.set("Primero inicia la camara.")
            messagebox.showwarning(
                "Camara detenida",
                "Primero debes iniciar la camara."
            )
            return

        self.detection_running = True
        self.status_var.set("Deteccion iniciada.")

        if hasattr(self, "detect_button"):
            self.detect_button.configure(text="Detener deteccion")

        if hasattr(self, "detect_button"):
            self.detect_button.configure(text="Detener deteccion")

    def stop_detection(self):
        self.detection_running = False
        self.status_var.set("Deteccion detenida.")

        if hasattr(self, "detect_button"):
            self.detect_button.configure(text="Iniciar deteccion")

        if hasattr(self, "detect_button"):
            self.detect_button.configure(text="Iniciar deteccion")

    def save_detection_image(self):
        if self.current_annotated is None:
            self.status_var.set("No hay imagen para guardar.")
            messagebox.showwarning(
                "Sin imagen",
                "No hay una imagen detectada para guardar."
            )
            return

        output_dir = BASE / "results" / "detections"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"detection_{timestamp}.jpg"

        cv2.imwrite(str(output_path), self.current_annotated)

        self.status_var.set(f"Imagen guardada: {output_path}")
        messagebox.showinfo(
            "Imagen guardada",
            f"La imagen fue guardada en:\n{output_path}"
        )

    def bind_keys(self):
        self.root.bind("q", lambda event: self.close_app())
        self.root.bind("s", lambda event: self.save_detection_image())
        self.root.bind("d", lambda event: self.toggle_detection())
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def toggle_detection(self):
        if self.detection_running:
            self.stop_detection()
        else:
            self.start_detection()

    def close_app(self):
        self.stop_camera()
        self.root.destroy()



    def setup_style(self):
        self.root.configure(bg="#0F172A")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Main.TFrame",
            background="#0F172A"
        )

        style.configure(
            "Panel.TFrame",
            background="#1E293B",
            relief="flat"
        )

        style.configure(
            "Title.TLabel",
            background="#0F172A",
            foreground="#F8FAFC",
            font=("Arial", 23, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background="#0F172A",
            foreground="#CBD5E1",
            font=("Arial", 11)
        )

        style.configure(
            "PanelTitle.TLabel",
            background="#1E293B",
            foreground="#F8FAFC",
            font=("Arial", 13, "bold")
        )

        style.configure(
            "Text.TLabel",
            background="#1E293B",
            foreground="#E2E8F0",
            font=("Arial", 10)
        )

        style.configure(
            "Metric.TLabel",
            background="#1E293B",
            foreground="#A7F3D0",
            font=("Arial", 11, "bold")
        )

        style.configure(
            "Status.TLabel",
            background="#0F172A",
            foreground="#93C5FD",
            font=("Arial", 10)
        )

        style.configure(
            "TButton",
            font=("Arial", 10, "bold"),
            padding=8
        )


def main():
    root = tk.Tk()
    app = GranadillaDetectionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
