import cv2
import numpy as np
from networktables import NetworkTables
import logging


logging.basicConfig(level=logging.DEBUG)  # logging default ayarlarında

ip = "10.60.38.2"  # RoboRio'muzun ip'si

NetworkTables.initialize(server=ip)  # NetworkTables kullanmak istediğimi söyledim
table = NetworkTables.getTable("idris_ustam")  # idris_ustam adında yeni bir table oluşturdum

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 180)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)

lower = np.array([16, 100, 100])
upper = np.array([36, 255, 255])
clasa = np.ones([5, 5])

x = 0

while True:
    _, ret = cap.read()
    hsv = cv2.cvtColor(ret, cv2.COLOR_BGR2HSV)
    maske = cv2.inRange(hsv, lower, upper)
    erotion = cv2.erode(maske, clasa)
    _, contours, _ = cv2.findContours(erotion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    if len(contours) > 0:
        for contour in contours:
            x, y, h, w = cv2.boundingRect(contour)
            ret = cv2.rectangle(ret, (x, y), (x + w, y + h), (255, 0, 0), 3)
    else:
        x = 0

    table.putNumber("X", x)
