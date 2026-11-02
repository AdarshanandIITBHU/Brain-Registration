
import cv2
import numpy as np

data = np.load("calibration_points.npz")

captures = data["corners"]
image_size = tuple(data["image_size"])

# Actual AprilTag outer black-square dimensions: 4 cm
TAG_SIZE = 0.04

# Four corners in the tag's coordinate system
object_points = np.array([
    [-TAG_SIZE / 2, -TAG_SIZE / 2, 0],
    [ TAG_SIZE / 2, -TAG_SIZE / 2, 0],
    [ TAG_SIZE / 2,  TAG_SIZE / 2, 0],
    [-TAG_SIZE / 2,  TAG_SIZE / 2, 0]
], dtype=np.float32)

object_points_all = [
    object_points.copy() for _ in captures
]

image_points_all = [
    corners.astype(np.float32) for corners in captures
]

# Estimate camera parameters
rms, camera_matrix, distortion, rvecs, tvecs = (
    cv2.calibrateCamera(
        object_points_all,
        image_points_all,
        image_size,
        None,
        None
    )
)

print("\nCAMERA CALIBRATION RESULTS")
print("--------------------------")
print("RMS error:", rms)
print("\nCamera matrix:")
print(camera_matrix)
print("\nDistortion coefficients:")
print(distortion)

np.savez(
    "camera_calibration.npz",
    camera_matrix=camera_matrix,
    distortion=distortion,
    image_size=np.array(image_size),
    rms=rms
)

print("\nSaved camera_calibration.npz")
