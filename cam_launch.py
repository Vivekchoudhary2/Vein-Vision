import cv2
from picamera2 import Picamera2
import time

print(cv2.__version__)

cam=Picamera2()
cam.preview_configuration.main.size = (1280,720)
cam.preview_configuration.main.format="RGB888"
cam.preview_configuration.align()
cam.configure("preview")
cam.start()

tLast=time.time()
time.sleep(0.1)

while True:
    dT=time.time()-tLast
    fps=int(1/dT)
    print(fps)
    tLast=time.time()
    frame=cam.capture_array()
    cv2.putText(frame, (str(fps)+' FPS'), (40,80), cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255),1)
    cv2.imshow('My webCam', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cv2.destroyAllWindows()
