import cv2
import numpy as np

print("OpenCV version:", cv2.__version__)

img = np.zeros((400, 600, 3), dtype=np.uint8)
cv2.circle(img, (300, 200), 80, (0, 255, 0), -1)

cv2.imwrite("results/test_opencv.png", img)

print("Imagen creada en results/test_opencv.png")
