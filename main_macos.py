#PiCam
import cv2
import numpy as np
import time
from scipy.spatial.transform import Rotation as R


ARUCO_DICT = {
    "DICT_4X4_50" : cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100" : cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250" : cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000" : cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50" : cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100" : cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250" : cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000" : cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50" : cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100" : cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250" : cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000" : cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50" : cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100" : cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250" : cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000" : cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL" : cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5" : cv2.aruco.DICT_APRILTAG_16H5,
    "DICT_APRILTAG_25h9" : cv2.aruco.DICT_APRILTAG_25H9,
    "DICT_APRILTAG_36h10" : cv2.aruco.DICT_APRILTAG_36H10,
    "DICT_APRILTAG_36h11" : cv2.aruco.DICT_APRILTAG_36H11,
}

def aruco_display(corners, ids, rejected, image):
        if len(corners) > 0:
            ids = ids.flatten()

            for (markerCorner, markerID) in zip(corners, ids):

                    corners = markerCorner.reshape((4,2))
                    (topLeft, topRight, bottomRight, bottomLeft) = corners

                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))

                    cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
                    cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
                    cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
                    cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

                    cX = int((topLeft[0] + bottomRight[0])/ 2.0)
                    cY = int((topLeft[1] + bottomRight[1])/ 2.0)
                    cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)

                    cv2.putText(image, str(markerID),(topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    print("[Inference] Aruco marker ID: {}".format(markerID))
        return image

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters()

try:
  cap = cv2.VideoCapture(0)

  while True:
  # Convert the raw buffer data to an image
      ret, frame = cap.read()
      if not ret:
        break
      gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
      detected_markers = aruco_display(corners, ids, rejected, frame)
      print(ids)
      cv2.imshow("frame", frame)
      key = cv2.waitKey(1) & 0xFF

      if key == ord("q"):
          break

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    cv2.destroyAllWindows()
