#Iki yo mung iseng cuk, kirone kliru salah nulisku koding yo dandanono
#Oleh mbok modif sak seneng udelmu

import numpy as np
import cv2
import random

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
upper_body = cv2.CascadeClassifier('haarcascade_upperbody.xml')



# Aturen nilai ambang batas, yo kisaran 80 ngasi 150
bw_threshold = 80

# Pesen sing kate mbok tampilne 
font = cv2.FONT_HERSHEY_SIMPLEX
org = (30, 30)
weared_mask_font_color = (255, 255, 255)
not_weared_mask_font_color = (0, 0, 255)
thickness = 2
font_scale = 1
weared_mask = "SIPP NGUNU, BAGUSS..."
not_weared_mask = "GAWENEN MASKERMU!!!"

# Moco video
cap = cv2.VideoCapture(0)

while 1:
    # Buka Frame pribadi
    ret, img = cap.read()
    img = cv2.flip(img,1)

    # Nggo ngubah image nyg gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert image in black and white
    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)
    #cv2.imshow('black_and_white', black_and_white)

    # deteksi raimu cukk
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # rupamu di deteksi iki
    faces_bw = face_cascade.detectMultiScale(black_and_white, 1.1, 4)


    if(len(faces) == 0 and len(faces_bw) == 0):
        cv2.putText(img, "RUPAMU GAK KETHOK!!", org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
    elif(len(faces) == 0 and len(faces_bw) == 1):
       
        cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
    else:
            for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]


            # deteksi cangkemu sing tukang ngerasani
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)

        # deteksi nek ra nganggo masker
        if(len(mouth_rects) == 0):
            cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
        else:
            for (mx, my, mw, mh) in mouth_rects:

                if(y < my < y + h):
                                        cv2.putText(img, not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)

                    #cv2.rectangle(img, (mx, my), (mx + mh, my + mw), (0, 0, 255), 3)
                    break

    # nggo delok rupamu
    cv2.imshow('Mask Detection', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# nampilno video
cap.release()
cv2.destroyAllWindows()
