
import cv2
import numpy as np
from pupil_apriltags import Detector

URL = "http://10.107.148.73:8080/video"
TAG_ID = 0

cap = cv2.VideoCapture(URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

detector = Detector(families="tag36h11", nthreads=2)

captures = []
image_size = None

print("AprilTag calibration")
print("--------------------")
print("SPACE = capture a view")
print("Q = save and exit")
print("Capture different angles and positions.")

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = detector.detect(gray)

        tag = next(
            (d for d in detections if d.tag_id == TAG_ID),
            None
        )

        display = frame.copy()

        if tag is not None:
            corners = tag.corners.astype(np.float32)

            cv2.polylines(
                display,
                [corners.astype(np.int32)],
                True, (0, 255, 0), 2
            )

            cv2.putText(
                display, "TAG DETECTED",
                (20, 35), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2
            )

        cv2.putText(
            display, f"Captures: {len(captures)}",
            (20, 70), cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (255, 255, 0), 2
        )

        cv2.imshow("Camera Calibration", display)

        key = cv2.waitKey(1) & 0xFF

        if key in (ord('q'), ord('Q')):
            break

        elif key == 32 and tag is not None:
            captures.append(tag.corners.astype(np.float32))
            image_size = (gray.shape[1], gray.shape[0])
            print(f"Captured view {len(captures)}")

finally:
    cap.release()
    cv2.destroyAllWindows()

if len(captures) >= 20:
    np.savez(
        "calibration_points.npz",
        corners=np.array(captures),
        image_size=np.array(image_size)
    )
    print(f"Saved {len(captures)} calibration views!")
else:
    print(f"Only {len(captures)} views. Need at least 20.")
