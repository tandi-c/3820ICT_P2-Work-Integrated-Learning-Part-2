import argparse
import sys
import tf_pose_estimation.DATA
import tf_pose_estimation.pose_estimation
import tf_pose_estimation.gait_analysis 


def main(file_name, video_title):
    #parser = argparse.ArgumentParser(description="tf-pose-estimation realtime webcam")
    #parser.add_argument("--video_file", default="", help="Input Video")
    #args = parser.parse_args()

    tf_pose_estimation.DATA.video_file = file_name

    tf_pose_estimation.DATA.resetDict()

    pointsDict = tf_pose_estimation.pose_estimation.run()
    
    pdf_path = tf_pose_estimation.gait_analysis.gaitAnalysis(pointsDict, video_title)

    return pdf_path


if __name__ == '__main__':
    main(file_name, video_title)