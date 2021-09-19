import argparse
import sys
import DATA
import pose_estimation

def main(params):
    parser = argparse.ArgumentParser(description="tf-pose-estimation realtime webcam")
    parser.add_argument("--video_file", default="", help="Input Video")

    parser.add_argument(
        "--resize",
        type=str,
        default="0x0",
        help="if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ",
    )
    parser.add_argument(
        "--resize-out-ratio",
        type=float,
        default=4.0,
        help="if provided, resize heatmaps before they are post-processed. default=1.0",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="mobilenet_thin",
        help="cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small",
    )
    parser.add_argument(
        "--show-process",
        type=bool,
        default=False,
        help="for debug purpose, if enabled, speed for inference is dropped.",
    )

    parser.add_argument(
        "--tensorrt", type=str, default="False", help="for tensorrt process."
    )
    args = parser.parse_args()

    DATA.video_file = args.video_file

    DATA.resetDict()

    pose_estimation.run(args)
    return


if __name__ == '__main__':
    main(sys.argv)
