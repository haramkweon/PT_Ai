import numpy as np
import time
import PoseModule as pm
import cv2


def counter(per_r, per_l, dir_r=0, dir_l=0, count_r=0, count_l=0):
    # Check for the dumbbell curls
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
    return color, count_r, count_l


def get_exercise(img, detector=pm.poseDetector, exercise=''):
    if exercise == 'curl':
        angle_r = detector.findAngle(img, 12, 14, 16)
        # Left Arm
        angle_l = detector.findAngle(img, 11, 13, 15)

    elif exercise == 'sqt':
        #sqt
        # left  hip knee ankle
        angle_l = detector.findAngle(img, 23,25,27)
        # right hip knee ankle
        angle_r = detector.findAngle(img, 24,26,28)

    elif exercise == 'side lateral raise':
        # SLR
        # Right
        angle_r = detector.findAngle(img, 16, 12, 24)
        # Left Arm
        angle_l = detector.findAngle(img, 15, 11, 23)
    elif exercise == 'push up':
        # push up
        # Right
        angle_r = detector.findAngle(img, 16, 12, 28)
        # Left Arm
        angle_l = detector.findAngle(img, 15, 11, 27)
    elif exercise == 'row':
        # 로우
        # Right
        angle_r = detector.findAngle(img, 12, 14, 24)
        # Left Arm
        angle_l = detector.findAngle(img, 11, 13, 23)
    else:# exercise == rest
        pass


def get_angle(angle_l, angle_r, exercise): ## 각도들 다 확인 해야함 직접
    if exercise == 'curl':
        exercise_angle_l = (45, 158)
        exercise_angle_r = (45, 200)
    elif exercise == 'sqt':
        exercise_angle_l = (60, 175) #  확인 완료
        exercise_angle_r = (60, 175)
    elif exercise == 'side lateral raise':
        exercise_angle_l = (5, 90)# 110
        exercise_angle_r = (5, 90)# 250
    elif exercise == 'push up': ## 확인 다시 ,, sholder rist 거리계산으로 바꿔야함
        exercise_angle_l = (45, 158)
        exercise_angle_r = (45, 200)
    elif exercise == 'row': ## 이거도 다시
        exercise_angle_l = (100, 200)
        exercise_angle_r = (100, 200)

    per_l = np.interp(angle_l, exercise_angle_l, (0, 100))  # 고쳐야함
    per_r = np.interp(angle_r, exercise_angle_r, (0, 100))  # 고쳐야함
    # print('Right:  ', angle_r, per_r)
    # print('Left:   ', angle_l, per_l)


def fps(img, pTime=0):
    # fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # put text(fps) on img
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)
