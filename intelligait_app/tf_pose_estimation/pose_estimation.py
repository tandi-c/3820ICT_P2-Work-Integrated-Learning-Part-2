import logging
import time
import tf_pose_estimation.DATA as DATA
import math
import os

import cv2

from tf_pose_estimation.tf_pose.estimator import TfPoseEstimator
from tf_pose_estimation.tf_pose.networks import get_graph_path, model_wh

logger = logging.getLogger("TfPoseEstimator-WebCam")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

args = {
    "resize": "0x0",
    "resize_out_ratio": 4.0,
    "model": "cmu",
    "show_process": False,
    "tensorrt": "False",
}

fps_time = 0
keyFeatures = DATA.keyFeatures
distances = []
width = 0
height = 0

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def resize(frame):
    global width, height
    resized = cv2.resize(frame, (width, height))
    return resized

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    if h > w:
        height = 720
    else:
        width = 720

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))
        

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)
    # print("resized:", dim)

    # return the resized image
    return resized

def draw_box(image, start_point, end_point):
    cv2.rectangle(image, start_point, end_point, (255, 0, 0), 2) 
    return image

def fit_person(image, start_point, end_point):
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
    image = image[y:h, x:w]
    try:
        image = resize(image)
    except Exception as e:
        print(str(e))
    return image


def run(video_file = None):
    global args, fps_time, distances, width, height
    logger.debug("initialization %s : %s" % (args["model"], get_graph_path(args["model"])))
    w, h = model_wh(args["resize"])
    if w > 0 and h > 0:
        e = TfPoseEstimator(
            get_graph_path(args["model"]),
            target_size=(w, h),
            trt_bool=str2bool(args["tensorrt"]),
        )
    else:
        e = TfPoseEstimator(
            get_graph_path(args["model"]),
            target_size=(432, 368),
            trt_bool=str2bool(args["tensorrt"]),
        )
    logger.debug("cam read+")
    if (video_file != None):
        cam = cv2.VideoCapture(video_file)
    else:
        cam = cv2.VideoCapture(DATA.video_file)
    ret_val, image = cam.read()
    image = image_resize(image)
    width = image.shape[1]
    height = image.shape[0]
    logger.info("cam image=%dx%d" % (height, width))

    output_video_temp = DATA.video_file[:-4] + "_pose_estimation_temp.mp4"
    output_video = DATA.video_file[:-4] + "_pose_estimation.mp4"
    vid_writer = cv2.VideoWriter(output_video_temp, cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))
    # vid_writer = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc('M','J','P','G'), 10, (width, height))
    frameRate = 0

    while True:
        ret_val, image = cam.read()
        if not ret_val:
            print("Video Finished")
            break
        frameRate += 1
        if frameRate % 3 != 0:
            print(frameRate)
            image = resize(image)

            humans = e.inference(
                image,
                resize_to_default=(w > 0 and h > 0),
                upsample_size=args["resize_out_ratio"],
            )

            human = humans[0]

            image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
            
            for i in range(14):
                try: 
                    a = human.body_parts[i]
                    x = a.x*image.shape[1]
                    y = a.y*image.shape[0]
                    DATA.pointsDict[keyFeatures[i]].append((int(x), int(y)))
                except:
                    DATA.pointsDict[keyFeatures[i]].append(None)

            cv2.putText(
                image,
                "FPS: %f" % (1.0 / (time.time() - fps_time)),
                (10, 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )
            # cv2.imshow("tf-pose-estimation result", image)
            fps_time = time.time()
            vid_writer.write(image)
            if cv2.waitKey(1) == 27:
                break
    vid_writer.release()
    os.system("ffmpeg -i {} -vcodec libx264 {}".format(output_video_temp, output_video))
    os.remove(output_video_temp)
    cv2.destroyAllWindows()
    return DATA.pointsDict