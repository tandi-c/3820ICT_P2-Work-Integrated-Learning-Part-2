# Intelligait
# 3820ICT - Work Integrated Learning Project

Intelligait is a web application for the analysis of a persons gait. It uses Tensorflow's pose estimation technology to analyse the hip, knee, and ankle joints to visualise any differences between the left and right joints throughout their gait cycle. 

## Install Dependencies

Must have python, pip and swig installed.

Then run the following command:
`pip install -r requirements.txt`

### To use CMU model

Download graph_opt.pb from http://www.mediafire.com/file/qlzzr20mpocnpa3/graph_opt.pb and place in `\tf_pose_estimation\models\graph\cmu`

