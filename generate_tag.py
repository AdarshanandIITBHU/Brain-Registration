import cv2
import numpy as np

from pupil_apriltags import Detector

# AprilTag configuration
tag_id = 0
tag_size = 600

# Create AprilTag detector
detector = Detector(
    families="tag36h11"
)

# Generate a test image
image = np.ones(
    (tag_size, tag_size),
    dtype=np.uint8
) * 255

# Generate AprilTag using OpenCV ArUco
aruco = cv2.aruco
dictionary = aruco.getPredefinedDictionary(
    aruco.DICT_APRILTAG_36h11
)

tag = aruco.generateImageMarker(
    dictionary,
    tag_id,
    tag_size
)

cv2.imwrite("apriltag_0.png", tag)

print("AprilTag generated successfully!")
print("Tag ID:", tag_id)