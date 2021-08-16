import argparse
import sys
import DATA
import OpenPose

def main(params):
    parser = argparse.ArgumentParser(description='Run keypoint detection')
    parser.add_argument("--device", default="cpu", help="Device to inference on")
    parser.add_argument("--video_file", default="sample_video.mp4", help="Input Video")

    args = parser.parse_args()

    DATA.video_file = args.video_file

    DATA.resetDict()

    OpenPose.poseEstimaiton()
    return


if __name__ == '__main__':
    main(sys.argv)
