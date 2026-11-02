
import os
import cv2
import json
import socket
import numpy as np

from pathlib import Path
from dotenv import load_dotenv
from pupil_apriltags import Detector

# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

CAMERA_URL = os.getenv(
    "PHONE_CAMERA_URL",
    "http://192.168.1.100:8080/video"
)

TAG_SIZE = 0.04
TAG_ID = 0

VIEWER_ADDRESS = ("127.0.0.1", 5005)

POSITION_ALPHA = 0.15
ROTATION_ALPHA = 0.12

# --------------------------------------------------
# Camera setup
# --------------------------------------------------

cap = cv2.VideoCapture(CAMERA_URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    raise RuntimeError(
        "Could not connect to phone camera. "
        "Check PHONE_CAMERA_URL in .env."
    )

detector = Detector(
    families="tag36h11",
    nthreads=2
)

# Approximate camera parameters
width = 640
height = 480

fx = 0.9 * width
fy = 0.9 * width
cx = width / 2
cy = height / 2

camera_matrix = np.array([
    [fx, 0, cx],
    [0, fy, cy],
    [0,  0,  1]
], dtype=np.float64)

distortion = np.zeros((5, 1), dtype=np.float64)

# UDP connection
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# --------------------------------------------------
# Rotation conversion
# --------------------------------------------------

def rotation_to_quaternion(R):
    trace = np.trace(R)

    if trace > 0:
        s = np.sqrt(trace + 1.0) * 2
        w = 0.25 * s
        x = (R[2, 1] - R[1, 2]) / s
        y = (R[0, 2] - R[2, 0]) / s
        z = (R[1, 0] - R[0, 1]) / s

    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = np.sqrt(
            1.0 + R[0, 0] - R[1, 1] - R[2, 2]
        ) * 2

        w = (R[2, 1] - R[1, 2]) / s
        x = 0.25 * s
        y = (R[0, 1] + R[1, 0]) / s
        z = (R[0, 2] + R[2, 0]) / s

    elif R[1, 1] > R[2, 2]:
        s = np.sqrt(
            1.0 + R[1, 1] - R[0, 0] - R[2, 2]
        ) * 2

        w = (R[0, 2] - R[2, 0]) / s
        x = (R[0, 1] + R[1, 0]) / s
        y = 0.25 * s
        z = (R[1, 2] + R[2, 1]) / s

    else:
        s = np.sqrt(
            1.0 + R[2, 2] - R[0, 0] - R[1, 1]
        ) * 2

        w = (R[1, 0] - R[0, 1]) / s
        x = (R[0, 2] + R[2, 0]) / s
        y = (R[1, 2] + R[2, 1]) / s
        z = 0.25 * s

    q = np.array([w, x, y, z], dtype=np.float64)
    return q / np.linalg.norm(q)


def smooth_quaternion(previous, current, alpha):
    # q and -q represent the same rotation.
    if np.dot(previous, current) < 0:
        current = -current

    result = (
        (1 - alpha) * previous
        + alpha * current
    )

    return result / np.linalg.norm(result)


# --------------------------------------------------
# Tracking state
# --------------------------------------------------

smoothed_position = None
smoothed_rotation = None

object_points = np.array([
    [-TAG_SIZE / 2, -TAG_SIZE / 2, 0],
    [ TAG_SIZE / 2, -TAG_SIZE / 2, 0],
    [ TAG_SIZE / 2,  TAG_SIZE / 2, 0],
    [-TAG_SIZE / 2,  TAG_SIZE / 2, 0]
], dtype=np.float32)

print("AprilTag tracking started!")
print("Camera:", CAMERA_URL)
print("Target tag: ID 0, family tag36h11")
print("Sending pose to Viser at UDP port 5005.")
print("Press Q to exit.")

# --------------------------------------------------
# Main tracking loop
# --------------------------------------------------

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

        if tag is not None:
            corners = tag.corners.astype(np.float32)

            success, rvec, tvec = cv2.solvePnP(
                object_points,
                corners,
                camera_matrix,
                distortion,
                flags=cv2.SOLVEPNP_IPPE_SQUARE
            )

            if success:
                R, _ = cv2.Rodrigues(rvec)

                current_position = tvec.flatten()
                current_rotation = rotation_to_quaternion(R)

                # Initialize smoothing
                if smoothed_position is None:
                    smoothed_position = current_position.copy()
                    smoothed_rotation = current_rotation.copy()

                else:
                    # Smooth position
                    smoothed_position = (
                        (1 - POSITION_ALPHA) * smoothed_position
                        + POSITION_ALPHA * current_position
                    )

                    # Smooth rotation
                    smoothed_rotation = smooth_quaternion(
                        smoothed_rotation,
                        current_rotation,
                        ROTATION_ALPHA
                    )

                # Send pose to Viser
                pose_data = {
                    "position": smoothed_position.tolist(),
                    "rotation": smoothed_rotation.tolist()
                }

                sock.sendto(
                    json.dumps(pose_data).encode("utf-8"),
                    VIEWER_ADDRESS
                )

                # Draw detected marker and axes
                cv2.polylines(
                    frame,
                    [corners.astype(np.int32)],
                    True,
                    (0, 255, 0),
                    2
                )

                cv2.drawFrameAxes(
                    frame,
                    camera_matrix,
                    distortion,
                    rvec,
                    tvec,
                    0.005,
                    2
                )

                cv2.putText(
                    frame,
                    "AprilTag ID: 0 - TRACKING",
                    (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 255, 0),
                    2
                )

        else:
            cv2.putText(
                frame,
                "AprilTag not detected",
                (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 0, 255),
                2
            )

        cv2.imshow("Brain Registration - Tracking", frame)

        if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
            break

finally:
    cap.release()
    sock.close()
    cv2.destroyAllWindows()
    print("Tracking stopped.")
