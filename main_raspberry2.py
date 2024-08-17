#!/usr/bin/python3
import time

import cv2

from picamera2 import MappedArray, Picamera2, Preview

# This version creates a lores YUV stream, extracts the Y channel and runs the face
# detector directly on that. We use the supplied OpenGL accelerated preview window
# and delegate the face box drawing to its callback function, thereby running the
# preview at the full rate with face updates as and when they are ready.

desired_aruco_dictionary = "DICT_6X6_1000"

# The different ArUco dictionaries built into the OpenCV library.
ARUCO_DICT = {
  "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
  "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
  "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
  "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
  "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
  "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
  "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
  "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
  "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
  "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
  "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
  "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
  "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
  "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
  "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
  "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
  "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}

this_aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])
this_aruco_parameters = cv2.aruco.DetectorParameters_create()

picam2 = Picamera2()
picam2.start_preview(Preview.DRM, x=0, y=0, width=1920, height=1080)
config = picam2.create_preview_configuration(main={"size": (1920, 1080)},
                                             lores={"size": (1920, 1080), "format": "YUV420"})
picam2.configure(config)

(w0, h0) = picam2.stream_configuration("main")["size"]
(w1, h1) = picam2.stream_configuration("lores")["size"]
s1 = picam2.stream_configuration("lores")["stride"]

picam2.start()

c = 0
while True:
    buffer = picam2.capture_buffer("lores")
    grey = buffer[:s1 * h1].reshape((h1, s1))
    c=c+1
    (corners, ids, rejected) = cv2.aruco.detectMarkers(grey, this_aruco_dictionary, parameters=this_aruco_parameters)
    if len(corners) > 0:
      ids = ids.flatten()
      print(c, ids, corners)