#!/usr/bin/env python3

import sys

from sense_hat import SenseHat

# Initialize global instance of Sense HAT API
sense = SenseHat()

k = [0, 0, 0] # Blank
r = [255, 0, 0] # Red
y = [255, 127, 0] # Yellow
g = [0, 255, 0] # Green

cross = [
k, r, k, k, k, k, r, k,
r, r, r, k, k, r, r, r,
k, r, r, r, r, r, r, k,
k, k, r, r, r, r, k, k,
k, k, r, r, r, r, k, k,
k, r, r, r, r, r, r, k,
r, r, r, k, k, r, r, r,
k, r, k, k, k, k, r, k
]

neutral_face = [
k, k, y, y, y, y, k, k,
k, y, k, k, k, k, y, k,
y, k, y, k, k, y, k, y,
y, k, k, k, k, k, k, y,
y, k, k, k, k, k, k, y,
y, k, y, y, y, y, k, y,
k, y, k, k, k, k, y, k,
k, k, y, y, y, y, k, k
]

smile_face = [
k, k, g, g, g, g, k, k,
k, g, k, k, k, k, g, k,
g, k, g, k, k, g, k, g,
g, k, k, k, k, k, k, g,
g, k, g, k, k, g, k, g,
g, k, k, g, g, k, k, g,
k, g, k, k, k, k, g, k,
k, k, g, g, g, g, k, k
]

def check_sense_stick():

    for event in sense.stick.get_events():
        if event.action == 'pressed':
            print('Stopping Smile Detector...')
            sense.show_message('STOPPING', scroll_speed=0.025)
            sys.exit()

def smile_detector(debug=False):

    import cv2

    print("Initializing Smile Detector...")
    sense.show_message('INITIALIZING', scroll_speed=0.025)

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

    cam = cv2.VideoCapture(0)
    # Keeps trying to open the camera; press SENSE Hat stick to terminate
    while not cam.isOpened():
        cam.open(0)
        check_sense_stick()

    print("Camera is opened.")

    sense.set_pixels(cross)

    while True:
        ret, img_color = cam.read()
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.05, minNeighbors=5, minSize=(45,45))

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(img_color, (x, y), (x+w, y+h), (0, 0, 255), 2)
                faceimg_color = img_color[y:y+h, x:x+w]
                faceimg_gray = img_gray[y:y+h, x:x+w]

                smiles = smile_cascade.detectMultiScale(faceimg_gray, scaleFactor=1.7, minNeighbors=3, minSize=(15, 15))

                if len(smiles) > 0:
                    sense.set_pixels(smile_face)
                    for (a, b, i, j) in smiles:
                        cv2.rectangle(faceimg_color, (a, b), (a+i, b+j), (0, 255, 0), 1)
                else:
                    sense.set_pixels(neutral_face)
        else:
            sense.set_pixels(cross)

        if debug:
            cv2.imshow('Smile Detector', img_color)
            cv2.waitKey(1)

        check_sense_stick()


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', dest='debug', default=False, help='Enable debug mode with camera window (requires X)')
    debug = parser.parse_args().debug
    assert isinstance(debug, bool)

    try:
        smile_detector(debug)
    except KeyboardInterrupt:
        sense.clear()
        raise
