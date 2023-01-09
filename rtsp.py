import cv2
import numpy as np
import os
#C:\Users\Administrator\Desktop\ml_models\venv\Lib\site-packages\cv2

print(os.environ.get("OPENCV_FFMPEG_CAPTURE_OPTIONS"))
#os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = 'protocol_whitelist;file,udp,rtp'
# Create a VideoCapture object and read from input file
#cap = cv2.VideoCapture("C:\\Users\\Administrator\\Desktop\\ml_models\\foo.sdp",cv2.CAP_FFMPEG)
cap=cv2.VideoCapture("rtsp://10.0.3.224:8555/mystream2",cv2.CAP_FFMPEG)
print(os.environ.get("OPENCV_FFMPEG_CAPTURE_OPTIONS"))
print(cap.isOpened())

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video file")


# Read until video is completed
while (cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
    print(ret)
    if ret == True:
        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
