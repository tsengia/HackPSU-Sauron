import cv2
import numpy as np
import urllib.request
import socket
from threading import Thread
from time import sleep
import sys

import mysql.connector

OUTPUT_DIR="flask-app/static/frames/"

stream_url="""https://rr1---sn-5ualdn7d.googlevideo.com/videoplayback/id/1EiC9bvVGnk.4/itag/95/source/yt_live_broadcast/expire/1649610886/ei/JrxSYq2qNoTnhwbZg4mgAw/ip/34.138.8.141/requiressl/yes/ratebypass/yes/live/1/sgoap/gir%3Dyes%3Bitag%3D140/sgovp/gir%3Dyes%3Bitag%3D136/hls_chunk_host/rr1---sn-5ualdn7d.googlevideo.com/playlist_duration/30/manifest_duration/30/gcr/us/spc/4ocVC6Sw6nQ5j0oRwOHkN2LY92Cv/vprv/1/playlist_type/DVR/mh/hd/mm/44/mn/sn-5ualdn7d/ms/lva/mv/u/mvi/1/pl/20/keepalive/yes/fexp/24001373,24007246/mt/1649588536/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,live,sgoap,sgovp,playlist_duration,manifest_duration,gcr,spc,vprv,playlist_type/sig/AOq0QJ8wRQIgNZl1uGPJiYAOin_4UcVeGKh6Py0qOzAaY6mzD-quN68CIQDRr2nW5HdnFHb0KU9qE11lX3tnCLyW1ODvrQG5llNEkA%3D%3D/lsparams/hls_chunk_host,mh,mm,mn,ms,mv,mvi,pl/lsig/AG3C_xAwRAIgb0FUd5m9FBgUZjcwxWq1FUDiUaB0FQ44aP-3fFlTYgsCIDh7speyiwE90j0Pt1eCz8okKaIj-9CLGRzDQHnNEZGZ/playlist/index.m3u8/sq/783286/goap/clen%3D81132%3Blmt%3D1649557525763146/govp/clen%3D223728%3Blmt%3D1649557525763143/dur/4.933/file/seg.ts"""

DB_ADDR = input("Input MySQL IP Addr: ")
DB_USER = input("Input MySQL User: ")
DB_PASS = input("Input MySQL password: ")

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

camera_captures = []
camera_captures.append(cv2.VideoCapture(stream_url))

def getImage(i):
    img = camera_captures[0].read()
    print("Got Image")
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
    conn = mysql.connector.connect(host=DB_ADDR, database='sauron-db-dev1', user=DB_USER, password=DB_PASS)
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
            numImages += 1
            filename = f'AnomolousImage{i}_{numImages}.jpg'
            sendSQL(conn, i, filename)
            filename = OUTPUT_DIR + filename
            cv2.imwrite(filename,img[1])


def sendSQL(conn, i, frame_file_name):
    cursor = conn.cursor()
    crisis_type = "camera detected anomoly"
    lat = camera_detection[i+1][0]
    lon = camera_detection[i+1][1]
    reporter = i
    description = f"Camera detected anomoly"
    cursor.execute(f"INSERT INTO report_list (type, latitude, longitude, reporter, description, frame) VALUES ('{crisis_type}', {lat}, {lon}, '{i}', '{description}', '{frame_file_name}');")
    conn.commit()

readImage(0)
#for i in range(NUM_STREAMS):
#    imagesThreads = Thread(target=readImage, args=(i,))
#    imagesThreads.start()
