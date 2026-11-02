
import cv2
import threading
import time

URL = "http://10.107.148.73:8080/video"

cap = cv2.VideoCapture(URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

latest_frame = None
lock = threading.Lock()
running = True

def read_camera():
    global latest_frame, running

    while running:
        ret, frame = cap.read()

        if ret:
            with lock:
                latest_frame = frame
        else:
            time.sleep(0.01)

thread = threading.Thread(target=read_camera, daemon=True)
thread.start()

print("Camera started. Press Q to quit.")

while True:
    with lock:
        frame = latest_frame.copy() if latest_frame is not None else None

    if frame is not None:
        # Resize only for display; this does not change camera zoom.
        display = cv2.resize(frame, (1000, 650))
        cv2.imshow("Phone Camera - Live Feed", display)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

running = False
thread.join(timeout=1)
cap.release()
cv2.destroyAllWindows()
