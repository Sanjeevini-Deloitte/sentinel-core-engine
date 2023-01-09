import datetime
import ssl
import threading

import cv2
# from vidgear.gears import CamGear


from gloves_detection_model import gloves
from goggles_detection_model import goggles
from helmet_detection_model import helmet
from numpy import double
from vest_detection_model import vest
from weapon_detection_model import weapon
from mask_detection_model import mask
from fire_smoke_detection_model import fire_smoke
from threading import Thread
from datetime import datetime


def ml_detection_input():
    ssl._create_default_https_context = ssl._create_unverified_context
    # live_video = cv2.VideoCapture(0)
    # live_video = CamGear(source='https://www.youtube.com/watch?v=TUgdqzPfYE4', stream_mode=True,
    # logging=True).start()  # YouTube Video URL as input
    # live_video=cv2.VideoCapture("C://Users//Administrator//Downloads//demo.mp4.mov")
    # live_video=cv2.VideoCapture("https://www.youtube.com/watch?v=W32w3Hl5M9Q")
    # live_video=cv2.VideoCapture('C://Users//Administrator//Desktop//ml_models//img.jpg')
    live_video = cv2.VideoCapture('C://Users//Administrator//Downloads//test.mov')
    #live_video = cv2.VideoCapture("rtsp://localhost:8555/mystream", cv2.CAP_FFMPEG)
    live_video.set(cv2.CAP_PROP_FPS, 30)
    frame_number = 0
    print(datetime.now())
    #fps = live_video.get(cv2.CAP_PROP_FPS)
    fps=30
    print(f"{fps} frames per second")
    time_lapse=60
    delay=fps*time_lapse
    print(delay)

    while live_video.isOpened():
        # while True:
        ret, frame = live_video.read()

        # ret, frame = live_video.read()
        # ret = True
        # frame = live_video.read()
        # frame = cv2.resize(frame, (720,720))
        frame_number += 1

        if frame is None:
            break
        elif frame_number % 300 == 1:
            print("frame number", frame_number)
            print(datetime.now())
            helmets = threading.Thread(target=helmet.helmet_recognisation(ret, frame))
            weapons = threading.Thread(target=weapon.weapon_recognisation(ret, frame))
            goggles_thread = threading.Thread(target=goggles.googles_recognisation(ret, frame))
            gloves_thread = threading.Thread(target=gloves.gloves_recognisation(ret, frame))
            vests = threading.Thread(target=vest.vest_recognisation(ret, frame))
            mask_thread = threading.Thread(target=mask.mask_recognisation(ret, frame))
            smoke = threading.Thread(target=fire_smoke.fire_smoke_recognisation(ret, frame))

            helmets.start()
            weapons.start()
            goggles_thread.start()
            gloves_thread.start()
            vests.start()
            mask_thread.start()
            smoke.start()

            helmets.join()
            weapons.join()
            goggles_thread.join()
            gloves_thread.join()
            vests.join()
            mask_thread.join()
            smoke.join()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    print(datetime.now())
    # live_video.stop()


ml_detection_input()
















