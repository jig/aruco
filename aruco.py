#!/usr/bin/python3
import time
import cv2
from picamera2 import MappedArray, Picamera2, Preview
import json
import numpy as np

# The different ArUco dictionaries built into the OpenCV library.
# cv2.aruco.DICT_4X4_50,
# cv2.aruco.DICT_4X4_100,
# cv2.aruco.DICT_4X4_250,
# cv2.aruco.DICT_4X4_1000,
# cv2.aruco.DICT_5X5_50,
# cv2.aruco.DICT_5X5_100,
# cv2.aruco.DICT_5X5_250,
# cv2.aruco.DICT_5X5_1000,
# cv2.aruco.DICT_6X6_50,
# cv2.aruco.DICT_6X6_100,
# cv2.aruco.DICT_6X6_250,
# cv2.aruco.DICT_6X6_1000,
# cv2.aruco.DICT_7X7_50,
# cv2.aruco.DICT_7X7_100,
# cv2.aruco.DICT_7X7_250,
# cv2.aruco.DICT_7X7_1000,
# cv2.aruco.DICT_ARUCO_ORIGINAL

this_aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
this_aruco_parameters = cv2.aruco.DetectorParameters_create()

picam2 = Picamera2()
picam2.start_preview(Preview.DRM, x=0, y=0, width=2028, height=1080)
config = picam2.create_preview_configuration(main={"size": (2028, 1080)},
                                             lores={"size": (2028, 1080), "format": "YUV420"})
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
      data = []
      i = 0
      for id in ids.tolist():
        data.append({
          "id": id,
          "corner": corners[i].tolist()
        })
        i = i + 1
      print(json.dumps(data))
