import numpy as np
import time
import PoseModule as pm
import cv2

cap = cv2.VideoCapture(0) # WEBCAM
detector = pm.poseDetector()
count_r = 0
count_l = 0
dir_r = 0
dir_l = 0
angle_list_r = []
angle_list_l = []
pTime = 0

while True:
    success, img = cap.read()
    # img = cv2.resize(img, (1280, 720))
    img = cv2.flip(img, 1)
    img = detector.findPose(img,False)
    lmList = detector.findPosition(img, False)
    if len(lmList) != 0:
        distance_r = detector.distance(img, 11, 15)
        distance_l = detector.distance(img, 12, 16)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    per_l = np.interp(distance_l, (200, 450), (0, 100))  # 고쳐야함 60? 100??
    per_r = np.interp(distance_r, (200, 450), (0, 100))  # 고쳐야함
    print('Right:  ', distance_r, per_r)
    print('Left:   ', distance_l, per_l)

    color = (255, 0, 255)
    if per_r == 100:
        color = (0, 255, 0)
        if dir_r == 0:
            count_r += 0.5
            dir_r = 1
    if per_r == 0:
        color = (0, 255, 0)
        if dir_r == 1:
            count_r += 0.5
            dir_r = 0
    if per_l == 100:
        color = (0, 255, 0)
        if dir_l == 0:
            count_l += 0.5
            dir_l = 1
    if per_l == 0:
        color = (0, 255, 0)
        if dir_l == 1:
            count_l += 0.5
            dir_l = 0

    cv2.putText(img, f'R {int(per_l)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                color, 4)
    cv2.putText(img, f'L {int(per_r)} %', (700, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                color, 4)

    # Draw Curl Count
    # cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED) # draw green box
    cv2.putText(img, str(int(count_r)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 10,
                (255, 0, 0), 10)  # 15, 25 text size
    cv2.putText(img, 'L', (45, 570), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 10)
    cv2.putText(img, str(int(count_l)), (500, 670), cv2.FONT_HERSHEY_PLAIN, 10,
                (255, 0, 0), 10)  # (500, 670) 그리는 좌표 값


    cv2.imshow("Image", img)
    cv2.waitKey(1)

