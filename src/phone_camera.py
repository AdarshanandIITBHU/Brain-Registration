
import os
import cv2
import threading
from pathlib import Path
from dotenv import load_dotenv

# Load configuration from project-root .env
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

CAMERA_URL = os.getenv(
    "PHONE_CAMERA_URL",
    "http://192.168.1.100:8080/video"
)

latest_frame = None
frame_lock = threading.Lock()
running = True


def camera_reader():
    global latest_frame, running

    cap = cv2.VideoCapture(CAMERA_URL)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        print("ERROR: Could not connect to phone camera.")
        print("Check PHONE_CAMERA_URL in your .env file.")
        running = False
        return

    print("Connected to phone camera.")

    while running:
        ret, frame = cap.read()

        if not ret:
            continue

        with frame_lock:
            latest_frame = frame

    cap.release()


thread = threading.Thread(target=camera_reader, daemon=True)
thread.start()

print("Press Q to exit.")

try:
    while running:
        with frame_lock:
            frame = (
                latest_frame.copy()
                if latest_frame is not None
                else None
            )

        if frame is not None:
            cv2.imshow("Phone Camera", frame)

        if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
            break

finally:
    running = False
    thread.join(timeout=2)
    cv2.destroyAllWindows()
