import cv2
import numpy as np
import os
#C:\Users\Administrator\Desktop\ml_models\venv\Lib\site-packages\cv2

print(os.environ.get("OPENCV_FFMPEG_CAPTURE_OPTIONS"))
#os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = 'protocol_whitelist;file,udp,rtp'
# Create a VideoCapture object and read from input file
#cap = cv2.VideoCapture("C:\\Users\\Administrator\\Desktop\\ml_models\\foo.sdp",cv2.CAP_FFMPEG)
cap=cv2.VideoCapture("rtsp://10.0.3.224:8555/mystream",cv2.CAP_FFMPEG)
cap2=cv2.VideoCapture("rtsp://10.0.3.224:8555/mystream2",cv2.CAP_FFMPEG)
#cap3=cv2.VideoCapture("rtsp://10.0.3.224:8555/mystream3",cv2.CAP_FFMPEG)
print(cap.isOpened())

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video file")
if (cap2.isOpened() == False):
    print("Error opening video file2")
#if (cap3.isOpened() == False):
   # print("Error opening video file3")
# Read until video is completed
while (cap.isOpened() and cap2.isOpened() and cap3.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
    ret2,framee=cap2.read()
    #ret3, frame3 = cap3.read()
    print(ret)
    if ret == True and ret2 == True:
        cv2.imshow('Frame', framee)
        cv2.imshow('Frame2', frame)
        #cv2.imshow('Frame3', frame3)


        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release
# the video capture object
cap.release()
cap2.release()
#cap3.release()



# Closes all the frames
cv2.destroyAllWindows()
