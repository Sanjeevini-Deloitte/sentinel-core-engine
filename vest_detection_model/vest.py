import torch
import cv2

from detect import detecting, color_box

model = torch.hub.load('C://Users//Administrator//Desktop//ml_models//yolov5-master', 'custom',
                       path='C://Users//Administrator//Desktop//ml_models//pt files//vest_weights.pt',
                       source="local")

classes = model.names


def vest_recognisation(ret, frame):
   # accuracy threshold
    acc = 0.45
    # ret is a boolean variable; 'true' if any frame is present in 'frame' variable
    if ret:
        # frame is converted into an image(from BGR to RGB format)
        # and then sent for detection on the frame(RGB format)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # stores the result of the detection(i.e. labels and coordinates)
        res = detecting(frame, model=model)
        # frame is converted back to BGR format
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # bounding boxes are made on the detected object along with the class name
        frame = color_box("vest", "no_vest", res, frame, classes=classes, acc=acc)
        #cv2.imshow('Vest Detection', frame)
        
