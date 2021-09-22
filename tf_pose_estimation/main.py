import argparse
import sys
import DATA
import pose_estimation
import gait_analysis

def main(params):
    parser = argparse.ArgumentParser(description="tf-pose-estimation realtime webcam")
    parser.add_argument("--video_file", default="", help="Input Video")
    args = parser.parse_args()

    DATA.video_file = args.video_file

    DATA.resetDict()

    pointsDict = pose_estimation.run()
    gait_analysis.gaitAnalysis(pointsDict)
    return


if __name__ == '__main__':
    main(sys.argv)
