import numpy as np
import time
import PoseModule as pm
import cv2

ex_list = ['curl','pushup','slr','squart']
# print(ex_list[0])
detector = pm.poseDetector()

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


def get_exercise(img, lmList, detector=detector, exercise='curl'):
    # lmList = detector.findPosition(img, False)
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

    elif exercise == 'slr':
        # SLR
        # Right
        angle_r = detector.findAngle(img, 16, 12, 24)
        # Left Arm
        angle_l = detector.findAngle(img, 15, 11, 23)
    elif exercise == 'pushup':
        # push up
        # Right
        #distance_r
        angle_r = detector.distance(img, 11, 15)
        # Left Arm
        #distance_l
        angle_l = detector.distance(img, 12, 16)
    # elif exercise == 'row':
    #     # 로우
    #     # Right
    #     angle_r = detector.findAngle(img, 12, 14, 24)
    #     # Left Arm
    #     angle_l = detector.findAngle(img, 11, 13, 23)
    else:# exercise == rest
        pass
    return angle_l, angle_r


def get_angle(exercise,angle_l, angle_r): ## 각도들 다 확인 해야함 직접
    # level 초 중 고
    if exercise == 'curl':
        exercise_angle_l = (45, 158)
        exercise_angle_r = (45, 200)
    elif exercise == 'sqt':
        exercise_angle_l = (60, 175) #  확인 완료
        exercise_angle_r = (60, 175)
    elif exercise == 'slr':
        exercise_angle_l = (5, 90)# 110
        exercise_angle_r = (5, 90)# 250
    elif exercise == 'pushup': ## 확인 다시 ,, sholder rist 거리계산으로 바꿔야함
        exercise_angle_l = (45, 158)
        exercise_angle_r = (45, 200)
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


def main():
    v_cap = cv2.VideoCapture(0)  # WEBCAM

    while True:
        exercise= ex_list[2]
        success, img = v_cap.read()
        img = cv2.flip(img, 1)  # flip mirror image
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        angle_l,angle_r = get_exercise(img, lmList, detector=detector, exercise=exercise )
        per_l,per_r = get_angle(exercise,angle_l, angle_r)
        print(per_l,per_r)

        cv2.imshow('img',img)
        cv2.waitKey(1)

main()