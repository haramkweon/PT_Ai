import numpy as np
import time
import PoseModule as pm
import cv2

detector=pm.poseDetector()

def counter(per, dir=0, count=0):
    # Check for the dumbbell curls
    color = (255, 0, 255)
    if per == 100:
        color = (0, 255, 0)
        if dir == 0:
            count += 0.5
            dir = 1
    if per == 0:
        color = (0, 255, 0)
        if dir == 1:
            count += 0.5
            dir = 0
    return color, count, dir


def get_exercise(img, exercise='curl'):
    #lmList = detector.findPosition(img,False)
    if exercise == 'curl':
        angle_r = detector.findAngle(img=img, p1=12, p2=14, p3=16, draw=True)
        # Left Arm
        angle_l = detector.findAngle(img=img, p1=11, p2=13, p3=15, draw=True)

    elif exercise == 'squart':
        #sqt
        # left  hip knee ankle
        angle_l = detector.findAngle(img=img, p1=23,p2=25,p3=27, draw=True)
        # right hip knee ankle
        angle_r = detector.findAngle(img=img, p1=24,p2=26,p3=28, draw=True)

    elif exercise == 'slr':
        # SLR
        # Right
        angle_r = detector.findAngle(img=img, p1=16, p2=12, p3=24, draw=True)
        # Left Arm
        angle_l = detector.findAngle(img=img, p1=15, p2=11, p3=23, draw=True)
    #elif exercise == 'pushup':
        # push up
        # Right
        #distance_r
    #    angle_r = detector.distance(img, 11, 15)
        # Left Arm
        #distance_l
    #    angle_l = detector.distance(img, 12, 16)
    # elif exercise == 'row':
    #     # 로우
    #     # Right
    #     angle_r = detector.findAngle(img, 12, 14, 24)
    #     # Left Arm
    #     angle_l = detector.findAngle(img, 11, 13, 23)
    else:# exercise == rest
        angle_l, angle_r = 0,0

    return angle_l, angle_r


def get_angle(exercise,angle_l, angle_r): ## 각도들 다 확인 해야함 직접
    # level 초 중 고
    exercise_angle_l=(0,0)
    exercise_angle_r=(0,0)

    if exercise == 'curl':
        exercise_angle_l = (45, 158)
        exercise_angle_r = (45, 200)
    elif exercise == 'squart':
        exercise_angle_l = (60, 175) #  확인 완료
        exercise_angle_r = (60, 175)
    elif exercise == 'slr':
        exercise_angle_l = (5, 90)# 110
        exercise_angle_r = (5, 90)# 250
    else:
        exercise_angle_l=(0,0)
        exercise_angle_r=(0,0)
    
    #elif exercise == 'pushup': ## 확인 다시 ,, sholder rist 거리계산으로 바꿔야함
    #    exercise_angle_l = (45, 158)
    #    exercise_angle_r = (45, 200)
    # elif exercise == 'row': ## 이거도 다시
    #     exercise_angle_l = (100, 200)
    #     exercise_angle_r = (100, 200)

    per_l = np.interp(angle_l, exercise_angle_l, (0, 100))  # 고쳐야함
    per_r = np.interp(angle_r, exercise_angle_r, (0, 100))  # 고쳐야함
    # print('Right:  ', angle_r, per_r)
    # print('Left:   ', angle_l, per_l)
    return per_l,per_r


def fps(img, pTime=0):
    # fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # put text(fps) on img
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

