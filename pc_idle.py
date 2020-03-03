import os
import time
from requests import get, post

import cv2

import win32api

import yaml

# import sys
# print("%x" % sys.maxsize, sys.maxsize > 2**32)

rp = realpath = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(rp, "config.yaml"), "r") as f:
    config = yaml.load(f)


def getIdleTime():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0


def trigger(action):
    print(action)

    headers = {
        'Authorization': 'Bearer {}'.format(config['token']),
        'content-type': 'application/json',
    }

    for entity_id in config['home_assistant_booleans']:
        url = "{}/services/input_boolean/{}".format(config['endpoint_url'], action)
        data = {"entity_id": "input_boolean.{}".format(entity_id)}
        # print ("    ", action, url, data)
        response = post(url, headers=headers, json=data)
        # print("    ", response.text)


use_camera = config['use_camera']
camera_id = config['camera_id']

idle = False


def do_sleep():
    time.sleep(config['interval'])

def detect_faces(camera_id, cascades):
    cam = cv2.VideoCapture(camera_id)
    # Check if the webcam is opened correctly
    if not cam.isOpened():
        print("Cannot open webcam, check ID, or maybe camera is used by another app.")
        do_sleep()
        return False
    ret, frame = cam.read()
    cam.release()
    face_detected = False
    for cascade in cascades:
        faceCascade = cv2.CascadeClassifier(os.path.join(rp, cascade))
        # print("Getting camera image...")
        if not ret:
            print("Cannot get image from camera, possibly wrong ID?")
            do_sleep()
            break
        # print(ret, frame)
        # cv2.imshow("test", frame)
        # cv2.waitKey(10)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if len(faces) > 0:
            print("Faces detected with {}: {}".format(cascade, len(faces)))
            do_sleep()
            return True
    return False

cascades = config['cascades']
offset = 0

face_detected = False
while True:
    idle_for = getIdleTime()
    if idle_for-offset < 0:
        offset = 0
    # print(idle_for-offset, idle_for, offset)
    if idle_for - offset > config['idle_if_seconds']:
        if not idle:
            if use_camera:
                face_detected = detect_faces(camera_id, cascades)
                if not face_detected:
                    time.sleep(5)
                face_detected = detect_faces(camera_id, cascades)
                if face_detected:
                    offset = getIdleTime()
                    continue

                if not face_detected:
                    print("No faces.")
                    trigger('turn_on')
                    idle = True
                    offset = 0
                    do_sleep()
                    continue
            else:
                trigger('turn_on')
                offset = 0
                idle = True
                do_sleep()
                continue

    else:
        if idle:
            trigger('turn_off')
            idle = False
            offset = 0
    # config['idle_if_seconds']
    #print ("Sleep in end")
    do_sleep()
