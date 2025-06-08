import cv2
from picamera2 import Picamera2
import time

print(cv2.__version__)

cam = Picamera2()
cam.preview_configuration.main.size = (640, 480)
cam.preview_configuration.main.format = "RGB888"
cam.preview_configuration.align()
cam.configure("preview")
cam.start()

tLast = time.time()
time.sleep(0.1)

while True:
    dT = time.time() - tLast
    fps = int(1 / dT)
    tLast = time.time()

    frame = cam.capture_array()

    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Apply histogram equalization
    equalized_frame = cv2.equalizeHist(gray_frame)

    # Display FPS on the equalized grayscale image
    cv2.putText(equalized_frame, (str(fps) + ' FPS'), (40, 80),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255), 1)

    cv2.imshow('Histogram Equalized Grayscale WebCam', equalized_frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
