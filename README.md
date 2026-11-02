# Brain Registration

Real-time AprilTag-based brain tracking and 3D visualization using Python, OpenCV, Viser, and an Android phone camera.

## What this project does

This project tracks a printed AprilTag using an Android phone camera and updates the position and orientation of a 3D brain model in a browser.

**Pipeline:**

1. An Android phone streams live video over Wi-Fi.
2. OpenCV receives the video stream.
3. The AprilTag detector identifies the marker.
4. OpenCV estimates the marker's 3D pose.
5. Position and rotation are smoothed.
6. Pose data is sent to the 3D viewer over UDP.
7. Viser updates the brain model in real time.

## Requirements

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

**Important:** The computer and phone must be connected to the same Wi-Fi network.

## 1. Clone the repository

Open PowerShell and run:

```powershell
git clone https://github.com/AdarshanandIITBHU/Brain-Registration.git
cd Brain-Registration
```

All following commands should be run from the `Brain-Registration` directory unless specified otherwise.

## 2. Install prerequisites

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\install_windows.ps1
```

This script checks for Python 3.12 and Git and attempts to install missing prerequisites using Windows Package Manager (`winget`).

If Python or Git was just installed, close and reopen PowerShell.

Verify the installations:

```powershell
py -3.12 --version
git --version
```

Python 3.12 is recommended because the AprilTag dependency may fail to build with newer Python versions.

## 3. Create the Python environment

Run:

```powershell
.\scripts\setup_environment.ps1
```

This script:

- Creates a virtual environment named `.venv`.
- Activates the environment.
- Upgrades pip.
- Installs packages from `requirements.txt`.

The dependencies include OpenCV, NumPy, pupil-apriltags, Viser, trimesh, pyglet, and python-dotenv.

If PowerShell cannot run the activation script, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then run the setup script again.

## 4. Configure the Android phone camera

### Install IP Webcam

1. Open Google Play Store on your Android phone.
2. Search for **IP Webcam**.
3. Install and open the application.
4. Open Video preferences.
5. Set resolution to 640 × 480, or the closest available option.
6. Set video quality to approximately 50%.
7. Set FPS to approximately 15.
8. Set zoom to 1×.
9. Return to the main screen.
10. Tap **Start server**.

The application will display an IP address and port.

For example:

```text
http://192.168.1.100:8080
```

The video stream URL is:

```text
http://192.168.1.100:8080/video
```

Use the actual IP address displayed on your phone. The example address above is not your phone's actual address.

### Test the camera connection

On your computer, open a browser and enter:

```text
http://YOUR_PHONE_IP:8080/video
```

Replace `YOUR_PHONE_IP` with the address displayed by IP Webcam.

You should see the live camera stream.

If the stream does not open, check that both devices are connected to the same Wi-Fi network and that IP Webcam is running.

## 5. Configure the project

Create your local environment configuration file:

```powershell
Copy-Item .env.example .env
```

Open it:

```powershell
notepad .env
```

Replace the example URL with your actual phone camera URL:

```env
PHONE_CAMERA_URL=http://YOUR_PHONE_IP:8080/video
```

Save the file and close Notepad.

**Important:**

- Do not include quotation marks around the URL.
- Do not upload `.env` to GitHub.
- Your phone's IP address may change when the camera server restarts. Update `.env` whenever this happens.

## 6. Prepare the AprilTag marker

The project uses:

- Family: `tag36h11`
- Marker ID: `0`
- Outer black-square size: **4 cm × 4 cm**

A sample marker is included:

```text
assets/apriltag_0.png
```

Print the marker with:

- The outer black square measuring exactly 4 cm × 4 cm.
- A clear white margin around the marker.
- No stretching, distortion, or cropping.

Keep the marker flat and visible to the phone camera.

You can generate the marker again using:

```powershell
.\.venv\Scripts\python.exe scripts\generate_tag.py
```

## 7. Run the complete project

Make sure:

- IP Webcam is running on your phone.
- The phone and computer are on the same Wi-Fi network.
- `.env` contains the correct camera URL.
- The printed AprilTag is ready.

From the project root, run:

```powershell
.\scripts\run_project.ps1
```

The launcher automatically:

1. Starts the Viser 3D brain viewer in a separate PowerShell window.
2. Waits three seconds.
3. Starts AprilTag pose tracking.

Open the viewer in your computer's browser:

**http://localhost:8081**

You should see the 3D brain model.

The camera window should also appear. Point the phone camera at the printed AprilTag. When the marker is detected, the tracking window displays its ID and tracking status, and the 3D brain receives the estimated pose.

Press **Q** in the camera tracking window to stop tracking. Close the viewer's PowerShell window to stop the 3D viewer.

## 8. Run the components separately (optional)

If you want to test or debug individual components, open separate PowerShell windows in the project directory.

### Terminal 1: Start the 3D brain viewer

```powershell
.\.venv\Scripts\python.exe src\view_brain.py
```

Open:

```text
http://localhost:8081
```

### Terminal 2: Start AprilTag pose tracking

```powershell
.\.venv\Scripts\python.exe src\pose_estimation.py
```

The tracking program reads the phone camera URL from `.env` and sends pose data to the viewer over UDP port `5005`.

### Other individual tests

Test the phone camera:

```powershell
.\.venv\Scripts\python.exe src\phone_camera.py
```

Test AprilTag detection:

```powershell
.\.venv\Scripts\python.exe src\apriltag_detect.py
```

## 9. Project structure

```text
Brain-Registration/
│
├── assets/
│   ├── brain_tumor_ar.glb
│   └── apriltag_0.png
│
├── src/
│   ├── phone_camera.py
│   ├── apriltag_detect.py
│   ├── pose_estimation.py
│   └── view_brain.py
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
```

## 10. Troubleshooting

### Python 3.12 is not recognized

Check installed Python versions:

```powershell
py -0p
```

Install Python 3.12 if it is missing, then reopen PowerShell.

### Camera feed is unavailable

- Confirm IP Webcam is running.
- Confirm the phone and computer use the same Wi-Fi network.
- Check the IP address displayed by the phone.
- Check the `PHONE_CAMERA_URL` value in `.env`.
- Try opening the video URL in a computer browser.
- Allow Python through Windows Firewall if prompted.

### The Viser viewer does not open

- Confirm that `src/view_brain.py` is running.
- Check whether port `8081` is already being used.
- Try opening `http://localhost:8081` again.

### AprilTag is not detected

- Use the supplied `assets/apriltag_0.png`.
- Confirm that the marker ID is 0 and family is `tag36h11`.
- Ensure the entire marker is visible.
- Use good lighting.
- Keep the marker flat and avoid motion blur.
- Ensure the printed outer black square is 4 cm × 4 cm.

### Brain model does not move

- Confirm that the AprilTag is detected in the camera window.
- Confirm that the Viser viewer is running.
- Make sure the viewer is listening on UDP port `5005`.
- Start the viewer before starting pose tracking.

### Dependencies fail to install

Use Python 3.12 and recreate the environment if necessary:

```powershell
deactivate
Remove-Item -Recurse -Force .venv
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Limitations

The current pose estimation uses approximate camera intrinsic parameters rather than a calibrated camera model. Tracking accuracy and stability depend on camera characteristics, lighting, marker visibility, and coordinate alignment.

This project is a development prototype and is not intended for clinical use or medical decision-making.

## License

See the `LICENSE` file for license terms.