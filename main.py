""" OpenCV, for image processing """
import cv2

ON_TRACK_BUFFER = 200

# Setup the camera
video_capture = cv2.VideoCapture(0)
video_capture.set(3, 1280)
video_capture.set(4, 720)

width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

while True:
    # Capture a frame
    ret, frame = video_capture.read()
    # Crop the image
    # [startY:endY, startX:endX]
    crop_img = frame[0:720, 0+100:1280-100]
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
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print(str(cx) + " " + str(cy))
        cv2.line(crop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(crop_img, (0, cy), (1280, cy), (255, 0, 0), 1)
        cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)
        if cx >= (1280-100)/2 + ON_TRACK_BUFFER:
            print("Turn Left!")
        if cx < (1280-100)/2 + ON_TRACK_BUFFER and cx > (1280-100)/2 - ON_TRACK_BUFFER:
            print("On Track!")
        if cx <= (1280-100)/2 - ON_TRACK_BUFFER:
            print("Turn Right")
    else:
        print("I don't see the line")

    # Display the resulting frame
    cv2.imshow('frame', crop_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
