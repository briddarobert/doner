""" OpenCV, for image processing """
import cv2
""" numpy for maths stuff """
import numpy as np
from cv2_enumerate_cameras import enumerate_cameras

for camera_info in enumerate_cameras():
    print(f'{camera_info.index}: {camera_info.name}')

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

ON_TRACK_BUFFER = 200

# Setup the camera
video_capture = cv2.VideoCapture(204)
video_capture.set(3, FRAME_WIDTH)
video_capture.set(4, FRAME_HEIGHT)

while True:
    # Capture a frame
    ret, frame = video_capture.read()
    # Crop the image
    # [startY:endY, startX:endX]
    crop_img = frame[0:FRAME_HEIGHT, 0+100:FRAME_WIDTH-100]
    # Convert to grayscale
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Color thresholding
    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
    # Find the contours of the frame
    contours, hierarchy = cv2.findContours(
        thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
    # Find the biggest contour (if detected)
    # Draw turning area
    cv2.line(crop_img, ((FRAME_WIDTH-100)//2 - ON_TRACK_BUFFER, 0), ((FRAME_WIDTH-100)//2 - ON_TRACK_BUFFER, FRAME_HEIGHT), (0, 0, 255), 1)
    cv2.line(crop_img, ((FRAME_WIDTH-100)//2 + ON_TRACK_BUFFER, 0), ((FRAME_WIDTH-100)//2 + ON_TRACK_BUFFER, FRAME_HEIGHT), (0, 0, 255), 1)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        rows,cols = crop_img.shape[:2]
        [vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)
        lefty = int((-x*vy/vx) + y)
        righty = int(((cols-x)*vy/vx)+y)
        cv2.line(crop_img,(cols-1,righty),(0,lefty),(0,255,0),2)
        if (lefty > 0 and righty > 0):
            if (lefty > righty):
                print("Left turn ahead")
            elif (righty > lefty):
                print("Left turn ahead")
            else:
                print("Wut?! (forse incrocio)")
        print(lefty, righty)
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print(str(cx) + " " + str(cy))
        cv2.line(crop_img, (cx, 0), (cx, FRAME_HEIGHT), (255, 0, 0), 1)
        cv2.line(crop_img, (0, cy), (FRAME_WIDTH, cy), (255, 0, 0), 1)
        cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)
        if cx >= (FRAME_WIDTH-100)/2 + ON_TRACK_BUFFER:
            print("Turn right! Adjustment")
        if cx < (FRAME_WIDTH-100)/2 + ON_TRACK_BUFFER and cx > (FRAME_WIDTH-100)/2 - ON_TRACK_BUFFER:
            print("On track!")
        if cx <= (FRAME_WIDTH-100)/2 - ON_TRACK_BUFFER:
            print("Turn left! Adjustment")
    else:
        print("No line found")

    # Display the resulting frame
    cv2.imshow('frame', crop_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
