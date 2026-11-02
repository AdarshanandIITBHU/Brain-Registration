
import cv2
from pupil_apriltags import Detector

# Phone camera stream
URL = "http://172.20.88.202:8080/video"

# Initialize AprilTag detector
detector = Detector(
    families="tag36h11",
    nthreads=2,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25
)

# Connect camera
cap = cv2.VideoCapture(URL)

if not cap.isOpened():
    print("ERROR: Cannot connect to phone camera")
    exit()

print("AprilTag detector started!")
print("Looking for tag36h11 markers...")
print("Press Q to quit.")

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Camera frame unavailable")
            break

        # Convert image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect AprilTags
        results = detector.detect(gray)

        for tag in results:
            # Get tag ID
            tag_id = tag.tag_id

            # Get four corners
            corners = tag.corners.astype(int)

            # Draw marker boundary
            for i in range(4):
                p1 = tuple(corners[i])
                p2 = tuple(corners[(i + 1) % 4])

                cv2.line(
                    frame, p1, p2,
                    (0, 255, 0), 3
                )

            # Calculate center
            center = tuple(tag.center.astype(int))

            cv2.circle(
                frame, center,
                6, (0, 0, 255), -1
            )

            # Display tag ID
            cv2.putText(
                frame,
                f"AprilTag ID: {tag_id}",
                (center[0] - 80, center[1] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            print(
                f"Detected Tag ID: {tag_id}, "
                f"Center: {center}"
            )

        # Display detection status
        if len(results) > 0:
            status = "APRILTAG DETECTED"
            color = (0, 255, 0)
        else:
            status = "SEARCHING FOR APRILTAG..."
            color = (0, 0, 255)

        cv2.putText(
            frame,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        cv2.imshow(
            "Brain Registration - AprilTag Detection",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
