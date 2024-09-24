# Raspberry + Aruco + Python

This code sample prints a single JSON array to stdout with the coordinates of several Aruco markers that appear on the field of view of the camera.

Tested with:
- Raspberry Pi 5
- Raspberry Pi Camera HQ
- Raspberry Pi OS "Bookworm" 64 bit

Based on code from:
- [How to Detect ArUco Markers Using OpenCV and Python](https://automaticaddison.com/how-to-detect-aruco-markers-using-opencv-and-python/) by Automatic Addison
- [The Picamera2 Library; A libcamera-based Python library for Rasperry Pi cameras](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf) by Raspberry Pi Foundation

# Install dependencies

First you need a virtual environment. Several ways to do it, I use a user wide environment for this case:

```bash
python -m venv ~/.env
python -m venv --system-site-packages ~/.env
source ~/.env/bin/activate
```

Install dependencies for this program now:

```bash
pip3 install opencv-python
pip3 install picamera2
```
