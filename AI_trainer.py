import numpy as np
import time
import cv2
from functions import *
from pose_classification import *

import sys
from MainWindow import MainWindow
from PyQt5.QtWidgets import *
import threading



def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    
    win.show()
    sys.exit(app.exec_())

global dir_r
global dir_l
global count_r
global count_l

set_list = []
count_list = []
exercise_list = []
angle_list_r = []
angle_list_l = []


pTime = 0 # for fps calculation

v_cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

video_n_frames = v_cap.get(cv2.CAP_PROP_FRAME_COUNT)
video_fps = v_cap.set(cv2.CAP_PROP_FPS, 30)
video_width = int(v_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280))
video_height = int(v_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720))


count_l, count_r = 0, 0
dir_l, dir_r = 0, 0
while True:
    success, img = v_cap.read()

    img = cv2.flip(img, 1) # flip mirror image
    img = detector.findPose(img,False)
    lmList = detector.findPosition(img, False)
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose_tracker.process(image=img1)
    pose_landmarks = result.pose_landmarks
    output_frame = img1.copy()
    if pose_landmarks is not None:
        mp_drawing.draw_landmarks(
        image=output_frame,
        landmark_list=pose_landmarks,
        connections=mp_pose.POSE_CONNECTIONS)

    if pose_landmarks is not None:
        # Get landmarks.
        frame_height, frame_width = output_frame.shape[0], output_frame.shape[1]
        pose_landmarks = np.array([[lmk.x * frame_width, lmk.y * frame_height, lmk.z * frame_width]
                                    for lmk in pose_landmarks.landmark], dtype=np.float32)
        assert pose_landmarks.shape == (33, 3), 'Unexpected landmarks shape: {}'.format(pose_landmarks.shape)

        # Classify the pose on the current frame.
        pose_classification = pose_classifier(pose_landmarks)
        #print(pose_classification)
        result = [k for k,v in pose_classification.items() if (max(pose_classification.values()) == v and v >=6)]
        if len(result) == 0:
            result.append("None")
        exercise = result[0]
        print(exercise)
        angle_l,angle_r = get_exercise(img, exercise)
        per_l, per_r = get_angle(exercise, angle_l,angle_r)
        print('Right:  ', angle_r, per_r)
        print('Left:   ', angle_l, per_l)
        color,dir_l,count_l = counter(per_l,dir_l, count_l)
        color,dir_r,count_r = counter(per_r,dir_r,count_r)

        if len(lmList) != 0:
            # cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)
        
            fps(img)
            cv2.putText(img, f'R {int(per_l)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)
            cv2.putText(img, f'L {int(per_r)} %', (700, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)
            # Draw Curl Count
            # cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED) # draw green box
            cv2.putText(img, str(int(count_r)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 10)  # 15, 25 text size
            cv2.putText(img, 'L', (45, 570), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 10)
            cv2.putText(img, str(int(count_l)), (500, 670), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 10)  # (500, 670) 그리는 좌표 값
            
        
    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
t=threading.Thread(target=main)
t.start()


v_cap.release()
cv2.destroyAllWindows()

    