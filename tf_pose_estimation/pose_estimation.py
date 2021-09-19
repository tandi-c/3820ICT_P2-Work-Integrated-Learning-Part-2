import logging
import time
import DATA

import cv2

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

logger = logging.getLogger("TfPoseEstimator-WebCam")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0
keyFeatures = DATA.keyFeatures

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    if h > w:
        height = 960
    else:
        width = 960

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


def run(args):
    global fps_time
    logger.debug("initialization %s : %s" % (args.model, get_graph_path(args.model)))
    w, h = model_wh(args.resize)
    if w > 0 and h > 0:
        e = TfPoseEstimator(
            get_graph_path(args.model),
            target_size=(w, h),
            trt_bool=str2bool(args.tensorrt),
        )
    else:
        e = TfPoseEstimator(
            get_graph_path(args.model),
            target_size=(432, 368),
            trt_bool=str2bool(args.tensorrt),
        )
    logger.debug("cam read+")
    cam = cv2.VideoCapture(DATA.video_file)
    ret_val, image = cam.read()
    image = image_resize(image)
    logger.info("cam image=%dx%d" % (image.shape[1], image.shape[0]))

    output_video = DATA.video_file[:-4] + "_pose_estimation.avi"
    vid_writer = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc('M','J','P','G'), 10, (image.shape[1],image.shape[0]))
    frameRate = 0

    while True:
        ret_val, image = cam.read()
        if not ret_val:
            print("Video Finished")
            break
        frameRate += 1
        if frameRate % 3 != 0:
            print(frameRate)
            image = image_resize(image)

            humans = e.inference(
                image,
                resize_to_default=(w > 0 and h > 0),
                upsample_size=args.resize_out_ratio,
            )

            image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

            human = humans[0]
            for i in range(14):
                try: 
                    a = human.body_parts[i]
                    x = a.x*image.shape[1]
                    y = a.y*image.shape[0]
                    # print(keyFeatures[i] + ": (" + str(x) + ", " + str(y) + ")")
                    DATA.pointsDict[keyFeatures[i]].append((int(x), int(y)))
                except:
                    # print("fail")
                    DATA.pointsDict[keyFeatures[i]].append(None)
                    # pass

            cv2.putText(
                image,
                "FPS: %f" % (1.0 / (time.time() - fps_time)),
                (10, 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )
            cv2.imshow("tf-pose-estimation result", image)
            fps_time = time.time()
            vid_writer.write(image)
            if cv2.waitKey(1) == 27:
                break
    vid_writer.release()
    cv2.destroyAllWindows()
    print(DATA.pointsDict)
    return
