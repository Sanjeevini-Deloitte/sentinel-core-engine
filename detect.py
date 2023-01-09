import configparser
import json
from datetime import datetime
import ssl

import cv2
import torch
import mlfunctions
from sqs import send_queue_message, receive_message

config = configparser.RawConfigParser()
config.read('config.properties')

ssl._create_default_https_context = ssl._create_unverified_context


def detecting(frame, model):
    frame = [frame]
    # print(f"Detecting . . .")
    res = model(frame)
    labels, cords = res.xyxyn[0][:, -1], res.xyxyn[0][:, :-1]
    return labels, cords

def color_box(modelname, violation_class, results, frame, classes, acc=0.45):
    prev_time = 0
    labels, cords = results
    n = len(labels)
    x_window, y_window = frame.shape[1], frame.shape[0]

    for i in range(n):  # processing of detected objects
        cords_list = cords[i]
        if cords_list[4] >= acc:  # Accuracy Comparison
            x1 = int(cords_list[0] * x_window)
            y1 = int(cords_list[1] * y_window)
            x2 = int(cords_list[2] * x_window)
            y2 = int(cords_list[3] * y_window)
            text_d = classes[int(labels[i])]
            if text_d == violation_class:
                color = (255, 0, 0)
            else:
                color = (85, 0, 0)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)  # object box
            cv2.rectangle(frame, (x1, y1 - 20), (x2, y1), color, -1)  # text box
            cv2.putText(frame, text_d + f" {round(float(cords_list[4]), 2)}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (255, 255, 255), 2)  # text adding
            violation=''
            if text_d == violation_class:
                if text_d == "Not Glove Wearing":
                    violation = "GLOVES"
                elif text_d == "Fire":
                    violation = "FIRE"
                elif text_d == "Smoke":
                    violation ="SMOKE"
                elif text_d == "without_mask":
                    violation = "MASK"
                elif text_d == "gun":
                    violation = "WEAPON"
                elif text_d == "eyes_without_goggles":
                    violation = "GOGGLES"
                elif text_d == "no_vest":
                    violation = "VEST"
                elif text_d == "without Helmet":
                    violation = "HELMET"
                
                
                current_time = datetime.now().time().second
                if current_time!=prev_time or prev_time == 0:
                    modelpath = config.get("screenshots", modelname)
                    # print(modelpath)
                    image_link = mlfunctions.voilation_screenshot(frame, modelpath) # Image Link
                    url=mlfunctions.cloudfront_link(modelpath)
                    print(url)
                    sqs_trigger_json = mlfunctions.json_generator(violation, cords_list, url) # JSON Output
                    print(sqs_trigger_json)
                    #if(violation_class == "without Helmet") :
                     #   send_queue_message(sqs_trigger_json, group='withoutHelmet')  # Sending JSON to SQS
                    #elif (violation_class == "Not Glove Wearing"):
                     #   send_queue_message(sqs_trigger_json, group='noGloveWearing')  # Sending JSON to SQS
                    #else :
                     #   send_queue_message(sqs_trigger_json, group=violation_class) # Sending JSON to SQS
                    send_queue_message(sqs_trigger_json,violation)
                    prev_time = current_time

    return frame
