
import cv2
from pathlib import Path

# Resolve project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"

ASSETS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = ASSETS_DIR / "apriltag_0.png"

# AprilTag configuration
TAG_ID = 0
TAG_SIZE = 600
MARGIN = 100

# Create AprilTag 36h11 dictionary
dictionary = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_APRILTAG_36h11
)

# Generate marker
marker = cv2.aruco.generateImageMarker(
    dictionary,
    TAG_ID,
    TAG_SIZE
)

# Add white margin around marker
image_size = TAG_SIZE + 2 * MARGIN

image = 255 * (
    cv2.UMat(image_size, image_size, cv2.CV_8UC1).get()
)

image[
    MARGIN:MARGIN + TAG_SIZE,
    MARGIN:MARGIN + TAG_SIZE
] = marker

# Save image
success = cv2.imwrite(str(OUTPUT_PATH), image)

if not success:
    raise RuntimeError("Could not save AprilTag image.")

print("AprilTag generated successfully!")
print("Family: tag36h11")
print("ID:", TAG_ID)
print("Saved to:", OUTPUT_PATH)
print("Print the black square at 4 cm wide.")
