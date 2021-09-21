import argparse
import sys
import tf_pose_estimation.DATA
import tf_pose_estimation.pose_estimation
import tf_pose_estimation.gait_analysis 


def main(params):
    parser = argparse.ArgumentParser(description="tf-pose-estimation realtime webcam")
    parser.add_argument("--video_file", default="", help="Input Video")
    args = parser.parse_args()

    tf_pose_estimation.DATA.video_file = args.video_file

    tf_pose_estimation.DATA.resetDict()

    pointsDict = pose_estimation.run()
    gait_analysis.gaitAnalysis(pointsDict)
    return


if __name__ == '__main__':
    main(sys.argv)