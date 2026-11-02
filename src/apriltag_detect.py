
import os
import cv2
import threading
from pathlib import Path
from dotenv import load_dotenv
from pupil_apriltags import Detector

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

CAMERA_URL = os.getenv(
    "PHONE_CAMERA_URL",
    "http://192.168.1.100:8080/video"
)

TAG_ID = 0

detector = Detector(
    families="tag36h11",
    nthreads=2
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

print("AprilTag detection started!")
print("Looking for tag36h11, ID 0.")
print("Press Q to exit.")

try:
    while running:
        with frame_lock:
            frame = (
                latest_frame.copy()
                if latest_frame is not None
                else None
            )

        if frame is None:
            cv2.waitKey(1)
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = detector.detect(gray)

        for tag in detections:
            if tag.tag_id != TAG_ID:
                continue

            corners = tag.corners.astype(int)

            for i in range(4):
                p1 = tuple(corners[i])
                p2 = tuple(corners[(i + 1) % 4])
                cv2.line(frame, p1, p2, (0, 255, 0), 2)

            center = tuple(tag.center.astype(int))

            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            cv2.putText(
                frame,
                f"AprilTag ID: {tag.tag_id}",
                (center[0] + 10, center[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        cv2.imshow("AprilTag Detection", frame)

        if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
            break

finally:
    running = False
    thread.join(timeout=2)
    cv2.destroyAllWindows()
