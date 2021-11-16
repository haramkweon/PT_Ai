import numpy as np
import time
import cv2
import PoseModule as pm
# import functions as f
from functions import *
# from pose_classification import *

# for data save
set_list = []
count_list = []
exercise_list = []
angle_list_r = []
angle_list_l = []

detector = pm.poseDetector() # call pose module

pTime = 0 # for fps calculation

v_cap = cv2.VideoCapture(0) # WEBCAM

while True:
    success, img = v_cap.read()
    img = cv2.flip(img, 1) # flip mirror image
    img = detector.findPose(img,False)
    lmList = detector.findPosition(img, False)
    # result = pose_tracker.process(image=img)
    #
    # if pose_landmarks is not None:
    #     mp_drawing.draw_landmarks(
    #         image=output_frame,
    #         landmark_list=pose_landmarks,
    #         connections=mp_pose.POSE_CONNECTIONS)
    #
    # if pose_landmarks is not None:
    #     # Get landmarks.
    #     frame_height, frame_width = output_frame.shape[0], output_frame.shape[1]
    #     pose_landmarks = np.array([[lmk.x * frame_width, lmk.y * frame_height, lmk.z * frame_width]
    #                                for lmk in pose_landmarks.landmark], dtype=np.float32)
    #     assert pose_landmarks.shape == (33, 3), 'Unexpected landmarks shape: {}'.format(pose_landmarks.shape)
    #
    #     # Classify the pose on the current frame.
    #     pose_classification = pose_classifier(pose_landmarks)
    # # if len(lmList) != 0:
    #
    #     exercise = [k for k,v in pose_classification.items() if (max(pose_classification.values())== v and v >=6)]
    #     exercise = exercise[0]
    exercise = 'curl'
    angle_l,angle_r = get_exercise(img, exercise = exercise)
    per_l, per_r = get_angle(exercise, lmList, angle_l,angle_r)
    print('Right:  ', angle_r, per_r)
    print('Left:   ', angle_l, per_l)
    color,count_l,dir_l = counter(per_l)
    color,count_r,dir_r = counter(per_r)


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

    # put fps
    fps(img)

    cv2.imshow('img', img)
    # cv2.waitKey(1)





