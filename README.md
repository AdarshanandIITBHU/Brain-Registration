# Brain Registration

Real-time AprilTag-based tracking and 3D brain visualization using Python, OpenCV, Viser, and an Android phone camera.

This project is a prototype for developing an augmented reality system that can display a 3D brain and tumor model in alignment with a physical head model.

## 1. Project Overview

The current implementation tracks an AprilTag marker using an Android phone camera and updates a 3D brain model in a browser.

### Current pipeline

1. An Android phone streams live video over Wi-Fi using IP Webcam.
2. OpenCV receives the camera stream.
3. The AprilTag detector identifies the printed marker.
4. OpenCV estimates the marker's 3D position and orientation using `solvePnP`.
5. The estimated pose is converted into position and quaternion rotation.
6. Position and rotation are smoothed to reduce jitter.
7. Pose data is transmitted over UDP.
8. Viser receives the pose and updates the 3D brain model.

### Long-term objective

The intended system will combine:

- MRI-derived brain and tumor reconstruction.
- Registration of MRI coordinates to a physical head model.
- AprilTag-based tracking of the physical head.
- Real-time transformation of the brain model into the camera coordinate system.
- Augmented reality visualization.

The current implementation is an early stage of this pipeline. Full anatomical registration has not yet been completed.

## 2. Current Implementation Status

| Component | Status |
|---|---|
| Android phone camera streaming | Working |
| OpenCV camera input | Working |
| AprilTag detection (`tag36h11`, ID 0) | Working |
| Marker pose estimation using `solvePnP` | Working |
| Position and quaternion conversion | Implemented |
| Pose smoothing | Implemented |
| UDP pose transmission | Working |
| Viser 3D brain viewer | Working |
| Real-time marker-driven model updates | Implemented |
| Rigid registration using Kabsch algorithm | Implemented and synthetically tested |
| GLB registration script | Implemented, awaiting real landmarks |
| MRI-to-physical-head registration | Not completed |
| Anatomically accurate brain placement | Not completed |
| Full AR alignment and validation | Future work |

## 3. Requirements

### Computer

- Windows 10 or Windows 11
- Python 3.12
- Git
- PowerShell
- Wi-Fi connection

### Phone and marker

- Android phone
- IP Webcam Android application
- Printed AprilTag marker

The computer and phone must be connected to the same Wi-Fi network.

## 4. Clone the Repository

```powershell
git clone https://github.com/AdarshanandIITBHU/Brain-Registration.git
cd Brain-Registration
```

Run the following commands from the project directory unless specified otherwise.

## 5. Install Prerequisites

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\install_windows.ps1
```

Verify the installations:

```powershell
py -3.12 --version
git --version
```

Python 3.12 is recommended because some AprilTag dependencies may have compatibility issues with newer Python versions.

## 6. Set Up the Python Environment

```powershell
.\scripts\setup_environment.ps1
```

This script creates a virtual environment named `.venv`, activates it, upgrades pip, and installs the dependencies in `requirements.txt`.

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then run the setup script again.

## 7. Configure the Android Phone Camera

### Install IP Webcam

1. Install IP Webcam from the Google Play Store.
2. Open the application.
3. Set the resolution to 640 × 480, or the closest available option.
4. Set FPS to approximately 15.
5. Set zoom to 1×.
6. Return to the main screen.
7. Tap **Start server**.

The application displays an IP address and port.

For example:

```text
http://192.168.1.100:8080
```

The video stream URL is:

```text
http://192.168.1.100:8080/video
```

Use the actual IP address displayed by your phone.

### Test the camera

Open the video URL in a browser on your computer.

If the stream does not open, check that both devices are connected to the same Wi-Fi network and that IP Webcam is running.

## 8. Configure the Project

Create the local environment file:

```powershell
Copy-Item .env.example .env
```

Open it:

```powershell
notepad .env
```

Set the camera URL:

```env
PHONE_CAMERA_URL=http://YOUR_PHONE_IP:8080/video
```

Save the file.

Important:
- Do not include quotation marks around the URL.
- Do not upload `.env` to GitHub.
- Update the IP address whenever your phone's address changes.

## 9. Prepare the AprilTag

The project uses:

- Family: `tag36h11`
- Marker ID: `0`
- Outer black-square size: 4 cm × 4 cm

A sample marker is included at:

```text
assets/apriltag_0.png
```

Print it without stretching or cropping. The outer black square must measure exactly 4 cm × 4 cm.

To generate the marker again:

```powershell
.\.venv\Scripts\python.exe scripts\generate_tag.py
```

The pose estimator currently uses an approximate camera intrinsic matrix for a 640 × 480 image:

- `fx = 0.9 × image width`
- `fy = 0.9 × image width`
- `cx = image width / 2`
- `cy = image height / 2`

The marker size is configured as 0.04 metres.

These camera parameters are provisional and should be replaced with calibrated values.

## 10. Run the Complete Project

Make sure IP Webcam is running and `.env` contains the correct camera URL.

Run:

```powershell
.\scripts\run_project.ps1
```

The launcher starts the Viser brain viewer in a separate PowerShell window and then starts pose tracking.

Open the viewer:

```text
http://localhost:8081
```

Point the phone camera at the printed AprilTag.

When the marker is detected, the tracking program estimates its pose and sends it to the viewer through UDP port `5005`.

Press **Q** in the camera tracking window to stop tracking.

Close the viewer's PowerShell window to stop the viewer.

**Important:** The current viewer applies the detected marker pose directly to the brain model. This demonstrates live tracking, but does not yet place the brain at its anatomically correct location inside the physical head.

## 11. Run Individual Components

Open separate PowerShell windows from the project directory.

### Terminal 1: Brain viewer

```powershell
.\.venv\Scripts\python.exe src\view_brain.py
```

### Terminal 2: Pose estimation

```powershell
.\.venv\Scripts\python.exe src\pose_estimation.py
```

### Other tests

Phone camera:

```powershell
.\.venv\Scripts\python.exe src\phone_camera.py
```

AprilTag detection:

```powershell
.\.venv\Scripts\python.exe src\apriltag_detect.py
```

## 12. Registration Pipeline

A major part of the project is determining the correct spatial relationship between the MRI-derived brain model and the physical head.

This is necessary because tracking an AprilTag alone only provides the marker's pose relative to the camera. It does not tell the system where the brain is inside the head.

### Coordinate frames

The intended system uses four coordinate frames:

1. **MRI frame:** Coordinates of the reconstructed brain and tumor.
2. **Patient/head frame:** Coordinates defined by anatomical landmarks on the physical head model.
3. **Marker frame:** Coordinates defined by the AprilTag attached to a rigid head support.
4. **Camera frame:** Coordinates of the phone camera.

The intended transformation chain is:

```text
MRI
 |
 | MRI-to-head registration
 v
Physical head
 |
 | Head-to-marker calibration
 v
AprilTag
 |
 | AprilTag pose estimation
 v
Camera
```

Mathematically:

```text
T_camera_from_MRI =
    T_camera_from_marker
    × T_marker_from_head
    × T_head_from_MRI
```

### Rigid registration

The project includes:

```text
src/registration.py
```

This module implements rigid point-cloud registration using the Kabsch algorithm.

It provides functions for:

- Estimating a rotation matrix and translation vector from corresponding points.
- Transforming 3D points.
- Calculating registration RMS error.
- Saving and loading transformation parameters.

The mathematical implementation was tested using synthetic landmarks with a known rotation and translation. The test produced an RMS error close to zero.

This verifies the implementation on synthetic data, not anatomical registration accuracy.

### GLB registration

The project also includes:

```text
src/register_glb.py
```

This script is intended to:

1. Read corresponding MRI and physical-head landmarks.
2. Estimate the rigid transformation.
3. Apply the transformation to the complete GLB scene.
4. Preserve the relative positions of the brain and tumor.
5. Save the registered model and transformation parameters.

The expected input file is:

```text
assets/landmarks.csv
```

Its required columns are:

```csv
mri_x,mri_y,mri_z,head_x,head_y,head_z
```

At least three non-collinear corresponding landmarks are required.

Run the registration script with:

```powershell
.\.venv\Scripts\python.exe src\register_glb.py
```

Expected outputs after successful registration:

```text
assets/brain_tumor_registered.glb
assets/mri_to_head_transform.npz
```

**Current limitation:** The landmarks file currently contains only its header. Real corresponding anatomical landmarks have not yet been collected, so the registration script cannot produce a valid patient-specific transformation.

### Brain and tumor model

The existing model is:

```text
assets/brain_tumor_ar.glb
```

It contains two separate mesh components:

- `translucent_brain`
- `predicted_tumor_WT`

Both are part of the same GLB scene. Registration must apply the same rigid transformation to the entire scene to preserve the tumor's position relative to the brain.

The current model does not include an external head surface or MRI volume in the project assets.

The viewer is configured to prefer `brain_tumor_registered.glb` when available and otherwise use the original brain model.

## 13. Project Structure

```text
Brain-Registration/
│
├── assets/
│   ├── brain_tumor_ar.glb
│   ├── brain_tumor_registered.glb       # Generated after registration
│   ├── mri_to_head_transform.npz        # Generated after registration
│   ├── landmarks.csv
│   └── apriltag_0.png
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
├── README.md
└── LICENSE
```

Generated registration files will appear only after successful registration. They should not be treated as existing source assets.

## 14. Future Work and Development Roadmap

The following work is required to move from the current tracking prototype to a properly registered AR system.

### Phase 1: Camera calibration

- Capture images of a checkerboard calibration pattern.
- Estimate the camera intrinsic matrix and distortion coefficients.
- Replace the approximate camera parameters in pose estimation.
- Validate pose accuracy at different distances and viewing angles.
- Improve pose stability and filtering.

### Phase 2: MRI and physical-head data

- Obtain the original MRI volume or a suitable MRI-derived head surface.
- Establish the coordinate system and physical scale of the MRI-derived model.
- Identify corresponding anatomical landmarks in the MRI and on the physical head model.
- Ensure that landmark coordinates are expressed in consistent units and coordinate conventions.
- Collect enough well-distributed landmarks for reliable registration.

### Phase 3: MRI-to-head registration

- Populate `assets/landmarks.csv` with real corresponding points.
- Run the Kabsch registration implementation.
- Inspect the registered brain model against the physical head.
- Calculate registration error.
- Validate the result using additional landmarks that were not used to calculate the transformation.
- Investigate whether rigid registration is sufficient or whether a more advanced registration method is needed.

### Phase 4: Marker-to-head calibration

- Attach the AprilTag to a rigid support fixed to the physical head model.
- Measure or calibrate the spatial relationship between the marker and the head coordinate frame.
- Implement the marker-to-head transformation.
- Ensure the marker cannot move relative to the head during tracking.

### Phase 5: Complete transformation pipeline

- Combine camera-to-marker pose estimation with marker-to-head and head-to-MRI transformations.
- Apply the complete transformation to the brain and tumor model.
- Ensure correct rotation conventions, coordinate handedness, units, and transformation order.
- Test the model at different head orientations and camera positions.

### Phase 6: AR visualization

- Improve the visualization so that the brain appears in the correct anatomical location.
- Add alignment controls and calibration procedures.
- Improve transparency, tumor visibility, and rendering quality.
- Explore phone-based AR rendering rather than relying only on a browser-based 3D viewer.
- Investigate camera calibration and rendering alignment for a more convincing AR experience.

### Phase 7: Validation and reliability

- Measure target registration error (TRE) using independent landmarks.
- Evaluate tracking stability under different lighting and viewing conditions.
- Measure latency and frame rate.
- Test repeatability after removing and repositioning the physical head model.
- Document limitations and experimental accuracy.

**Important:** The system must be validated using independent measurements before any claims about anatomical accuracy can be made. It is currently a research and development prototype, not a clinical tool.

## 15. Troubleshooting

### Camera feed unavailable

- Confirm IP Webcam is running.
- Check that both devices are on the same Wi-Fi network.
- Verify the phone IP address.
- Check `PHONE_CAMERA_URL` in `.env`.
- Test the stream in a computer browser.
- Allow Python through Windows Firewall if prompted.

### Viser viewer does not open

- Confirm `src/view_brain.py` is running.
- Check whether port `8081` is already in use.
- Try opening `http://localhost:8081` again.

### AprilTag is not detected

- Confirm the marker family is `tag36h11`.
- Confirm the marker ID is `0`.
- Ensure the entire marker is visible.
- Use adequate lighting.
- Avoid motion blur.
- Verify the printed black square measures 4 cm × 4 cm.

### Brain model does not move

- Confirm AprilTag detection is working.
- Confirm the Viser viewer is running.
- Check that UDP port `5005` is available.
- Start the viewer before starting pose tracking.

### Registration script reports insufficient landmarks

The registration script requires at least three non-collinear corresponding landmarks.

Check that `assets/landmarks.csv` contains valid numeric coordinates for both MRI and head landmarks.

A blank template cannot produce a transformation.

### Dependencies fail to install

Recreate the environment using Python 3.12:

```powershell
deactivate
Remove-Item -Recurse -Force .venv
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 16. Limitations

- Camera intrinsics are currently approximated rather than calibrated.
- Pose estimation accuracy depends on camera characteristics, marker size, lighting, and marker visibility.
- The brain model currently follows the AprilTag pose directly.
- Real MRI-to-head registration has not yet been performed.
- Marker-to-head calibration has not yet been implemented.
- The project does not yet demonstrate anatomically accurate brain placement inside a physical head.
- Clinical accuracy and safety have not been established.

## 17. License

See the `LICENSE` file for license terms.
