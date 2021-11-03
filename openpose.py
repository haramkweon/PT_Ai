import cv2
import os
from data_load import *
def output_keypoints(frame, proto_file, weights_file, threshold, model_name, BODY_PARTS):
    global points

    net = cv2.dnn.readNetFromCaffe(proto_file, weights_file)

    # 입력 이미지의 사이즈 정의
    image_height = 368
    image_width = 368

    # 네트워크에 넣기 위한 전처리
    try:
        input_blob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (image_width, image_height), (0, 0, 0), swapRB=False, crop=False)

        # 전처리된 blob 네트워크에 입력
        net.setInput(input_blob)

        # 결과 받아오기
        out = net.forward()
        # The output is a 4D matrix :
        # The first dimension being the image ID ( in case you pass more than one image to the network ).
        # The second dimension indicates the index of a keypoint.
        # The model produces Confidence Maps and Part Affinity maps which are all concatenated.
        # For COCO model it consists of 57 parts – 18 keypoint confidence Maps + 1 background + 19*2 Part Affinity Maps. Similarly, for MPI, it produces 44 points.
        # We will be using only the first few points which correspond to Keypoints.
        # The third dimension is the height of the output map.
        out_height = out.shape[2]
        # The fourth dimension is the width of the output map.
        out_width = out.shape[3]

        # 원본 이미지의 높이, 너비를 받아오기
        frame_height, frame_width = frame.shape[:2]

        # 포인트 리스트 초기화
        points = []
        piornt_list= []
        print(f"\n============================== {model_name} Model ==============================")
        for i in range(len(BODY_PARTS)):

            # 신체 부위의 confidence map
            prob_map = out[0, i, :, :]

            # 최소값, 최대값, 최소값 위치, 최대값 위치
            min_val, prob, min_loc, point = cv2.minMaxLoc(prob_map)

            # 원본 이미지에 맞게 포인트 위치 조정
            x = (frame_width * point[0]) / out_width
            x = int(x)
            y = (frame_height * point[1]) / out_height
            y = int(y)
            if prob > threshold:  # [pointed]
                cv2.circle(frame, (x, y), 5, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, lineType=cv2.LINE_AA)
                points.append((x, y))
                print(f"[pointed] {BODY_PARTS[i]} ({i}) => prob: {prob:.5f} / x: {x} / y: {y}")
                
            else:  # [not pointed]
                cv2.circle(frame, (x, y), 5, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1, lineType=cv2.LINE_AA)

                points.append((x, y))
                print(f"[not pointed] {BODY_PARTS[i]} ({i}) => prob: {prob:.5f} / x: {x} / y: {y}")

        #cv2.imshow("Output_Keypoints", frame)
        cv2.waitKey(0)
       
        return points
    except Exception as e:
        print(str(e))
'''
def output_keypoints_with_lines(frame, POSE_PAIRS):
    print()
    for pair in POSE_PAIRS:
        part_a = pair[0]  # 0 (Head)
        part_b = pair[1]  # 1 (Neck)
        if points[part_a] and points[part_b]:
            print(f"[linked] {part_a} {points[part_a]} <=> {part_b} {points[part_b]}")
            cv2.line(frame, points[part_a], points[part_b], (0, 255, 0), 3)
        else:
            print(f"[not linked] {part_a} {points[part_a]} <=> {part_b} {points[part_b]}")

    cv2.imshow("output_keypoints_with_lines", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''

BODY_PARTS_MPI = {0: "Head", 1: "Neck", 2: "RShoulder", 3: "RElbow", 4: "RWrist",
                  5: "LShoulder", 6: "LElbow", 7: "LWrist", 8: "RHip", 9: "RKnee",
                  10: "RAnkle", 11: "LHip", 12: "LKnee", 13: "LAnkle", 14: "Chest",
               10: "RAnkle", 11: "LHip", 12: "LKnee", 13: "LAnkle", 14: "Chest",
                  15: "Background"}

POSE_PAIRS_MPI = [[0, 1], [1, 2], [1, 5], [1, 14], [2, 3], [3, 4], [5, 6],
                  [6, 7], [8, 9], [9, 10], [11, 12], [12, 13], [14, 8], [14, 11]]

# 신경 네트워크의 구조를 지정하는 prototxt 파일 (다양한 계층이 배열되는 방법 등)
protoFile_mpi = "/home/user/openpose/models/pose/mpi/pose_deploy_linevec.prototxt"


# 훈련된 모델의 weight 를 저장하는 caffemodel 파일
weightsFile_mpi = "/home/user/openpose/models/pose/mpi/pose_iter_160000.caffemodel"

# 이미지 경로
#img_list, listimageclass, listDay, listSession, listModel, listFitness
#path, imageclass, day, session, model, fitness = imageListLoader()
path = imageListLoader('./image/')

image = []
frame = []
for i in path:
    frame_mpii = cv2.imread(i)
    
    points= output_keypoints(frame=frame_mpii, proto_file=protoFile_mpi, weights_file=weightsFile_mpi,
                                threshold=0.2, model_name="MPII", BODY_PARTS=BODY_PARTS_MPI)   
    frame.append(points)

label = []
for i in frame:
    for j in i:
        for k in range(len(j)):
            label.append(j[k])
label_list = []

for i in range(0, len(label), 2):
    try:
        label_list.append(("{} {}").format(label[i], label[i+1]))
    except Exception as e:
        print(e)

count =0
flag = []
f = open('label.txt', 'w')
for j in range(0, len(label_list)): 
    f.writelines(label_list[j]+'\n')
    flag.append(15+16*j)
    for j in flag:
        if count == j:
            f.writelines("=================="+'\n')
            
        
    count+=1
    
f.close()




