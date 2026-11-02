
import cv2

# Open default webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Cannot access camera")
    exit()

print("Camera connected!")
print("Press Q to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    cv2.imshow("Brain Registration - Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
