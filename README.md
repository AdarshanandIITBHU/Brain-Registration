
# Brain Registration

Real-time 3D brain visualization and AprilTag-based tracking using Python, OpenCV, Viser, and an Android phone camera.

## Features

- Android phone camera streaming over Wi-Fi
- AprilTag detection using the tag36h11 family
- 3D position and orientation estimation
- UDP communication between tracking and visualization
- Real-time 3D brain model visualization
- Smoothed position and rotation updates
- Interactive Viser controls

## Project Structure

```text
Brain-Registration/
├── assets/
│   ├── brain_tumor_ar.glb
│   └── apriltag_0.png
├── src/
│   ├── phone_camera.py
│   ├── apriltag_detect.py
│   ├── pose_estimation.py
│   └── view_brain.py
├── tools/
│   ├── calibration/
│   ├── testing/
│   └── generate_tag.py
├── scripts/
│   ├── install_windows.ps1
│   ├── setup_environment.ps1
│   └── run_project.ps1
├── docs/
│   └── phone_setup.md
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Requirements

- Windows 10 or Windows 11
- Python 3.12
- Git
- Android phone
- Wi-Fi connection shared by the PC and phone

## 1. Clone the repository

```powershell
git clone https://github.com/AdarshanandIITBHU/Brain-Registration.git
cd Brain-Registration
```

## 2. Install prerequisites

Open PowerShell in the project directory:

```powershell
.\scripts\install_windows.ps1
```

This checks for Python 3.12 and Git and installs missing prerequisites through winget.

## 3. Set up Python

```powershell
.\scripts\setup_environment.ps1
```

This creates `.venv` and installs the required Python packages.

## 4. Configure the Android camera

Install **IP Webcam** on your Android phone.

Follow the instructions in:

`docs/phone_setup.md`

Start the phone's camera server and note the IP address.

Copy `.env.example` to `.env` and configure your phone's video URL.

## 5. Run the project

```powershell
.\scripts\run_project.ps1
```

The Viser viewer will open at:

http://localhost:8081

The phone camera window will display AprilTag tracking.

## 6. Generate an AprilTag

The project uses the `tag36h11` family and marker ID `0`.

A sample marker is provided in:

`assets/apriltag_0.png`

You can generate another marker using:

```powershell
python scripts/generate_tag.py
```

Print the marker with a 4 cm black square and a white margin.

## How it works

1. IP Webcam streams video from the Android phone.
2. OpenCV reads the video stream.
3. The AprilTag detector identifies the printed marker.
4. OpenCV estimates the marker's pose.
5. Position and rotation are smoothed.
6. Pose data is transmitted over UDP on port 5005.
7. Viser updates the 3D brain model.

## Troubleshooting

### Python 3.12 is not recognized

Check the Python launcher:

```powershell
py -0p
```

### Camera feed is unavailable

Check the phone IP address, Wi-Fi connection, and IP Webcam server.

### Viser page does not open

Check that port 8081 is available and that `view_brain.py` is running.

### AprilTag is not detected

- Check that the printed marker is not distorted.
- Use good lighting.
- Keep the entire marker visible.
- Confirm that the marker ID is 0.

### UDP tracking does not work

Make sure the viewer is running and listening on port 5005.

## Limitations

The current camera intrinsics are approximate. Pose accuracy and registration stability depend on camera calibration, marker detection, and coordinate alignment.

This project is a development prototype and is not intended for clinical use.

## License

See the repository's license file for the applicable terms.
