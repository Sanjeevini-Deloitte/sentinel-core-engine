import datetime
import ssl
import threading

import cv2
# from vidgear.gears import CamGear


# from gloves_detection_model import gloves
from goggles_detection_model import goggles_copy
# from helmet_detection_model import helmet
# from vest_detection_model import vest
# from weapon_detection_model import weapon
from mask_detection_model import mask_copy
# from fire_smoke_detection_model import fire_smoke
# from threading import Thread
from datetime import datetime


def ml_detection_input():
    ssl._create_default_https_context = ssl._create_unverified_context
    # live_video = cv2.VideoCapture(0)
    # live_video = CamGear(source='https://www.youtube.com/watch?v=TUgdqzPfYE4', stream_mode=True,
    # logging=True).start()  # YouTube Video URL as input
    # live_video=cv2.VideoCapture("C://Users//Administrator//Downloads//demo.mp4.mov")
    # live_video=cv2.VideoCapture("https://www.youtube.com/watch?v=W32w3Hl5M9Q")
    # live_video=cv2.VideoCapture('C://Users//Administrator//Desktop//ml_models//img.jpg')
    # live_video = cv2.VideoCapture('C://Users//Administrator//Downloads//test.mov')
    live_video = cv2.VideoCapture("rtsp://10.0.3.224:8555/mystream", cv2.CAP_FFMPEG)
    live_video2 = cv2.VideoCapture("rtsp://10.0.3.224:8555/mystream2", cv2.CAP_FFMPEG)
    # live_video3 = cv2.VideoCapture("rtsp://10.0.3.224:8555/mystream3", cv2.CAP_FFMPEG)

    frame_number = 0
    print(datetime.now())

    while live_video.isOpened() and live_video2.isOpened():  # and live_video3.isOpened():
        # while True:
        ret, frame = live_video.read()
        ret2, frame2 = live_video2.read()
        # ret3, frame3 =live_video3.read()

        # ret, frame = live_video.read()
        # ret = True
        # frame = live_video.read()
        # frame = cv2.resize(frame, (720,720))
        frame_number += 1

        if frame is None or frame2 is None:  # or frame3 is None:
            break
        elif frame_number %241 == 1:
            print("frame number", frame_number)
            # print(datetime.now())
            # helmets = threading.Thread(target=helmet.helmet_recognisation(ret, frame))
            # weapons = threading.Thread(target=weapon.weapon_recognisation(ret, frame))
            goggles_thread1 = threading.Thread(target=goggles_copy.googles_recognisation(ret, frame,1))
            goggles_thread2 = threading.Thread(target=goggles_copy.googles_recognisation(ret2, frame2,2))
            # gloves_thread = threading.Thread(target=gloves.gloves_recognisation(ret, frame))
            # vests = threading.Thread(target=vest.vest_recognisation(ret, frame))
            mask_thread1 = threading.Thread(target=mask_copy.mask_recognisation(ret, frame, 1))
            mask_thread2 = threading.Thread(target=mask_copy.mask_recognisation(ret, frame2, 2))
            # mask_thread3 = threading.Thread(target=mask_copy.mask_recognisation(ret, frame3, 3))
            # smoke = threading.Thread(target=fire_smoke.fire_smoke_recognisation(ret, frame))

            # helmets.start()
            # weapons.start()
            goggles_thread1.start()
            goggles_thread2.start()
            # gloves_thread.start()
            # vests.start()
            mask_thread1.start()
            mask_thread2.start()
            # mask_thread3.start()
            # smoke.start()

            # helmets.join()
            # weapons.join()
            goggles_thread1.join()
            goggles_thread2.join()
            # gloves_thread.join()
            # vests.join()
            mask_thread1.join()
            mask_thread2.join()
            # mask_thread3.join()
            # smoke.join()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    print(datetime.now())
    # live_video.stop()


ml_detection_input()
















