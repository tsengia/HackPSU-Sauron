
import cv2
import numpy as np
import urllib.request
import socket
from threading import Thread
from time import sleep
import sys

import mysql.connector



NUM_STREAMS = 3
camera_detection = {
    1: (40.794283574885, -77.86160950086462),
    2: (40.80815035162377, -77.85774100463853),
    3: (40.80363808326678, -77.88414215231585),
    4: (40.79683529903736, -77.87240905897102),
    5: (40.78510824839257, -77.83438908645542),
    6: (40.786435036283976, -77.87215718362314),
    7: (40.785504344187125, -77.86173538975947),
    8: (40.80327992398894, -77.86239705144267),
    9: (40.791753925057584, -77.85720656188117),
    10: (40.76004196744249, -77.87800418253835),
}
def getImage(i):
    cap = cv2.VideoCapture(f"udp://127.0.0.1:300{i}")
    img = cap.read()
    # print(img)
    # cv2.imshow('lalala', img[1])
    # avg_color_per_row = np.average(img[1], axis=0)
    # avg_color = np.average(avg_color_per_row, axis=0)
    # print(avg_color)
    return img

def createIncident(img):

    center_coords = (-10,-10)
    radius = 40
    color = (255,255,255)
    thickness = 500

    img = (img[0], cv2.circle(img[1], center_coords, radius, color, thickness))
    return img


def checkIncident(img):
    if img[0]:
        for i in range(20):
            for j in range(20):
                for k in range(3):
                    if not img[1][i][j][k] == 255:
                        return False
        return True
    else:
        return False


def readImage(i):
    counter = 0
    numImages = 0
    while True:
        sleep(2)
        counter +=1
        
        img = getImage(i+1)
        if (i == 0 and counter%10 == 0) or (i == 1 and counter%20 == 0) or (i == 2 and counter%30 == 0):
            img = createIncident(img)
        print(f"{i}Incident: {checkIncident(img)}")
        if checkIncident(img):
            numImages +=1
            sendSQL(i, numImages)
            cv2.imwrite(f'AnomolousImage{i}_{numImages}.jpg',img[1])


def sendSQL(i, numImages):
    conn = mysql.connector.connect(host='35.243.244.228', database='sauron-db-dev1', user='grafana-user', password='password123456')
    cursor = conn.cursor()
    crisis_type = "camera detected anomoly"
    lat = camera_detection[i+1][0]
    lon = camera_detection[i+1][1]
    reporter = i
    description = f"~~~{numImages}~~~Camera autonomously detected anomoly"
    cursor.execute(f"INSERT INTO report_list (type, latitude, longitude, reporter, description) VALUES ('{crisis_type}', {lat}, {lon}, '{i}', '{description}');")
    conn.commit()


for i in range(NUM_STREAMS):
    imagesThreads = Thread(target=readImage, args=(i,))
    imagesThreads.start()
