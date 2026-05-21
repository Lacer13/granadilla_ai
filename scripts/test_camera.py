from picamera2 import Picamera2
import cv2
import time
import os

os.makedirs("captures", exist_ok=True)

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")

picam2.start()
time.sleep(2)

frame = picam2.capture_array()
cv2.imwrite("captures/test_picamera2.jpg", frame)

picam2.stop()

print("Imagen guardada en captures/test_picamera2.jpg")
