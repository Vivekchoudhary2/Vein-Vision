import cv2
from picamera2 import Picamera2
import time

print(cv2.__version__)

# Initialize camera
cam = Picamera2()
cam.preview_configuration.main.size = (640, 480)
cam.preview_configuration.main.format = "RGB888"
cam.preview_configuration.align()
cam.configure("preview")
cam.start()

tLast = time.time()
time.sleep(0.1)

# Initialize CLAHE
clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(4, 4))

while True:
    dT = time.time() - tLast
    fps = int(1 / dT)
    tLast = time.time()

    # Capture frame
    frame = cam.capture_array()

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Apply CLAHE
    enhanced = clahe.apply(gray)

    # Overlay FPS text
    cv2.putText(enhanced, f'{fps} FPS', (40, 80), cv2.FONT_HERSHEY_COMPLEX,
                1, (255), 1)

    # Display enhanced image
    cv2.imshow('CLAHE Enhanced Camera Feed', enhanced)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
