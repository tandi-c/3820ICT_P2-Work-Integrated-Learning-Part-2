"""DATA.py: Description..."""

__author__      = "Barack Obama"
__copyright__   = "Copyright 2021, Planet Earth"

# Global Data
video_file = ""
pointsDict = {}
keyFeatures = ["Head", "Chest", "R_Shoulder", "R_Elbow", "R_Wrist", "L_Shoulder", "L_Elbow", "L_Wrist", "R_Hip", "R_Knee", "R_Ankle", "L_Hip", "L_Knee", "L_Ankle"]

def resetDict():
    global pointsDict
    pointsDict = {
        "Head": [(0,0)],
        "Chest": [(0,0)],
        "L_Shoulder": [(0,0)],
        "R_Shoulder": [(0,0)],
        "L_Elbow": [(0,0)],
        "R_Elbow": [(0,0)],
        "L_Wrist": [(0,0)],
        "R_Wrist": [(0,0)],
        "L_Hip": [(0,0)],
        "R_Hip": [(0,0)],
        "L_Knee": [(0,0)],
        "R_Knee": [(0,0)],
        "L_Ankle": [(0,0)],
        "R_Ankle": [(0,0)],
        "Distance": [0]
    }
    return 