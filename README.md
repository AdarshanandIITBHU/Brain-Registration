# Brain Registration & Augmented Reality

A prototype for visualizing an MRI-derived 3D brain and tumor model and tracking it using an Android phone camera and AprilTag.

The long-term objective is to develop an augmented reality system that displays a patient's MRI-derived brain and tumor in the correct anatomical position relative to their head.

> **Project status:** AR tracking and 3D visualization prototype. Patient-to-MRI anatomical registration and clinical accuracy validation are not yet implemented.

---

## 1. Current Features

- Loads a 3D brain and tumor model from a GLB file.
- Uses an Android phone camera as a live video source through IP Webcam.
- Detects AprilTag markers using the `tag36h11` family.
- Estimates marker position and orientation using OpenCV PnP.
- Sends pose information over UDP.
- Displays and moves the 3D model in a Viser viewer.
- Includes manual position controls.
- Includes a rigid registration implementation using the Kabsch algorithm.
- Includes a registration script that accepts corresponding landmark coordinates and exports a transformed GLB.

## 2. Project Structure

```text
Brain-Registration/
│
├── assets/
│   ├── brain_tumor_ar.glb
│   ├── apriltag_0.png
│   ├── landmarks.csv
│   ├── brain_tumor_registered.glb
│   └── mri_to_head_transform.npz
│
├── src/
│   ├── phone_camera.py
│   ├── apriltag_detect.py
│   ├── pose_estimation.py
│   ├── view_brain.py
│   ├── registration.py
│   └── register_glb.py
│
├── tools/
│   ├── calibration/
│   │   ├── calibrate_camera.py
│   │   └── capture_calibration.py
│   └── testing/
│       └── camera_test.py
│
├── scripts/
│   ├── install_windows.ps1
│   ├── setup_environment.ps1
│   ├── run_project.ps1
│   └── generate_tag.py
│
├── docs/
│   └── phone_setup.md
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
