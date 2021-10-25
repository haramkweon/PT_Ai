import time
import cv2
import PoseModule as pm

def countdown(time_sec):
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        print(time_sec)
        time_sec -= 1
    return time_sec
    print('stop')

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
set_count = 0
pTime = 0
time_sec = 5 # 30

while True:
    #fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    success, img = cap.read()
    img = detector.findPose(img, False)
    # img = cv2.resize(img, (1280, 720))
    img = cv2.flip(img, 1)  # flip mirror image
    # img = cv2.imread("PoseVideos/1.jpeg")
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)


    # print(img)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        # Right Arm
        angle_r = detector.findAngle(img, 12, 14, 16)
        # Left Arm
        angle_l = detector.findAngle(img, 11, 13, 15)
    else:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        print(time_sec)
        time_sec -= 1
        if time_sec == 0:
            set_count += 1
            time_sec = 5

        cv2.putText(img, str(int(time_sec)), (500, 500), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)



    cv2.imshow("Image", img)
    cv2.waitKey(1)
    # set_count += 1
    # print(set_count)