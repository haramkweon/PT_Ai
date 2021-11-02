import cv2
import os

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

        
        cv2.imshow("Output_Keypoints", frame)
        cv2.waitKey(0)
        # print(points)
        # print(len(points))
        return frame, points
    except Exception as e:
        print(str(e))

# def output_keypoints_with_lines(frame, POSE_PAIRS):
#     print()
#     for pair in POSE_PAIRS:
#         part_a = pair[0]  # 0 (Head)
#         part_b = pair[1]  # 1 (Neck)
#         if points[part_a] and points[part_b]:
#             print(f"[linked] {part_a} {points[part_a]} <=> {part_b} {points[part_b]}")
#             cv2.line(frame, points[part_a], points[part_b], (0, 255, 0), 3)
#         else:
#             print(f"[not linked] {part_a} {points[part_a]} <=> {part_b} {points[part_b]}")
#
#     cv2.imshow("output_keypoints_with_lines", frame)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

BODY_PARTS_MPI = {0: "Head", 1: "Neck", 2: "RShoulder", 3: "RElbow", 4: "RWrist",
                  5: "LShoulder", 6: "LElbow", 7: "LWrist", 8: "RHip", 9: "RKnee",
                  10: "RAnkle", 11: "LHip", 12: "LKnee", 13: "LAnkle", 14: "Chest",
                  15: "Background"}

POSE_PAIRS_MPI = [[0, 1], [1, 2], [1, 5], [1, 14], [2, 3], [3, 4], [5, 6],
                  [6, 7], [8, 9], [9, 10], [11, 12], [12, 13], [14, 8], [14, 11]]
'''
BODY_PARTS_COCO = {0: "Nose", 1: "Neck", 2: "RShoulder", 3: "RElbow", 4: "RWrist",
                   5: "LShoulder", 6: "LElbow", 7: "LWrist", 8: "RHip", 9: "RKnee",
                   10: "RAnkle", 11: "LHip", 12: "LKnee", 13: "LAnkle", 14: "REye",
                   15: "LEye", 16: "REar", 17: "LEar", 18: "Background"}

POSE_PAIRS_COCO = [[0, 1], [0, 14], [0, 15], [1, 2], [1, 5], [1, 8], [1, 11], [2, 3], [3, 4],
                   [5, 6], [6, 7], [8, 9], [9, 10], [12, 13], [11, 12], [14, 16], [15, 17]]

BODY_PARTS_BODY_25 = {0: "Nose", 1: "Neck", 2: "RShoulder", 3: "RElbow", 4: "RWrist",
                      5: "LShoulder", 6: "LElbow", 7: "LWrist", 8: "MidHip", 9: "RHip",
                      10: "RKnee", 11: "RAnkle", 12: "LHip", 13: "LKnee", 14: "LAnkle",
                      15: "REye", 16: "LEye", 17: "REar", 18: "LEar", 19: "LBigToe",
                      20: "LSmallToe", 21: "LHeel", 22: "RBigToe", 23: "RSmallToe", 24: "RHeel", 25: "Background"}

POSE_PAIRS_BODY_25 = [[0, 1], [0, 15], [0, 16], [1, 2], [1, 5], [1, 8], [8, 9], [8, 12], [9, 10], [12, 13], [2, 3],
                      [3, 4], [5, 6], [6, 7], [10, 11], [13, 14], [15, 17], [16, 18], [14, 21], [19, 21], [20, 21],
                      [11, 24], [22, 24], [23, 24]]
'''
# 신경 네트워크의 구조를 지정하는 prototxt 파일 (다양한 계층이 배열되는 방법 등)
protoFile_mpi = "C:\openpose-master\openpose-master\models\pose\mpi\pose_deploy_linevec.prototxt"
#protoFile_mpi_faster = "C:\openpose-master\openpose-master\models\pose\mpi\pose_deploy_linevec_faster_4_stages.prototxt"
#protoFile_coco = "C:\\openpose\\models\\pose\\coco\\pose_deploy_linevec.prototxt"
#protoFile_body_25 = "C:\\openpose\\models\\pose\\body_25\\pose_deploy.prototxt"

# 훈련된 모델의 weight 를 저장하는 caffemodel 파일
weightsFile_mpi = "C:\openpose-master\openpose-master\models\pose\mpi\pose_iter_160000.caffemodel"
#weightsFile_coco = "C:\\openpose\\models\\pose\\coco\\pose_iter_440000.caffemodel"
#weightsFile_body_25 = "C:\\openpose\\models\\pose\\body_25\\pose_iter_584000.caffemodel"

# 이미지 경로
path = "C:/qwer/"

file_list = os.listdir(path)
image = []
for i in file_list:

    path_list = os.path.join(path, i)
    image.append(path_list)
print(image)    

# 키포인트를 저장할 빈 리스트
'''

i = 0
for file_name in file_list:

# 이미지 읽어오기
    frame_mpii = cv2.imread(path+file_name)
    #frame_coco = frame_mpii.copy()

    #frame_body_25 = frame_mpii.copy()

    # MPII Model
    frame_MPII, points= output_keypoints(frame=frame_mpii, proto_file=protoFile_mpi, weights_file=weightsFile_mpi,
                                threshold=0.2, model_name="MPII", BODY_PARTS=BODY_PARTS_MPI)
    #points.append(list(points))

    print(f"[pointed] {BODY_PARTS[i]} ({i}) => prob: {prob:.5f} / x: {x} / y: {y}")
                

            else:  # [not pointed]


                cv2.circle(frame, (x, y), 5, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1, lineType=cv2.LINE_AA)

                points.append((x, y))
                print(f"[not pointed] {BODY_PARTS[i]} ({i}) => prob: {prob:.5f} / x: {x} / y: {y}")
pen("label"+str(i))
        #f.write(str(points_list))
        #f.write(str(list(points)))

    
    #output_keypoints_with_lines(frame=frame_MPII, POSE_PAIRS=POSE_PAIRS_MPI)

    
    
    # COCO Model
    frame_COCO = output_keypoints(frame=frame_coco, proto_file=protoFile_coco, weights_file=weightsFile_coco,
                                threshold=0.2, model_name="COCO", BODY_PARTS=BODY_PARTS_COCO)
    output_keypoints_with_lines(frame=frame_COCO, POSE_PAIRS=POSE_PAIRS_COCO)

    # BODY_25 Model
    
    
    
    
    rame_BODY_25 = output_keypoints(frame=frame_body_25, proto_file=protoFile_body_25, weights_file=weightsFile_body_25,
                                threshold=0.2, model_name="BODY_25", BODY_PARTS=BODY_PARTS_BODY_25)
    output_keypoints_with_lines(frame=frame_BODY_25, POSE_PAIRS=POSE_PAIRS_BODY_25)
    '''
frame = []
for i in image:
    frame_mpii = cv2.imread(i)

    frame_MPII, points= output_keypoints(frame=frame_mpii, proto_file=protoFile_mpi, weights_file=weightsFile_mpi,
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
        print(len(label))
    except Exception as e:
        print(e)

f = open('label.txt', 'w')
for j in range(0, len(label_list)):
    f.writelines(label_list[j]+'\n')
    print(label_list[j])
    if j == 15:
        f.writelines("=================="+'\n')
    elif j == 31:
        f.writelines("=================="+'\n')
    elif j == 47:
        f.writelines("=================="+'\n')
    elif j == 63:
        f.writelines("=================="+'\n')
    elif j == 79:
        f.writelines("=================="+'\n')
    elif j == 95:
        f.writelines("=================="+'\n')
    elif j == 111:
        f.writelines("=================="+'\n')
    elif j == 127:
        f.writelines("=================="+'\n')
    elif j == 143:
        f.writelines("=================="+'\n')
    elif j == 159:
        f.writelines("=================="+'\n')
    elif j == 175:
        f.writelines("=================="+'\n')
    elif j == 191:
        f.writelines("=================="+'\n')
    elif j == 207:
        f.writelines("=================="+'\n')
    elif j == 223:
        f.writelines("=================="+'\n')
    elif j == 239:
        f.writelines("=================="+'\n')
    elif j == 255:
        f.writelines("=================="+'\n')
    elif j == 271:
        f.writelines("=================="+'\n')
    elif j == 287:
        f.writelines("=================="+'\n')
    elif j == 303:
        f.writelines("=================="+'\n')
    elif j == 319:
        f.writelines("=================="+'\n')
    elif j == 335:
        f.writelines("=================="+'\n')
    elif j == 351:
        f.writelines("=================="+'\n')
    elif j == 367:
        f.writelines("=================="+'\n')
    elif j == 383:
        f.writelines("=================="+'\n')
    elif j == 399:
        f.writelines("=================="+'\n')
    elif j == 415:
        f.writelines("=================="+'\n')
    elif j == 431:
        f.writelines("=================="+'\n')
    elif j == 447:
        f.writelines("=================="+'\n')
    elif j == 463:
        f.writelines("=================="+'\n')
    elif j == 479:
        f.writelines("=================="+'\n')
    elif j == 495:
        f.writelines("=================="+'\n')
f.close()




