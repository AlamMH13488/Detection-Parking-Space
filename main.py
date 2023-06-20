import cv2
import pickle
import cvzone
import numpy as np

# video feed
cap = cv2.VideoCapture('1.mp4')

with open('1', 'rb') as f:
        posList = pickle.load(f)

width, height = 85, 180

def checkParkingSpace(imgPro):
    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y+height,x:x+width]
        # cv2.imshow(str(x*y),imgCrop)
        count = cv2.countNonZero(imgCrop)

        if count < 1200:
            cvzone.putTextRect(img, f'available', (x+width-70,y+height-3), scale = 1, thickness = 2, offset = 0, colorR = (0, 255, 0))
            color = (0, 255, 0)
            thickness = 6
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x,y+height-3), scale = 1, thickness = 2, offset = 0, colorR = color)

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 30)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations = 2)
    checkParkingSpace(imgDilate)

    # for pos in posList:
    img = cv2.resize(img, (1100,720))
    imgMedian = cv2.resize(imgMedian, (1100,720))
    imgThreshold = cv2.resize(imgThreshold,(1100,720))
    cv2.imshow("test", img)
    # cv2.imshow("imageBlur", imgBlur)
    # cv2.imshow("imageTresh", imgThreshold)
    cv2.imshow("imageMedian", imgMedian)
    cv2.waitKey(1)
