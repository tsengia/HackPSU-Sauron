import cv2
import numpy as np
import urllib.request
import socket
from threading import Thread
from time import sleep
import sys
import subprocess

import mysql.connector

OUTPUT_DIR="flask-app/static/frames/"

stream_prefix="https://youtube.com/watch?v="
stream_ids=["YByJ2h0T5JY","1EiC9bvVGnk","y0pEGfaKi50"]
stream_formats=[95,95,95]

DB_ADDR = input("Input MySQL IP Addr: ")
DB_USER = input("Input MySQL User: ")
DB_PASS = input("Input MySQL password: ")

# Create our input streams
camera_captures = []
for i,sid in enumerate(stream_ids):
    # Grab the actual stream using youtube-dl
    stream_url = stream_prefix + sid
    print("Grabbing stream for: " + stream_url)
    
    stream_uri = subprocess.run(["youtube-dl","-f",str(stream_formats[i]),"-g",stream_url], text=True, stdout=subprocess.PIPE)
    if stream_uri.returncode == 0:
        camera_captures.append(cv2.VideoCapture(str(stream_uri.stdout).strip()))
        print("Added capture for " + sid + ".")
    else:
        print("Failed to add capture for " + sid + "!")

camera_location = {
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
    ret,img = camera_captures[i].read()
    return ret,img

def createIncident(img):
    center_coords = (-10,-10)
    radius = 40
    color = (255,255,255)
    thickness = 500
    img = cv2.circle(img, center_coords, radius, color, thickness)
    return img


def checkIncident(img):
    for i in range(20):
        for j in range(20):
            for k in range(3):
                if not img[i][j][k] == 255:
                    return False
        return True

def readImage(i):
    global DB_ADDR, DB_USER
    conn = mysql.connector.connect(host=DB_ADDR, database='sauron-db-dev1', user=DB_USER, password=DB_PASS)
    print("Runner #" + str(i) + " Connected to DB.")
    counter = 0
    numImages = 0
    anom_counter = 0
    while True:
        counter += 1
        anom_counter += 1
        
        ret, img = getImage(i)
        if not ret:
            print("Bad return value for getImage!")
            continue
        if anom_counter >= 60:
            anom_counter = 0
            img = createIncident(img)
        #print(f"{i}Incident: {checkIncident(img)}")
        if checkIncident(img):
            numImages += 1
            filename = f'AnomolousImage{i}_{numImages}.jpg'
            sendSQL(conn, i, filename)
            filename = OUTPUT_DIR + filename
            cv2.imwrite(filename,img)

def sendSQL(conn, i, frame_file_name):
    cursor = conn.cursor()
    crisis_type = "Camera Detected Traffic Anomoly"
    lat = camera_location[i+1][0]
    lon = camera_location[i+1][1]
    reporter = "Camera #" + str(i)
    description = f"Camera detected anomoly."
    cursor.execute(f"INSERT INTO report_list (type, latitude, longitude, reporter, description, frame) VALUES ('{crisis_type}', {lat}, {lon}, '{i}', '{description}', '{frame_file_name}');")
    conn.commit()

##readImage(0)
for i in range(0,len(camera_captures)):
    imagesThreads = Thread(target=readImage, args=(i,))
    imagesThreads.start()
