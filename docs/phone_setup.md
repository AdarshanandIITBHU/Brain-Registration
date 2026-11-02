
# Android Phone Camera Setup

This project uses an Android phone as a wireless camera through the
IP Webcam application.

## Requirements

- Android phone
- Windows PC
- Both devices connected to the same Wi-Fi network
- IP Webcam application

## Installation

1. Open Google Play Store on your Android phone.
2. Search for **IP Webcam**.
3. Install the application.
4. Open IP Webcam.
5. Open Video preferences.
6. Set the resolution to 640x480 (or the closest available option).
7. Set video quality to approximately 50%.
8. Set FPS to approximately 15.
9. Set zoom to 1x.
10. Return to the main screen and tap Start server.

## Connect the PC

The application displays a local IP address and port.

For example:

http://192.168.1.100:8080

The video stream endpoint is:

http://192.168.1.100:8080/video

Use the actual address displayed by your phone, not the example above.

## Network requirements

- The phone and PC must be on the same local network.
- Allow Python through Windows Firewall if prompted.
- Do not expose the IP Webcam server to the public internet.

## Troubleshooting

### Camera feed does not open

- Check that the phone's server is running.
- Check that both devices are on the same Wi-Fi network.
- Verify the IP address and port.
- Try opening the video URL in a browser on the PC.

### Camera feed is laggy

Try:
- 640x480 resolution
- 50% video quality
- 15 FPS
- 1x zoom

The project uses a threaded camera reader to reduce frame buffering.
