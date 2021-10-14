import cv2
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils

#model
mpPose = mp.solutions.pose
pose = mpPose.Pose()


cap = cv2.VideoCapture(0)

pTime=0
while True:
    ret, frame = cap.read()
    # cv2.imshow('frame', frame) # none mirror
    img = cv2.flip(frame, 1)
    cv2.imshow('mirror', img)  # mirror
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # success, img = cap.read()
    # imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # RGB convertion
    # results = pose.process(imgRGB)
    results = pose.process(img)
    #print(results.pose_landmarks) # 이건 좌표값 프린트

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        #pose connections 점들 이어줌 , results.pose_landmarks 점 찍어줌

        for id, lm in enumerate(results.pose_landmarks.landmark):
            h ,w ,c = img.shape
            cx, cy = int(lm.x *w), int(lm.y*h)
            # print(cx, cy)
            cv2.circle(img,(cx,cy), 5 ,(255,0,0), cv2.FILLED)
            # make bluedots


    #landmark number, google.github.io/mediapipe/solutions/pose.html



    #check frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)

cap.release()

cv2.destroyWindow()


