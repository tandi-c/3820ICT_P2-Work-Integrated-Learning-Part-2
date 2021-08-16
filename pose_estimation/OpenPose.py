import cv2
import time
import DATA
import math

MODE = "BODY_25"

if MODE == "COCO":
    protoFile = "pose/coco/pose_deploy_linevec.prototxt"
    weightsFile = "pose/coco/pose_iter_440000.caffemodel"
    nPoints = 18
    POSE_PAIRS = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],[1,8],[8,9],[9,10],[1,11],[11,12],[12,13],[0,14],[0,15],[14,16],[15,17]]

elif MODE == "MPI" :
    protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
    weightsFile = "pose/mpi/pose_iter_160000.caffemodel"
    nPoints = 15
    POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13]]

elif MODE == "BODY_25" :
    protoFile = "pose/body_25/pose_deploy.prototxt"
    weightsFile = "pose/body_25/pose_iter_584000.caffemodel"
    nPoints = 15
    POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,8], [8,9], [9,10], [10,11], [8,12], [12,13], [13,14]]

# keyFeatures = ["Head", "Neck", "R_Shoulder", "R_Elbow", "R_Wrist", "L_Shoulder", "L_Elbow", "L_Wrist", "R_Hip", "R_Knee", "R_Ankle", "L_Hip", "L_Knee", "L_Ankle", "Sternum"]
keyFeatures = ["Head", "Chest", "R_Shoulder", "R_Elbow", "R_Wrist", "L_Shoulder", "L_Elbow", "L_Wrist", "M_Hip", "R_Hip", "R_Knee", "R_Ankle", "L_Hip", "L_Knee", "L_Ankle"]

net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
net.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)

inWidth = 368
inHeight = 368
threshold = 0.35
frameRate = 0
totalTime = 0

distances = []

def resize(frame):
    resized = cv2.resize(frame, (500, 800))
    return resized

def firstPass(frame, prevStart, prevEnd, prevChest):
    global totalTime, distances
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]

    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                            (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inpBlob)
    output = net.forward()

    H = output.shape[2]
    W = output.shape[3]
    # Empty list to store the detected keypoints
    points = []

    for i in range(nPoints):
        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        
        # Scale the point to fit on the original image
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H

        if prob > threshold : 
            # Add the point to the list if the probability is greater than the threshold
            points.append((int(x), int(y)))
        else :
            points.append(None)
    
    chest = points[1]
    hip = points[8]

    # Test for outliers
    # if (prevChest and len(distances) != 0):
    #     normDist = int(sum(distances) / len(distances))
    #     distance = int(math.sqrt( ((int(chest[0])-int(prevChest[0]))**2)+((int(chest[1])-int(prevChest[1]))**2) ))
    #     if (distance > normDist):
    #         print("skip")
    #         return frame, prevStart, prevEnd, chest, 1

    # Draw Box
    if (chest == None or hip == None):
        start_point = prevStart 
        end_point = prevEnd
    else:
        distance = int(math.sqrt( ((int(chest[0])-int(hip[0]))**2)+((int(chest[1])-int(hip[1]))**2) ))
        distances.append(distance);
        if (len(distances) > 15):
            distances.pop(0)
        normDist = int(sum(distances) / len(distances))

        start_point = (int(chest[0] - 1.5*(normDist)), int(chest[1] - 1.5*(normDist))) 
        end_point = (int(hip[0] + 1.5*(normDist)), int(hip[1] + 2.5*(normDist))) 

    if (start_point[1] < 0):
        y=0
    else:
        y=start_point[1]
    if (start_point[0] < 0):
        x=0
    else:
        x=start_point[0]
    h=end_point[1]
    w=end_point[0]
    print(y,x,h,w)
    frame = frame[y:h, x:w]
    print(frame.shape)
    try:
        frame = resize(frame)
        cv2.imshow('Output-Skeleton', frame)
    except Exception as e:
        print(str(e))
    return frame, start_point, end_point, chest, 0

def secondPass(frame, prevStart, prevEnd, t):
    global totalTime
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]

    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                            (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inpBlob)
    output = net.forward()

    H = output.shape[2]
    W = output.shape[3]
    # Empty list to store the detected keypoints
    points = []

    for i in range(nPoints):
        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        
        # Scale the point to fit on the original image
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H

        if prob > threshold : 
            # Add the point to the list if the probability is greater than the threshold
            points.append((int(x), int(y)))
            DATA.pointsDict[keyFeatures[i]].append((int(x), int(y)))
        else :
            points.append(None)
            DATA.pointsDict[keyFeatures[i]].append(None)

    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]

        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 255), 3, lineType=cv2.LINE_AA)
            cv2.circle(frame, points[partA], 8, (0, 0, 255), thickness=-2, lineType=cv2.FILLED)
            cv2.circle(frame, points[partB], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
    
    # Draw Box
    chest = points[1]
    hip = points[8]

    if (chest == None or hip == None):
        start_point = prevStart 
        end_point = prevEnd
    else:
        distance = int(math.sqrt( ((int(chest[0])-int(hip[0]))**2)+((int(chest[1])-int(hip[1]))**2) ))
        distances.append(distance);
        if (len(distances) > 15):
            distances.pop(0)
        normDist = int(sum(distances) / len(distances))
        DATA.pointsDict["Distance"].append(normDist)

        start_point = (int(chest[0] - 1.5*(normDist)), int(chest[1] - 1.5*(normDist))) 
        end_point = (int(hip[0] + 1.5*(normDist)), int(hip[1] + 2.5*(normDist))) 

    cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 2) 

    totalTime += time.time() - t
    cv2.putText(frame, "time taken = {:.2f} sec".format(time.time() - t), (50, 50), cv2.FONT_HERSHEY_COMPLEX, .5, (255, 50, 0), 2, lineType=cv2.LINE_AA)
    cv2.imshow('Output-p2', frame)
    return frame, start_point, end_point

def check_empty_img(frame):
    # Checking if the image is empty or not
    if frame is None:
        result = "Image is empty!!"
    else:
        result = "Image is not empty!!"
    return result

def poseEstimaiton():
    global frameRate
    DATA.resetDict()
    input_source = DATA.video_file
    cap = cv2.VideoCapture(input_source)
    hasFrame, frame = cap.read()
    output_video = DATA.video_file[:-4] + "_pose_estimation.avi"
    frame = resize(frame)
    vid_writer = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame.shape[1],frame.shape[0]))
    
    while cv2.waitKey(1) < 0:
        t = time.time()
        hasFrame, frame = cap.read()
        # print(check_empty_img(frame))
        if not hasFrame:
            cv2.waitKey()
            break
        prev1Start = (0,0)
        prev2Start = (0,0)
        prev1End = (1000,1000)
        prev2End = (1000,1000)
        prevChest = None
        frameRate += 1
        if frameRate % 3 != 0:
            print(frameRate)
            frame, prev1Start, prev1End, prevChest, skip = firstPass(frame, prev1Start, prev1End, prevChest)
            if (skip == 0):
                frame, prev2Start, prev2End = secondPass(frame, prev2Start, prev2End, t)
                vid_writer.write(frame)
            
    vid_writer.release()
    print(DATA.pointsDict)
    print(len(DATA.pointsDict["L_Knee"]))
    print("Total time taken = {:.2f} sec".format(totalTime))
    return