import configparser
import datetime
import time
from datetime import datetime
import os
import cv2
import json
import torch

from storage_bucket import upload_screenshots

timestr = time.strftime("%H%M%S")
config = configparser.RawConfigParser()
config.read('config.properties')

json_output = {}


def json_generator(text_d, cords_list,image_link,cam_no):
    json_output.update({"cameraId": cam_no})
    json_output.update({"confidenceLevel": f"{round(float(cords_list[4])*100, 2)}"})
    json_output.update({"intensityLevel": 93})
    json_output.update({'imageLink': image_link})
    json_output.update({"violationTime": time.strftime("%Y-%m-%d %H:%M:%S")})
    json_output.update({"violationType": text_d})
    myjson = json.dumps(json_output)
    return myjson


def voilation_screenshot(frame, model_path):

    screenshot_path = config.get('screenshots', 'path')
    screenshot_link = screenshot_path+model_path + "/frame_%s" % time.strftime("%H%M%S") + ".png"
    cv2.imwrite(screenshot_path+model_path + "/frame_%s" % time.strftime("%H%M%S") + ".png", frame)
    image_link = upload_screenshots(model_path+time.strftime("%H%M%S"), screenshot_link) # Upload screenshot to S3 Bucket
    os.remove(screenshot_link)
    return image_link


def load_models(model_name):
    model = torch.hub.load('C://Users//Administrator//Desktop//ml_models//yolov5-master', 'custom',
                           path=model_name,
                           force_reload=True)
    classes = model.names
    return model, classes
