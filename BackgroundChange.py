print('Instructions:')
print('Press A key to change the background forward.')
print('Press D key to change the background backward.')
print('Press C to capture your image with the virtual background.')
print('Press Q to quit the program.')
print('')
print('Starting your Web Camera...')

import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
from datetime import datetime

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(cv2.CAP_PROP_FPS, 60)
segmentor = SelfiSegmentation()
fpsReader = cvzone.FPS()

listImg = os.listdir('images')

imgList = []

for imgPath in listImg:
    img = cv2.imread(f'images/{imgPath}')
    imgList.append(img)

indexImg = 0

while True:
    success, img = cap.read()
    imgOut = segmentor.removeBG(img, imgList[indexImg], threshold = 0.75)

    imgStacked = cvzone.stackImages([img, imgOut], 2, 1)
    _, imgStacked = fpsReader.update(imgStacked, color = (0, 0, 255))


    cv2.imshow('Image', imgStacked)
    key = cv2.waitKey(1)
    
    if key == ord('c'):
        now = datetime.now()
        currentTime = now.strftime("%H_%M_%S")
        currentDate = now.strftime("%d_%m_%Y")
        imageName = currentTime + '__' + currentDate + '.jpg'
        cv2.imwrite(imageName, imgOut) 

    if key == ord('a'):
        if indexImg > 0:
            indexImg -= 1

    elif key == ord('d'):
        if indexImg < len(imgList) - 1:
            indexImg += 1
            
    elif key == ord('q'):
        break