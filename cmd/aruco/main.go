package main

import (
	"fmt"
	"math"

	"gocv.io/x/gocv"
)

func main() {
	// set to use a video capture device 0
	deviceID := 1

	// open webcam
	webcam, err := gocv.OpenVideoCapture(deviceID)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer webcam.Close()

	// open display window
	window := gocv.NewWindow("Face Detect")
	defer window.Close()

	// prepare image matrix
	img := gocv.NewMat()
	defer img.Close()

	fmt.Printf("start reading camera device: %v\n", deviceID)
	for {
		if ok := webcam.Read(&img); !ok {
			fmt.Printf("cannot read device %v\n", deviceID)
			return
		}
		if img.Empty() {
			continue
		}

		dict := gocv.GetPredefinedDictionary(gocv.ArucoDict6x6_50)
		params := gocv.NewArucoDetectorParameters()
		detector := gocv.NewArucoDetectorWithParams(dict, params)
		defer detector.Close()

		borderColor := gocv.NewScalar(255, 0, 255, 0)
		markerCorners, markerIds, _ := detector.DetectMarkers(img)
		for i, marker := range markerIds {
			if marker == 0 {
				// height, width, _, _, _ := measure(markerCorners[i])
				// fmt.Printf("marker=%d x=%f y=%f height=%f width=%f\n", marker, x, y, height, witdh)
				// fmt.Printf("marker=%d height=%f width=%f\n", marker, height, width)
				dist, angle := targetPose(markerCorners[i])
				fmt.Printf("distance=%.1f cm, angle=%.0f°\n", dist/10, angle)
				gocv.ArucoDrawDetectedMarkers(img, markerCorners, markerIds, borderColor)
			}
		}

		// show the image in the window, and wait 1 millisecond
		window.IMShow(img)
		window.WaitKey(1)
	}
}

func measure(marker []gocv.Point2f) (float64, float64, float64, float64, bool) {
	height1 := (marker[3].Y - marker[0].Y)
	height2 := (marker[2].Y - marker[1].Y)
	width1 := (marker[1].X - marker[0].X)
	width2 := (marker[2].X - marker[3].X)
	x := float64(marker[0].X+marker[1].X+marker[2].X+marker[3].X) / 4
	y := float64(marker[0].Y+marker[1].Y+marker[2].Y+marker[3].Y) / 4
	return float64(height1+height2) / 2, float64(width1+width2) / 2, x, y, height1 > height2
}

func targetPose(marker []gocv.Point2f) (dist, angle float64) {
	height, width, _, _, side := measure(marker)
	dist = 22500 / height
	if width > height {
		angle = 0
	} else {
		angle = math.Acos(width/height) / 2 / 3.1415926535 * 360
		if side {
			angle = -angle
		}
	}
	return
}
