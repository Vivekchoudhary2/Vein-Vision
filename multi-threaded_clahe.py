import cv2
from picamera2 import Picamera2
import threading
import time

# === GLOBALS ===
frame = None
running = True
lock = threading.Lock()
fps = 0

# === Setup Camera ===
cam = Picamera2()
cam.preview_configuration.main.size = (640, 480)  # Lower resolution = better FPS
cam.preview_configuration.main.format = "RGB888"
cam.preview_configuration.align()
cam.configure("preview")
cam.start()
time.sleep(0.2)

# === CLAHE setup ===
clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(12, 12))


# === Thread 1: Frame Grabber ===
def capture_frames():
    global frame, running
    while running:
        temp = cam.capture_array()
        with lock:
            frame = temp


# === Thread 2: Processing + Display ===
def process_display():
    global frame, running, fps
    t_last = time.time()

    while running:
        with lock:
            if frame is None:
                continue
            current_frame = frame.copy()

        # Calculate FPS
        now = time.time()
        fps = int(1 / (now - t_last))
        t_last = now

        # Convert to Grayscale
        gray = cv2.cvtColor(current_frame, cv2.COLOR_RGB2GRAY)

        # Apply CLAHE
        clahe_img = clahe.apply(gray)

        # Overlay FPS
        cv2.putText(clahe_img, f"{fps} FPS", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)

        # Show
        cv2.imshow("CLAHE Output", clahe_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

    cv2.destroyAllWindows()


# === Launch Threads ===
thread1 = threading.Thread(target=capture_frames)
thread2 = threading.Thread(target=process_display)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
