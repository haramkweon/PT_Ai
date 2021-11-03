import os


def imageListLoader(root_path):
    root = root_path
    img_list = []
    
    NUMBER_OF_SESSION = 9
    NUMBER_OF_MODEL = 5
    NUMBER_OF_FITNESS = 32

    listimageclass = ['DUMBEL_CURL']
    listSession = [] 
    listModel = []
    #561-1-3-27-Z87_A ~ 592
    listFitness = []

    
    for idx in range(NUMBER_OF_SESSION): #1, 2, 3, 4, 5, 6, 7
        sessionname = str('%d' % (idx+1))
        listSession.append(sessionname)

    for idx in range(NUMBER_OF_MODEL): #A, B, C, D, E
        modelname = chr(idx+65)
        listModel.append(modelname)

    for model in range(5):
        for idx in range(NUMBER_OF_FITNESS):
            fitnessName = str('4'+str(idx + 41)+'-2-1-20-Z5_{}'.format(chr(model+65)))
            listFitness.append(fitnessName)
    
    listClass = os.listdir(root+listimageclass[0])
    print(listClass)
    for classId in listClass:
        if not os.path.isdir(root+listimageclass[0]+'/'+classId):
            continue
    
        for imageclass in listimageclass:
            for session in listSession:
                for model in listModel:
                    for fitness in listFitness:
                        sub_path = root + imageclass + '/' + classId + '/' + session + '/' + model + '/' + fitness + '/'
                        if os.path.isdir(sub_path) is False:
                            continue

                        listImage = os.listdir(sub_path)

                        for imageName in listImage:
                            ftitle, ext = os.path.splitext(imageName)
                            if ext != '.jpg':
                                continue

                            img_list.append(sub_path+imageName)


    return img_list
    

